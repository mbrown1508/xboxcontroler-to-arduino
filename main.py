import xbox
import time

REFRESH_TIME = 1
    
joy = xbox.Joystick(REFRESH_TIME+10)     # Just to make sure that the Joystick is always updated when it loops.
refresh_seconds = 1 / REFRESH_TIME
last_run = time.time()

class dataPacket:
    def __init__(self):
        self.leftX, self.leftY = 0, 0
        self.leftXPos, self.leftYPos = 0, 0

    def set_leftX(self, leftX):
        self.leftXPos = 1 if leftX > 0 else 0
        self.leftX = abs(int(leftX * 255))


    def set_leftY(self, leftY):
        self.leftYPos = 1 if leftY > 0 else 0
        self.leftY = abs(round(leftY * 255))

    def __str__(self):
        return "{} {} {} {}".format(self.leftX, self.leftY, self.leftXPos, self.leftYPos)

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
                data_packet.set_leftX(joy.leftX())
                data_packet.set_leftY(joy.leftY())

                print(data_packet)

                # # Right trigger
                # print "Rtrg ",fmtFloat(joy.rightTrigger()),
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
