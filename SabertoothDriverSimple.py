# Library for Sabertooth Simplified Serial
# Test w/ RPi4B+ -> USB to TTL 5V Cable -> Sabertooth 2X25
# USB to TTL Cable Hookup to Sabertooth: GND -> 0V, TX -> S1
# DIP Config (9600 Buad): 1UP - 2DOWN - 3 UP - 4DOWN - 5UP - 6UP

import serial
import time

class SerialMotorControl:
    serialPort = '/dev/ttyUSB0'
    # Setup usb serial communication. If you have multiple usb serial devices, this may need to be changed.
    # This cannot detect which one is the SaberTooth
    ard = 0

    def __init__(self, port):
        # define the raspberry pi port and baud rate
        self.serialPort = port
        self.ard = serial.Serial(port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1)
        self.stop()

    @staticmethod
    # this function is to constraint the min and max byte numbers
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))
    # this function recieves the speed of the motos in %
    # and the motor number and outputs the corresponding byte number
    def get_byte_of_motor(self, motor, power):
        power = self.constrain(power, -127, 127)
        magnitude = abs(power) >> 1
        command = 0
        if (motor == 0): # the right side motors
            if power < 0: # < 0 means reverse
                command = 63 - magnitude
            else: #forward
                command = 64 + magnitude
        else:
            if motor == 1: # the left side motors
                if power < 0: # < 0 means reverse 
                    command = 191 - magnitude
                else: #forward
                    command = 192 + magnitude
        # constrain the commands between 1 and 254
        command = self.constrain(command, 1, 254)
        #print(command)
        return command

    # this function 
    # send a command to motors (0 = motor 1, 1 = motor 2, -100 < power < 100)
    def motor_raw_simple(self, motor, power):
        data = self.get_byte_of_motor(motor, power)
        print("data = ", data)
        self.motor_raw(bytes([data]))
        
    # sent the byte data to the motor driver
    def motor_raw(self, data):
        self.ard.write(data)
    # drive both mototrs at the same time with different powers on each side
    def drive_both(self, left_power, right_power):
        self.motor_raw_simple(0, left_power)
        self.motor_raw_simple(1, right_power)
    #drive both with inputting the same power
    def drive(self, power):
        self.drive_both(power, power)
    # drive both sides forward at the same speed
    def drive_forward(self, power):
        self.drive(power)
        #print("Forward")
    # drive both sides backward at the same speed
    def drive_backward(self, power):
        self.drive(-power)
        print("Backward")
    # drive left: right side in reverse & left side forward at the same speed
    def drive_left(self, power):
        self.drive_both(-power, power)
        print("Left")
        
    # drive right: right side forward & left side in reverse at the same speed
    def drive_right(self, power):
        self.drive_both(power, -power)
        print("Right")
    # stop both motors
    def stop(self):
        self.drive(0)
        print("Stop")
# define the USB port connecting the Sabertooth to Raspberry Pi
motors = SerialMotorControl('/dev/ttyUSB0')
