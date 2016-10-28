import xbox
import time

REFRESH_TIME = 30
    
joy = xbox.Joystick(REFRESH_TIME+10)     # Just to make sure that the Joystick is always updated when it loops.
refresh_seconds = 1 / REFRESH_TIME
last_run = time.time()

# Loop forever
try:
    while True:
        now = time.time()
        if last_run + refresh_seconds < time.time():
            last_run = now

            # Show connection status
            if joy.connected():
                print("Connected   ")
            else:
                print("Disconnected")

            # Left analog stick
            print("Lx,Ly ",joy.leftX(),joy.leftY())


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

    # Close out when done
except KeyboardInterrupt:
    joy.close()
