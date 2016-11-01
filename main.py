import xbox
import time

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

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.rightX,
                                          self.rightY,
                                          self.right_trigger,
                                          self.left_trigger,
                                          self.rightXPos,
                                          self.rightYPos)

data_packet = dataPacket()

# Loop forever
try:
    while True:
        now = time.time()
        if last_run + refresh_seconds < time.time():
            last_run = now

            # Show connection status
            if joy.connected():

                # Left analog stick
                data_packet.set_rightX(joy.rightX())
                data_packet.set_rightY(joy.rightY())
                data_packet.set_right_trigger(joy.rightTrigger())
                data_packet.set_left_trigger(joy.rightTrigger())

                print(data_packet)

                # # Right trigger
                # print "Rtrg ",fmtFloat(),
                # # A/B/X/Y buttons
                # print "Buttons ",
                # if joy.A():
                #     print "A",
                # else:
                #     print " ",
                # if joy.B():
                #     print "B",
                # else:
                #     print " ",
                # if joy.X():
                #     print "X",
                # else:
                #     print " ",
                # if joy.Y():
                #     print "Y",
                # else:
                #     print " ",
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
