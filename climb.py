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


# # Step 4: Place middle legs on stair
# def middle_legs_climb():
#     lift_leg("right2", 90, 120, 120)
#     place_leg("right2", 110, 100, 50)

#     lift_leg("left2", 90, 120, 120)
#     place_leg("left2", 70, 100, 50)


# # Step 5: Move body forward again
# def final_body_forward():
#     lift_leg("right3", 90, 120, 120)
#     place_leg("right3", 90, 90, 90)

#     lift_leg("left3", 90, 120, 120)
#     place_leg("left3", 90, 90, 90)


# # Step 6: Place rear legs on stair
# def rear_legs_climb():
#     lift_leg("right3", 90, 120, 120)
#     place_leg("right3", 110, 100, 50)

#     lift_leg("left3", 90, 120, 120)
#     place_leg("left3", 70, 100, 50)


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
