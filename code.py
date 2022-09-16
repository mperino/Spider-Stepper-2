import time
import board
import digitalio
## Define PINS
## Steppers 1-4 are predefined, and all you need to do is enable or disable them
## by setting them True or False
## You can change pin assignments if using a board other than Pico 2040.
stepper1 = True
stepper2 = True
stepper3 = True
stepper4 = True
## Setup wiring for each stepper
if stepper1 == True:
    pin11 = digitalio.DigitalInOut(board.GP0)
    pin12 = digitalio.DigitalInOut(board.GP1)
    pin13 = digitalio.DigitalInOut(board.GP2)
    pin14 = digitalio.DigitalInOut(board.GP3)
    pin11.direction = digitalio.Direction.OUTPUT
    pin12.direction = digitalio.Direction.OUTPUT
    pin13.direction = digitalio.Direction.OUTPUT
    pin14.direction = digitalio.Direction.OUTPUT
if stepper2 == True:
    pin21 = digitalio.DigitalInOut(board.GP4)
    pin22 = digitalio.DigitalInOut(board.GP5)
    pin23 = digitalio.DigitalInOut(board.GP6)
    pin24 = digitalio.DigitalInOut(board.GP7)
    pin21.direction = digitalio.Direction.OUTPUT
    pin22.direction = digitalio.Direction.OUTPUT
    pin23.direction = digitalio.Direction.OUTPUT
    pin24.direction = digitalio.Direction.OUTPUT

if stepper3 == True:
    pin31 = digitalio.DigitalInOut(board.GP8)
    pin32 = digitalio.DigitalInOut(board.GP9)
    pin33 = digitalio.DigitalInOut(board.GP10)
    pin34 = digitalio.DigitalInOut(board.GP11)
    pin31.direction = digitalio.Direction.OUTPUT
    pin32.direction = digitalio.Direction.OUTPUT
    pin33.direction = digitalio.Direction.OUTPUT
    pin34.direction = digitalio.Direction.OUTPUT

if stepper4 == True:
    pin41 = digitalio.DigitalInOut(board.GP12)
    pin42 = digitalio.DigitalInOut(board.GP13)
    pin43 = digitalio.DigitalInOut(board.GP14)
    pin44 = digitalio.DigitalInOut(board.GP15)
    pin41.direction = digitalio.Direction.OUTPUT
    pin42.direction = digitalio.Direction.OUTPUT
    pin43.direction = digitalio.Direction.OUTPUT
    pin44.direction = digitalio.Direction.OUTPUT


#Define steps per rotation
stepsperrot = 2048

#Define forward and backwards RPM (max is less than 20)
forwardRPM=8
backwardsRPM=10
#Define how many steps. or use rotations (stepsperrot * #) to lower/raise at start and end
lowersteps = stepsperrot * 1
#define how many steps to cycle up and down after initial lower the "twitching"
twitchsteps = 30

#define how long to pause at end before re-starting
sleeptime = 5

#===============================================================================================
# Functions to translate steps into co-ordinated rotation.
# This is pure bit-banging with time sleeping to get RPM's
# ==============================================================================================

def statefromsteppin(pin, step):
    #   step 1 2 3 4
    # pin 1  1 1 0 0
    # pin 2  0 1 1 0
    # pin 3  0 0 1 1
    # pin 4  1 0 0 1
    #
    Offset = [1, 0, 3, 2]
    Timing = [0, 1, 1, 0]
    TPOS = ((step - 1) % 4 + Offset[pin - 1]) % 4
    if Timing[TPOS] == 1:
        return True
    else:
        return False

def rotatestepsatrpm(steppernum, steps, rpm):
    if steps >= 1:
        for i in range(1, steps + 1):
            firepins(steppernum,i)
            time.sleep(60 / (rpm * stepsperrot))
    if steps <= 1:
        for i in range(-1, steps - 1, -1):
            firepins(steppernum, i)
            time.sleep(60 / (rpm * stepsperrot))

def firepins(steppernum, nextstep):
#    print("Step:{}".format(nextstep))
    if steppernum == 1 and stepper1 == True:
        pin11.value = statefromsteppin(1, nextstep)
        pin12.value = statefromsteppin(2, nextstep)
        pin13.value = statefromsteppin(3, nextstep)
        pin14.value = statefromsteppin(4, nextstep)
    elif steppernum == 2 and stepper2 == True:
        pin21.value = statefromsteppin(1, nextstep)
        pin22.value = statefromsteppin(2, nextstep)
        pin23.value = statefromsteppin(3, nextstep)
        pin24.value = statefromsteppin(4, nextstep)
    elif steppernum == 3 and stepper3 == True:
        pin31.value = statefromsteppin(1, nextstep)
        pin32.value = statefromsteppin(2, nextstep)
        pin33.value = statefromsteppin(3, nextstep)
        pin34.value = statefromsteppin(4, nextstep)
    elif steppernum == 4 and stepper4 == True:
        pin41.value = statefromsteppin(1, nextstep)
        pin42.value = statefromsteppin(2, nextstep)
        pin43.value = statefromsteppin(3, nextstep)
        pin44.value = statefromsteppin(4, nextstep)
    else:
        print("no valid stepper number or stepper is not enabled.")

def stopstepper(steppernum):
    if steppernum == 1 and stepper1 == True:
        pin11.value = statefromsteppin(1, False)
        pin12.value = statefromsteppin(2, False)
        pin13.value = statefromsteppin(3, False)
        pin14.value = statefromsteppin(4, False)
    elif steppernum == 2 and stepper2 == True:
        pin21.value = statefromsteppin(1, False)
        pin22.value = statefromsteppin(2, False)
        pin23.value = statefromsteppin(3, False)
        pin24.value = statefromsteppin(4, False)
    elif steppernum == 3 and stepper3 == True:
        pin31.value = statefromsteppin(1, False)
        pin32.value = statefromsteppin(2, False)
        pin33.value = statefromsteppin(3, False)
        pin34.value = statefromsteppin(4, False)
    elif steppernum == 4 and stepper4 == True:
        pin41.value = statefromsteppin(1, False)
        pin42.value = statefromsteppin(2, False)
        pin43.value = statefromsteppin(3, False)
        pin44.value = statefromsteppin(4, False)
    else:
        print("no valid stepper number or stepper is not enabled.")

# Lower each spider one at a time
for i in range(1,5):
    print(i)
    rotatestepsatrpm(i, lowersteps, forwardRPM)
    stopstepper(i)


