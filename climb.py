import numpy as np
from adafruit import ServoKit
import time

# Define servo boards
board1 = ServoKit(channels=16, address=0x40)
board2 = ServoKit(channels=16, address=0x41)

# Servo mapping for each leg
LEG_SERVOS = {
    "right1": {"coxa": 9, "femur": 8, "tibia": 7},
    "right2": {"coxa": 12, "femur": 11, "tibia": 10},
    "right3": {"coxa": 15, "femur": 14, "tibia": 13},
    "left1": {"coxa": 15, "femur": 14, "tibia": 13},
    "left2": {"coxa": 12, "femur": 11, "tibia": 10},
    "left3": {"coxa": 9, "femur": 8, "tibia": 7},
}


# Function to set servo angles smoothly
def set_servo_angle(leg, joint, target_angle, duration=1.0, steps=50):
    board = board1 if "right" in leg else board2
    pin = LEG_SERVOS[leg][joint]
    current_angle = board.servo[pin].angle or 90
    angles = np.linspace(current_angle, target_angle, steps)
    for angle in angles:
        board.servo[pin].angle = angle
        time.sleep(duration / steps)


def up_pos():
    set_servo_angle("right1", "coxa", 100)
    set_servo_angle("right1", "femur", 100)  # + = +
    set_servo_angle("right1", "tibia", 90)  # + = -

    set_servo_angle("right2", "coxa", 95)
    set_servo_angle("right2", "femur", 110)
    set_servo_angle("right2", "tibia", 90)

    set_servo_angle("right3", "coxa", 90)
    set_servo_angle("right3", "femur", 95)
    set_servo_angle("right3", "tibia", 90)

    set_servo_angle("left1", "coxa", 95)
    set_servo_angle("left1", "femur", 85)
    set_servo_angle("left1", "tibia", 90)

    set_servo_angle("left2", "coxa", 90)
    set_servo_angle("left2", "femur", 85)
    set_servo_angle("left2", "tibia", 110)

    set_servo_angle("left3", "coxa", 90)
    set_servo_angle("left3", "femur", 95)
    set_servo_angle("left3", "tibia", 90)


stand_pos_angles = {
    # right legs
    "right1": {"coxa": 100, "femur": 145, "tibia": 140},
    "right2": {"coxa": 95, "femur": 140, "tibia": 125},
    "right3": {"coxa": 90, "femur": 135, "tibia": 150},
    # left legs
    "left1": {"coxa": 95, "femur": 135, "tibia": 140},
    "left2": {"coxa": 90, "femur": 125, "tibia": 150},
    "left3": {"coxa": 90, "femur": 140, "tibia": 145},
}


def stand_pos():
    set_servo_angle("right1", "coxa", stand_pos_angles["right1"]["coxa"])
    set_servo_angle("right1", "femur", stand_pos_angles["right1"]["femur"])  # + = +
    set_servo_angle("right1", "tibia", stand_pos_angles["right1"]["tibia"])  # + = -

    set_servo_angle("right2", "coxa", stand_pos_angles["right2"]["coxa"])
    set_servo_angle("right2", "femur", stand_pos_angles["right2"]["femur"])  # + = +
    set_servo_angle("right2", "tibia", stand_pos_angles["right2"]["tibia"])  # + = -

    set_servo_angle("right3", "coxa", stand_pos_angles["right3"]["coxa"])
    set_servo_angle("right3", "femur", stand_pos_angles["right3"]["femur"])  # + = +
    set_servo_angle("right3", "tibia", stand_pos_angles["right3"]["tibia"])  # + = -

    set_servo_angle("left1", "coxa", stand_pos_angles["left1"]["coxa"])
    set_servo_angle("left1", "femur", stand_pos_angles["left1"]["femur"])  # + = +
    set_servo_angle("left1", "tibia", stand_pos_angles["left1"]["tibia"])  # + = -

    set_servo_angle("left2", "coxa", stand_pos_angles["left2"]["coxa"])
    set_servo_angle("left2", "femur", stand_pos_angles["left2"]["femur"])  # + = +
    set_servo_angle("left2", "tibia", stand_pos_angles["left2"]["tibia"])  # + = -

    set_servo_angle("left3", "coxa", stand_pos_angles["left3"]["coxa"])
    set_servo_angle("left3", "femur", stand_pos_angles["left3"]["femur"])  # + = +
    set_servo_angle("left3", "tibia", stand_pos_angles["left3"]["tibia"])  # + = -


# Step 1: Adjust balance by moving middle legs forward
def adjust_balance():
    set_servo_angle("right2", "femur", 120)
    set_servo_angle("left2", "femur", 120)

    set_servo_angle("right2", "coxa", 60)
    set_servo_angle("left2", "coxa", 120)

    set_servo_angle("right2", "femur", 90)
    set_servo_angle("left2", "femur", 90)


# Step 2: Place front legs on stair
def front_legs_climb():
    set_servo_angle("right1", "femur", 150)
    set_servo_angle("right1", "tibia", 120)
    set_servo_angle("right1", "coxa", 45)

    time.sleep(0.5)

    set_servo_angle("right1", "femur", 120)
    set_servo_angle("right1", "tibia", 160)

    time.sleep(0.5)

    set_servo_angle("left1", "femur", 150)
    set_servo_angle("left1", "tibia", 120)
    set_servo_angle("left1", "coxa", 45)

    time.sleep(0.5)

    set_servo_angle("left1", "femur", 120)
    set_servo_angle("left1", "tibia", 160)


# Step 3: Move body forward
def move_body_forward():
    set_servo_angle("right3", "femur", 120)
    set_servo_angle("right3", "tibia", 120)
    set_servo_angle("right3", "coxa", 60)

    time.sleep(0.5)
    set_servo_angle("right3", "femur", 90)
    set_servo_angle("right3", "tibia", 90)

    time.sleep(0.5)
    set_servo_angle("left3", "femur", 120)
    set_servo_angle("left3", "tibia", 120)
    set_servo_angle("left3", "coxa", 120)

    time.sleep(0.5)
    set_servo_angle("left3", "femur", 90)
    set_servo_angle("left3", "tibia", 90)

    time.sleep(0.5)
    set_servo_angle("right3", "coxa", 90)
    set_servo_angle("left3", "coxa", 90)
    set_servo_angle("right2", "coxa", 90)
    set_servo_angle("left2", "coxa", 90)


# Step 4: Place middle legs on stair
def middle_legs_climb():
    pass


# Step 5: Move body forward again
def final_body_forward():
    pass


# Step 6: Place rear legs on stair
def rear_legs_climb():
    pass


# Execute the stair climbing sequence
def climb_stair():
    print("Adjusting balance...")
    adjust_balance()

    print("Climbing front legs...")
    front_legs_climb()

    print("Moving body forward...")
    move_body_forward()

    print("Climbing middle legs...")
    middle_legs_climb()

    print("Final forward movement...")
    final_body_forward()

    print("Climbing rear legs...")
    rear_legs_climb()


# Run the climbing routine
climb_stair()
