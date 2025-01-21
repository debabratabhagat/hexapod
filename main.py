from adafruit_servokit import ServoKit
import time
import numpy as np

# Initialize ServoKit instances for two PCA9685 boards
board1 = ServoKit(channels=16, address=0x40)
board2 = ServoKit(channels=16, address=0x41)

# Define servo pins for each leg
LEG_SERVOS = {
    "right1": {"coxa": 3, "femur": 7, "tibia": 6},
    "right2": {"coxa": 5, "femur": 4, "tibia": 3},
    "right3": {"coxa": 15, "femur": 14, "tibia": 13},
    "left1": {"coxa": 13, "femur": 14, "tibia": 15},
    "left2": {"coxa": 5, "femur": 4, "tibia": 3},
    "left3": {"coxa": 6, "femur": 7, "tibia": 2},
}

UP_ANGLES = {
    "right1": {"coxa": 80, "femur": 85, "tibia": 110},
    "right2": {"coxa": 80, "femur": 80, "tibia": 90},
    "right3": {"coxa": 70, "femur": 85, "tibia": 85},
    "left1": {"coxa": 65, "femur": 70, "tibia": 85},
    "left2": {"coxa": 75, "femur": 85, "tibia": 90},
    "left3": {"coxa": 65, "femur": 80, "tibia": 85},
}

# Define stance angles
STANCE_ANGLES = {
    "right1": {"coxa": 60, "femur": 90, "tibia": 100},
    "right2": {"coxa": 70, "femur": 85, "tibia": 95},
    "right3": {"coxa": 50, "femur": 90, "tibia": 90},
    "left1": {"coxa": 70, "femur": 85, "tibia": 95},
    "left2": {"coxa": 60, "femur": 90, "tibia": 100},
    "left3": {"coxa": 50, "femur": 90, "tibia": 90},
}

# Offset for lift and swing phases
LIFT_OFFSET = 30
SWING_OFFSET = 30


# Function to calculate lift and swing angles dynamically
def calculate_dynamic_angles(stance_angles, lift_offset, swing_offset):
    lift_angles = {}
    swing_angles = {}

    for leg, angles in stance_angles.items():
        lift_angles[leg] = {
            "coxa": angles["coxa"],
            "femur": angles["femur"] + lift_offset,  # Lift femur up
            "tibia": angles["tibia"] + lift_offset,  # Extend tibia
        }
        swing_angles[leg] = {
            "coxa": angles["coxa"] + swing_offset
            if "left" in leg
            else angles["coxa"] - swing_offset,
            
            "femur": angles["femur"],
            "tibia": angles["tibia"],
        }

    return lift_angles, swing_angles


# Calculate lift and swing angles
LIFT_ANGLES, SWING_ANGLES = calculate_dynamic_angles(
    STANCE_ANGLES, LIFT_OFFSET, SWING_OFFSET
)


def interpolate(start_angle, end_angle, steps):
    return np.linspace(start_angle, end_angle, steps)


def move_smooth(board, pin, start_angle, end_angle, steps):
    angles = interpolate(start_angle, end_angle, steps)
    for angle in angles:
        board.servo[pin].angle = angle
        time.sleep(0.01)


# Function to move a single servo
def move_servo(board, pin, angle):
    board.servo[pin].angle = angle


# Function to move a leg
def move_leg_smooth(leg_name, start_angles, end_angles):
    board = board1 if leg_name.startswith("right") else board2
    pins = LEG_SERVOS[leg_name]

    move_smooth(board, pins["coxa"], start_angles["coxa"], end_angles["coxa"], 10)
    move_smooth(board, pins["femur"], start_angles["femur"], end_angles["femur"], 10)
    move_smooth(board, pins["tibia"], start_angles["tibia"], end_angles["tibia"], 10)


def move_leg(leg_name, angles):
    board = board1 if leg_name.startswith("right") else board2
    pins = LEG_SERVOS[leg_name]

    move_servo(board, pins["coxa"], angles["coxa"])
    move_servo(board, pins["femur"], angles["femur"])
    move_servo(board, pins["tibia"], angles["tibia"])


# Function to set all legs to specific angles
def set_leg_positions(angles):
    for leg_name, angle_set in angles.items():
        move_leg(leg_name, angle_set)


# Tripod gait function
def tripod_gait():
    # Tripod groups
    TRIPOD_1 = ["right1", "left2", "right3"]
    TRIPOD_2 = ["left1", "right2", "left3"]

    while True:
        # Move Tripod 1: Lift, Swing, Stand
        for leg in TRIPOD_1:
            move_leg_smooth(leg, STANCE_ANGLES[leg], LIFT_ANGLES[leg])
        time.sleep(0.3)

        for leg in TRIPOD_1:
            move_leg_smooth(leg, STANCE_ANGLES[leg], SWING_ANGLES[leg])
        time.sleep(0.3)

        for leg in TRIPOD_1:
            move_leg_smooth(leg, LIFT_ANGLES[leg], STANCE_ANGLES[leg])
        time.sleep(0.3)

        # Move Tripod 2: Lift, Swing, Stand
        for leg in TRIPOD_2:
            move_leg_smooth(leg, STANCE_ANGLES[leg], LIFT_ANGLES[leg])
        time.sleep(0.3)

        for leg in TRIPOD_2:
            move_leg_smooth(leg, STANCE_ANGLES[leg], SWING_ANGLES[leg])
        time.sleep(0.3)

        for leg in TRIPOD_2:
            move_leg_smooth(leg, LIFT_ANGLES[leg], STANCE_ANGLES[leg])
        time.sleep(0.3)


# Main execution
if __name__ == "__main__":
    try:
        print("Starting hexapod movement...")
        # Set all legs to initial standing position
        set_leg_positions(UP_ANGLES)
        time.sleep(2)
        # set_leg_positions(STANCE_ANGLES)
        # time.sleep(2)
        # Begin tripod gait
        # tripod_gait()
    except KeyboardInterrupt:
        print("Stopping hexapod.")

        print("do you want to de power the servos?")
        value = input("Enter y/n: ")

        if value == "y":
            print("De-powering servos...")
            for i in range(16):
                board1.servo[i].angle = None
                board2.servo[i].angle = None
            print("Servos de-powered.")
        else:
            print("Servos still powered.")
