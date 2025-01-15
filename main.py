from adafruit_servokit import ServoKit

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
    if i == 2:
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


# Home positions
# home_pos_RL11, home_pos_RL12, home_pos_RL13 = 80, 85, 110
# home_pos_RL21, home_pos_RL22, home_pos_RL23 = 80, 80, 90
# home_pos_RL31, home_pos_RL32, home_pos_RL33 = 70, 85, 85

# home_pos_LL11, home_pos_LL12, home_pos_LL13 = 65, 70, 85
# home_pos_LL21, home_pos_LL22, home_pos_LL23 = 75, 85, 90
# home_pos_LL31, home_pos_LL32, home_pos_LL33 = 65, 80, 85
home_pos_RL1 = [80, 85, 110]
home_pos_RL2 = [80, 80, 90]
home_pos_RL3 = [70, 85, 85]

home_pos_LL1 = [65, 70, 85]
home_pos_LL2 = [75, 85, 90]
home_pos_LL3 = [65, 80, 85]


# Function to set the standing position
def stand_pos():
    # Right leg

    right_leg_1(1, home_pos_RL1[0])  # R1
    right_leg_1(2, home_pos_RL1[1])
    right_leg_1(3, home_pos_RL1[2])

    right_leg_2(1, home_pos_RL2[0])  # R2
    right_leg_2(2, home_pos_RL2[1])
    right_leg_2(3, home_pos_RL2[2])

    right_leg_3(1, home_pos_RL3[0])  # R3
    right_leg_3(2, home_pos_RL3[1])
    right_leg_3(3, home_pos_RL3[2])

    # Left leg
    left_leg_1(1, home_pos_LL1[0])  # L1
    left_leg_1(2, home_pos_LL1[1])
    left_leg_1(3, home_pos_LL1[2])

    left_leg_2(1, home_pos_LL2[0])  # L2
    left_leg_2(2, home_pos_LL2[1])
    left_leg_2(3, home_pos_LL2[2])

    left_leg_3(1, home_pos_LL3[0])  # L3
    left_leg_3(2, home_pos_LL3[1])
    left_leg_3(3, home_pos_LL3[2])


# Main execution
if __name__ == "__main__":
    # Example: Set the standing position
    while True:
        stand_pos()
