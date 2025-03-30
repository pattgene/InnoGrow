import sys
import sys, tty, termios
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
def getch():
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

sys.path.append("..")
from STservo_sdk import *                 # Uses STServo SDK library

# Default setting
BAUDRATE = 1000000         # STServo default baudrate : 1000000
DEVICENAME = '/dev/tty.usbmodem58750064291'    # Check which port is being used on your controller

# These values set the hard code position, only chage max value, keep minimum constant at zero 
STS_MINIMUM_POSITION_VALUE  = 0          # STServo will rotate between this value
STS_MAXIMUM_POSITION_VALUE  = 100


STS_MOVING_SPEED            = 2400        # STServo moving speed
STS_MOVING_ACC              = 50          # STServo moving acc

index = 0
sts_goal_position = [STS_MINIMUM_POSITION_VALUE, STS_MAXIMUM_POSITION_VALUE]         # Goal position
sts_x_position = []
sts_y_position = []

with open("centre_of_boxes.txt", 'r') as coordinates:
    for line in coordinates:
        line = line.strip()
        if line:
            split = line.split(',')
            if len(split) == 2:
                x_coord = split[0][1:]
                y_coord = split[1].split(')')[0]
                sts_x_position.append(x_coord)
                sts_y_position.append(y_coord)

print(sts_x_position)
print(sts_y_position)

# ~11.5 motor steps to rotate 1 degree 


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sts(portHandler)
    
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Write STServo goal position/moving speed/moving acc
    for sts_id in range(0, 7):

        #change sts_goal_position to change the input position for the motor to rotate 
        sts_comm_result, sts_error = packetHandler.RegWritePosEx(sts_id, sts_goal_position[index], STS_MOVING_SPEED, STS_MOVING_ACC)
        if sts_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(sts_comm_result))
        if sts_error != 0:
            print("%s" % packetHandler.getRxPacketError(sts_error))
    packetHandler.RegAction()                                                           # Tells the servo to execute move

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0

# Close port
portHandler.closePort()