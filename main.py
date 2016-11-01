import xbox
import time

from math import atan, sqrt, degrees

REFRESH_TIME = 1
    
joy = xbox.Joystick(REFRESH_TIME+10)     # Just to make sure that the Joystick is always updated when it loops.
refresh_seconds = 1 / REFRESH_TIME
last_run = time.time()

class dataPacket:
    def __init__(self):
        self.rightX, self.rightY = 0, 0
        self.rightXPos, self.rightYPos = 0, 0

    def set_rightX(self, rightX):
        self.rightXPos = 1 if rightX > 0 else 0
        self.rightX = abs(int(rightX * 255))

    def set_rightY(self, rightY):
        self.rightYPos = 1 if rightY > 0 else 0
        self.rightY = abs(int(rightY * 255))

    def set_right_trigger(self, right_trigger):
        self.right_trigger = abs(int(right_trigger * 255))

    def set_left_trigger(self, left_trigger):
        self.left_trigger = abs(int(left_trigger * 255))

    def set_left_analogue(self, X, Y):
        if X == 0:
            self.left_direction, self.left_magnitude, self.left_direction_pos = 0, 0, 0
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
                        self.left_direction_pos = 1
                    else:
                        self.left_direction = abs(int(-90 - 90 - self.left_direction))
                        self.left_direction_pos = 0
                else:
                    if self.left_direction > 0:
                        self.left_direction = abs(int(self.left_direction))
                        self.left_direction_pos = 1
                    else:
                        self.left_direction = abs(int(self.left_direction))
                        self.left_direction_pos = 0

            else:
                self.left_direction, self.left_magnitude, self.left_direction_pos = 0, 0, 0

    def set_right_buttons(self, A, B, X, Y):
        self.x_button = X
        self.y_botton = Y
        self.a_button = A
        self.b_button = B

    def __str__(self):
        return "{} {} {} {} {} {} {} {} {} {} {} {} {}".format(   self.rightX,
                                                                  self.rightXPos,
                                                                  self.rightY,
                                                                  self.rightYPos,
                                                                  self.right_trigger,
                                                                  self.left_trigger,
                                                                  self.left_magnitude,
                                                                  self.left_direction,
                                                                  self.left_direction_pos,
                                                                  self.x_button,
                                                                  self.y_botton,
                                                                  self.a_button,
                                                                  self.b_button)

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
