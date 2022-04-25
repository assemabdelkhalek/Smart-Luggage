import time
#from SabertoothDriverSimple import SerialMotorControl
from SabertoothDriverSimple import SerialMotorControl
#import the GPIO library
import RPi.GPIO as GPIO
#define the USB port for the Raspberry Pi
motors = SerialMotorControl('/dev/ttyUSB0')
GPIO.setmode(GPIO.BOARD) ##
GPIO.setwarnings(False) ##
# Define GPIO for ultrasonic central
GPIO_TRIGGER_CENTRAL = 16
GPIO_ECHO_CENTRAL = 18
GPIO.setup(GPIO_TRIGGER_CENTRAL, GPIO.OUT)  # Trigger > Out
GPIO.setup(GPIO_ECHO_CENTRAL, GPIO.IN)      # Echo < In

# Define GPIO for ultrasonic Right
GPIO_TRIGGER_RIGHT = 33
GPIO_ECHO_RIGHT = 35
GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)  # Trigger > Out
GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)      # Echo < In

# Define GPIO for ultrasonic Left
GPIO_TRIGGER_LEFT = 38
GPIO_ECHO_LEFT = 40
GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)  # Trigger > Out
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)      # Echo < In

# the back sensor is disbaled until we need it.
# Define GPIO for ultrasonic Back
# GPIO_TRIGGER_BACK = 29
# GPIO_ECHO_BACK = 31
# GPIO.setup(GPIO_TRIGGER_BACK, GPIO.OUT)  # Trigger > Out
# GPIO.setup(GPIO_ECHO_BACK, GPIO.IN)      # Echo < In

# Detect front obstacle
def frontobstacle():

    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER_CENTRAL, False)
    # Allow module to settle
    time.sleep(0.2)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER_CENTRAL, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_CENTRAL, False)
    # start measuring the time ECHO is HIGH
    start = time.time()
    while GPIO.input(GPIO_ECHO_CENTRAL) == 0:
        start = time.time()
    while GPIO.input(GPIO_ECHO_CENTRAL) == 1:
        # record when ECHO is LOW
        stop = time.time()
    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # Multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000 / 2  # distance of both directions so divide by 2
    print("Front Distance : %.1f" % distance)
    return distance

def rightobstacle():
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER_RIGHT, False)
    # Allow module to settle
    time.sleep(0.2)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER_RIGHT, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_RIGHT, False)
    # start measuring the time ECHO is HIGH
    start = time.time()
    while GPIO.input(GPIO_ECHO_RIGHT) == 0:
        start = time.time()
    while GPIO.input(GPIO_ECHO_RIGHT) == 1:
        stop = time.time()
        # record when ECHO is LOW
    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # Multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000 / 2  # Distance of both directions so divide by 2
    print("Right Distance : %.1f" % distance)
    return distance

def leftobstacle():
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER_LEFT, False)
    # Allow module to settle
    time.sleep(0.2)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER_LEFT, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_LEFT, False)
    # start measuring the time ECHO is HIGH
    start = time.time()
    while GPIO.input(GPIO_ECHO_LEFT) == 0:
        start = time.time()
    while GPIO.input(GPIO_ECHO_LEFT) == 1:
        # record when ECHO is LOW
        stop = time.time()
    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # Multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000 / 2  # Distance of both directions so divide by 2
    print("Left Distance : %.1f" % distance)
    return distance
# the back obstacle currently is disabled
def backobstacle():
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER_BACK, False)
    # Allow module to settle
    time.sleep(0.2)
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER_BACK, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_BACK, False)
    # start measuring the time ECHO is HIGH
    start = time.time()
    while GPIO.input(GPIO_ECHO_BACK) == 0:
        start = time.time()
    while GPIO.input(GPIO_ECHO_BACK) == 1:
        # record when ECHO is LOW
        stop = time.time()
    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # Multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000 / 2  # Distance of both directions so divide by 2
    print("Back Distance : %.1f" % distance)
    return distance

# The algorithm in this function follows the flowchart provided in the report
# Avoid obstacles and drive forward
def obstacleavoiddrive():
    motors.drive_forward(25)
    start = time.time()
    # Drive 5 minutes - just for testing
    # instead of while True:
    while start > time.time() - 300:  # 300 = 60 seconds * 5
        if frontobstacle() < 50: # if detected fron obstacle < 50cm
            motors.stop() #stop for 2 seconds
            time.sleep(2)
            while leftobstacle() < 50: #check is an obstacle is detected on the left
                motors.stop() #if a left obstacle is detected, stop until clear
                time.sleep(2) #if clear, continue
                
            motors.drive_left(100) #turn left 90 degress
            time.sleep(3)
            motors.drive_forward(25) # move forward
            time.sleep(2)
            while rightobstacle() < 50: #check is an obstacle is detected on the right
                motors.stop() #if a right obstacle is detected, stop until clear
                time.sleep(2) #if clear, continue
                
            motors.drive_right(100) #turn right 90 degress
            time.sleep(3)
            motors.drive_forward(25) # move forward
            time.sleep(2)
            while rightobstacle() < 50: #check is an obstacle is detected on the right
                motors.stop() #if a right obstacle is detected, stop until clear
                time.sleep(2) #if clear, continue
                
            motors.drive_right(100) #turn right 90 degress
            time.sleep(3)
            motors.drive_forward(25) # move forward
            time.sleep(2)
            while leftobstacle() < 50: #check is an obstacle is detected on the left
                motors.stop() #if a left obstacle is detected, stop until clear
                time.sleep(2) #if clear, continue
                
            motors.drive_left(100) #turn left 90 degress
            time.sleep(3)
            motors.drive_forward(25) # move forward
            time.sleep(2)
            
            motors.stop() #stop after passing the obstacle for 5 sec
            time.sleep(5) # Just for safety
 
    # Clear GPIOs, it will clear GPIOs for triger ultrasonic sensors       
    motors.stop()
    cleargpios()
#  clear GPIOs function
def cleargpios():
    print("clearing GPIO")
    GPIO.output(16, False)
    GPIO.output(33, False)
    GPIO.output(38, False)
    #GPIO.output(29, False)
    print("All GPIOs CLEARED")
# The main function to run the program
def main():
    # First clear GPIOs
    motors.stop()
    cleargpios()
    print("start driving: ")
    # Start obstacle avoid driving
    obstacleavoiddrive()
# run the main function
if __name__ == "__main__":
    main()
