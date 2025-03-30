import sys, termios
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

sys.path.append("..")
from STservo_sdk import*                 # Uses STServo SDK library

# Default setting
BAUDRATE                = 1000000         # STServo default baudrate : 1000000
DEVICENAME              = '/dev/tty.usbmodem58750064291'    # Check which port is being used on your controller
STS_MOVING_SPEED            = 2400        # STServo moving speed
STS_MOVING_ACC              = 50          # STServo moving acc

motor_1_positions = [0, 200, 500, 200]         # Hardcoded positions 
motor_2_positions = [0, 200, 500, 200]

portHandler = PortHandler(DEVICENAME)
packetHandler = sts(portHandler)
portHandler.openPort()
portHandler.setBaudRate(BAUDRATE)

for i in range(3): #number of times loop through 
    for j in range(2): #number of positions 
        #move motor 1 
        sts_comm_result, sts_error = packetHandler.RegWritePosEx(1, motor_1_positions[j], STS_MOVING_SPEED, STS_MOVING_ACC)
        sts_comm_result, sts_error = packetHandler.RegWritePosEx(2, motor_2_positions[j], STS_MOVING_SPEED, STS_MOVING_ACC)
        packetHandler.RegAction()

# Close port
portHandler.closePort()