from adafruit_servokit import ServoKit
import time
import numpy as np

# Initialize ServoKit instances for two PCA9685 boards
board1 = ServoKit(channels=16, address=0x40)
board2 = ServoKit(channels=16, address=0x41)

# Servo pulse range
SERVOMIN = 125  # Minimum pulse length count
SERVOMAX = 575  # Maximum pulse length count


# Angle-to-pulse conversion function
def angle_to_pulse(angle):
    return int((SERVOMAX - SERVOMIN) * angle / 180 + SERVOMIN)


# Right leg functions
def right_leg_1(i, angle):  # Right Leg 1 --> 0, 1, 2
    if i == 2 or i == 1:
        board1.servo[i + 5].angle = angle
    else:
        board2.servo[i - 1].angle = angle


def right_leg_2(i, angle):  # Right Leg 2 --> 3, 4, 5
    board1.servo[i + 2].angle = angle


def right_leg_3(i, angle):  # Right Leg 3 --> 13, 14, 15
    board1.servo[i + 12].angle = angle


# Left leg functions
def left_leg_1(i, angle):  # Left Leg 1 --> 13, 14, 15
    board2.servo[i + 12].angle = angle


def left_leg_2(i, angle):  # Left Leg 2 --> 3, 4, 5
    board2.servo[i + 2].angle = angle


def left_leg_3(i, angle):  # Left Leg 3 --> 6, 7, 2
    if i == 3:
        board2.servo[i - 1].angle = angle
    else:
        board2.servo[i + 5].angle = angle


# home_pos_RL1 = [80, 85, 110]
# home_pos_RL2 = [80, 80, 90]
# home_pos_RL3 = [70, 85, 85]

# home_pos_LL1 = [65, 70, 85]
# home_pos_LL2 = [75, 85, 90]
# home_pos_LL3 = [65, 80, 85]

# def stand_pos():
#     # Right leg

#     right_leg_1(1, home_pos_RL1[0])  # R1
#     right_leg_1(2, home_pos_RL1[1])
#     right_leg_1(3, home_pos_RL1[2])

#     right_leg_2(1, home_pos_RL2[0])  # R2
#     right_leg_2(2, home_pos_RL2[1])
#     right_leg_2(3, home_pos_RL2[2])

#     right_leg_3(1, home_pos_RL3[0])  # R3
#     right_leg_3(2, home_pos_RL3[1])
#     right_leg_3(3, home_pos_RL3[2])

#     # Left leg
#     left_leg_1(1, home_pos_LL1[0])  # L1
#     left_leg_1(2, home_pos_LL1[1])
#     left_leg_1(3, home_pos_LL1[2])

#     left_leg_2(1, home_pos_LL2[0])  # L2
#     left_leg_2(2, home_pos_LL2[1])
#     left_leg_2(3, home_pos_LL2[2])

#     left_leg_3(1, home_pos_LL3[0])  # L3
#     left_leg_3(2, home_pos_LL3[1])
#     left_leg_3(3, home_pos_LL3[2])


rl_pins = [[6, 7, 2], [3, 4, 5], [13, 14, 15]]
ll_pins = [[13, 14, 15], [3, 4, 5], [6, 7, 2]]

up_pos_RL = [[80, 85, 110], [80, 80, 90], [70, 85, 85]]
up_pos_LL = [[65, 70, 85], [75, 85, 90], [65, 80, 85]]


def leg_position(rl_pins, ll_pins, Rl_angles, Ll_angles):
    for i in range(3):
        right_leg_1(rl_pins[0][i], Rl_angles[0][i])
        right_leg_2(rl_pins[1][i], Rl_angles[1][i])
        right_leg_3(rl_pins[2][i], Rl_angles[2][i])

        left_leg_1(ll_pins[0][i], Ll_angles[0][i])
        left_leg_2(ll_pins[1][i], Ll_angles[1][i])
        left_leg_3(ll_pins[2][i], Ll_angles[2][i])


# Hexapod dimensions (in mm)
COXA_LENGTH = 59  # Distance from body to femur joint
FEMUR_LENGTH = 71  # Upper leg length
TIBIA_LENGTH = 166  # Lower leg length


# Inverse kinematics function
def inverse_kinematics(x, y, z):
    h = np.sqrt(np.square(x) + np.square(y))
    h = max(h, 0.1)
    l = np.sqrt(np.square(h) + np.square(z))

    coxa_angle = np.degrees(np.arctan2(y, x))

    femur_angle = 90 - np.degrees(
        np.arctan2(z, h)
        + np.arccos(np.square(FEMUR_LENGTH) + np.square(l) - np.square(TIBIA_LENGTH))
        / (2 * FEMUR_LENGTH * l)
    )

    tibia_angle = np.degrees(
        np.arccos(
            (np.square(FEMUR_LENGTH) + np.square(TIBIA_LENGTH) - np.square(l))
            / (2 * FEMUR_LENGTH * TIBIA_LENGTH)
        )
    )

    return coxa_angle, femur_angle, tibia_angle


# Main execution
if __name__ == "__main__":
    # Example: Set the standing position
    # while True:
    leg_position(rl_pins, ll_pins, up_pos_RL, up_pos_LL)
    time.sleep(10)
    # Standing position
    delta = 30
    stand_pos_rl = [
        [80 - delta, 85 - delta, 110 + delta],
        [80 + delta, 80 + delta, 90 - delta],
        [70 - delta, 85 + delta, 85 - delta],
    ]
    stand_pos_ll = [
        [65 + delta, 70 + delta, 85 - delta],
        [75 - delta, 85 - delta, 90 + delta],
        [65 + delta, 80 - delta, 85 + delta],
    ]

    leg_position(rl_pins, ll_pins, stand_pos_rl, stand_pos_ll)
    time.sleep(10)

    # forward
