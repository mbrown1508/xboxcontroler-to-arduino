import xbox
import time

from math import atan, sqrt, degrees

REFRESH_TIME = 1
    
joy = xbox.Joystick(REFRESH_TIME+10)     # Just to make sure that the Joystick is always updated when it loops.
refresh_seconds = 1 / REFRESH_TIME
last_run = time.time()

import ctypes
c_uint8 = ctypes.c_uint8

class Flags_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                ("rightXPos",     c_uint8, 1 ),  # asByte & 1
                ("rightYPos", c_uint8, 1 ),  # asByte & 2
                ("left_direction_pos",    c_uint8, 1 ),  # asByte & 4
                ("x_button",       c_uint8, 1 ),  # asByte & 8
                ("y_button",       c_uint8, 1 ),  # asByte & 16
                ("a_button",       c_uint8, 1 ),  # asByte & 32
                ("b_button",       c_uint8, 1 ),  # asByte & 64
                ("not_implemented",       c_uint8, 1 ),  # asByte & 128
                ]

class Flags( ctypes.Union ):
    _anonymous_ = ("bit",)
    _fields_ = [
                ("bit",    Flags_bits ),
                ("asByte", c_uint8    )
                ]

class dataPacket:
    def __init__(self):
        self.flags = Flags()
        self.flags.asByte = 0x00

    def set_rightX(self, rightX):
        self.flags.rightXPos = 1 if rightX > 0 else 0
        self.rightX = abs(int(rightX * 255))

    def set_rightY(self, rightY):
        self.flags.rightYPos = 1 if rightY > 0 else 0
        self.rightY = abs(int(rightY * 255))

    def set_right_trigger(self, right_trigger):
        self.right_trigger = abs(int(right_trigger * 255))

    def set_left_trigger(self, left_trigger):
        self.left_trigger = abs(int(left_trigger * 255))

    def set_left_analogue(self, X, Y):
        if X == 0:
            self.left_direction, self.left_magnitude, self.flags.left_direction_pos = 0, 0, 0
        else:
            self.left_magnitude = sqrt(X*X + Y*Y) * 255
            if self.left_magnitude > 25:
                self.left_direction = degrees(atan(Y/X))

                # Clean up magnitude
                if self.left_magnitude > 255:
                    self.left_magnitude = 255
                self.left_magnitude = int(self.left_magnitude)

                # Clean up direction
                if X < 0:
                    self.left_direction *= -1
                    if self.left_direction > 0:
                        self.left_direction = abs(int(90 + 90 - self.left_direction))
                        self.flags.left_direction_pos = 1
                    else:
                        self.left_direction = abs(int(-90 - 90 - self.left_direction))
                        self.flags.left_direction_pos = 0
                else:
                    if self.left_direction > 0:
                        self.left_direction = abs(int(self.left_direction))
                        self.flags.left_direction_pos = 1
                    else:
                        self.left_direction = abs(int(self.left_direction))
                        self.flags.left_direction_pos = 0

            else:
                self.left_direction, self.left_magnitude, self.flags.left_direction_pos = 0, 0, 0

    def set_right_buttons(self, A, B, X, Y):
        self.flags.x_button = X
        self.flags.y_button = Y
        self.flags.a_button = A
        self.flags.b_button = B

    def return_byte_array(self):
        return bytearray([
            self.rightX,
            self.rightY,
            self.right_trigger,
            self.left_trigger,
            self.left_magnitude,
            self.left_direction,
            self.flags.asByte
        ])

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {} {} {} {}\n{}".format(self.rightX,
                                                                  self.flags.rightXPos,
                                                                  self.rightY,
                                                                  self.flags.rightYPos,
                                                                  self.right_trigger,
                                                                  self.left_trigger,
                                                                  self.left_magnitude,
                                                                  self.left_direction,
                                                                  self.flags.left_direction_pos,
                                                                  self.flags.x_button,
                                                                  self.flags.y_button,
                                                                  self.flags.a_button,
                                                                  self.flags.b_button,
                                                                  str(self.return_byte_array()))


data_packet = dataPacket()


# Loop forever
try:
    while True:
        now = time.time()
        if last_run + refresh_seconds < time.time():
            last_run = now

            # Show connection status
            if joy.connected():

                # Right analog stick
                data_packet.set_rightX(joy.rightX())
                data_packet.set_rightY(joy.rightY())

                # Left analog stick
                data_packet.set_left_analogue(joy.leftX(deadzone=0), joy.leftY(deadzone=0))

                # Triggers
                data_packet.set_right_trigger(joy.rightTrigger())
                data_packet.set_left_trigger(joy.leftTrigger())

                # Set Right buttons
                data_packet.set_right_buttons(joy.A(), joy.B(), joy.X(), joy.Y())

                print(data_packet)

                # # Dpad U/D/L/R
                # print "Dpad ",
                # if joy.dpadUp():
                #     print "U",
                # else:
                #     print " ",
                # if joy.dpadDown():
                #     print "D",
                # else:
                #     print " ",
                # if joy.dpadLeft():
                #     print "L",
                # else:
                #     print " ",
                # if joy.dpadRight():
                #     print "R",
                # else:
                #     print " ",
            else:
                print("Disconnected")

    # Close out when done
except KeyboardInterrupt:
    joy.close()
