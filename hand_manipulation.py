import time
from time import sleep
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


factory = PiGPIOFactory()

servo1 = Servo(8, min_pulse_width = 1.4/1000, max_pulse_width = 1.6/1000, pin_factory = factory)
servo2 = Servo(25, min_pulse_width = 1.37/1000, max_pulse_width = 1.6/1000, pin_factory = factory)
servo3 = Servo(24, min_pulse_width = 1.4/1000, max_pulse_width = 1.55/1000, pin_factory = factory)
servo4 = Servo(23, min_pulse_width = 1.4/1000, max_pulse_width = 1.6/1000, pin_factory = factory)
servo5 = Servo(7, min_pulse_width = 1.4/1000, max_pulse_width = 1.6/1000, pin_factory = factory)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)
r2 = 22
GPIO.setup(4, GPIO.OUT)
r5 = 4
GPIO.setup(17, GPIO.OUT)
r4 = 17
GPIO.setup(27, GPIO.OUT)
r3 = 27
GPIO.setup(6, GPIO.OUT)
r1 = 6

all_reachable_notes = ["C2", "D2", "E2", "F2", "G2", "A2", "B2", "C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4", "B4"]

note_to_position = {
    "C2": 0,
    "D2": 0,
    "E2": 0,
    "F2": 1.3,
    "G2": 4,
    "A2": 6.7,
    "B2": 9.5,
    "C3": 10.9,
    "D3": 13.7,
    "E3": 16.4,
    "F3": 17.9,
    "G3": 20.6,
    "A3": 23.2,
    "B3": 25.9,
    "C4": 27.4,
    "D4": 30.1,
    "E4": 33,
    "F4": 34.4,
    "G4": 37.1,
    "A4": 39.7,
    "B4": 42.4
}

kit = MotorKit(address=0x6f, i2c=board.I2C(), steppers_microsteps=16)
distance_between_fingers = 2.5 #cm
stepper_speed = 215 #steps/s

def initialize():
    # servo1.mid()
    GPIO.output(r1, 0)
    sleep(1)
    servo2.min()
    GPIO.output(r2, 0)
    sleep(1)
    # servo3.max()
    GPIO.output(r3, 0)
    sleep(1)
    # servo4.max()
    GPIO.output(r4, 0)
    sleep(1)
    # servo5.max()  # this is the straight pos
    GPIO.output(r5, 0)
    sleep(1)


def move_hand_to_position(middle_finger_note, next_note, next_finger):
    next_middle_finger_position = (next_finger-3)*2.5 + note_to_position[next_note] #use the middle finger as reference
    next_middle_finger_note = getMiddleFingerNote(next_note, next_finger)
    distance = next_middle_finger_position - note_to_position[middle_finger_note]
    distance_rev = distance * 50 / 1.4

    for i in range(abs(int(distance_rev))):
        if distance_rev < 0:
            kit.stepper2.onestep(direction = stepper.BACKWARD, style=stepper.DOUBLE)
            time.sleep(0.00008)
        else:
            kit.stepper2.onestep(direction = stepper.FORWARD, style=stepper.DOUBLE)
            time.sleep(0.00008)

    kit.stepper2.release()
    return next_middle_finger_note


def play_note0 (next_duration, next_finger):
    #calculate the duration to be spent traveling from one position to another
    next_duration = next_duration/10000
    #actuate the respective servos for the respective duration
    print("Playing note0")
    print("Next duration: " + str(next_duration))
    if next_finger == 1:
        GPIO.output(r1, 1)
        sleep(next_duration)
        GPIO.output(r1, 0)

    elif next_finger == 2:
        GPIO.output(r2, 1)
        sleep(next_duration)
        GPIO.output(r2, 0)

    elif next_finger == 3:
        GPIO.output(r3, 1)
        sleep(next_duration)
        GPIO.output(r3, 0)

    elif next_finger == 4:
        GPIO.output(r4, 1)
        sleep(next_duration)
        GPIO.output(r4, 0)

    elif next_finger == 5:
        GPIO.output(r5, 1)
        sleep(next_duration)
        GPIO.output(r5, 0)


def play_note1(middle_finger_note, next_next_note, next_duration, next_finger, next_next_finger):
    # calculate the duration to be spent traveling from one position to another
    next_next_middle_finger_position = (next_next_finger - 3) * 2.5 + note_to_position[next_next_note]  # use the middle finger as reference
    distance = abs(next_next_middle_finger_position - note_to_position[middle_finger_note])
    distance_steps = distance * 50 / 1.4

    next_duration = (next_duration/10000) - distance_steps/stepper_speed#to make it in seconds

    # actuate the respective servos for the respective duration
    print("Playing note1")
    print("Next duration: " + str(next_duration))
    if next_finger == 1:
        GPIO.output(r1, 1)
        sleep(next_duration)
        GPIO.output(r1, 0)

    elif next_finger == 2:
        GPIO.output(r2, 1)
        sleep(next_duration)
        GPIO.output(r2, 0)

    elif next_finger == 3:
        GPIO.output(r3, 1)
        sleep(next_duration)
        GPIO.output(r3, 0)

    elif next_finger == 4:
        GPIO.output(r4, 1)
        sleep(next_duration)
        GPIO.output(r4, 0)

    elif next_finger == 5:
        GPIO.output(r5, 1)
        sleep(next_duration)
        GPIO.output(r5, 0)

def getMiddleFingerNote(next_note, next_finger):
    next_note_index = all_reachable_notes.index(next_note)
    middle_finger_index = next_note_index + (next_finger-3)
    return all_reachable_notes[middle_finger_index]

def subtract_durations(phaser_note_duration, user_note_duration):
    remaining_duration = abs(user_note_duration - phaser_note_duration)
    if remaining_duration > 0:
        return False, remaining_duration
    else:
        return True, remaining_duration