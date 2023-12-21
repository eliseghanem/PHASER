import csv
import hand_manipulation as hm
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
import pitch_detection as pd

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
phaser_note_sequence = [] #we will populate this list with the contents of the csv
user_note_sequence = []

with open(r'/home/raspberrypi/Desktop/happybirthday_midi.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    for row in csv_reader:
        phaser_note_sequence.append(row)

with open(r'/home/raspberrypi/Desktop/happybirthday_midi_user.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    for row in csv_reader:
        user_note_sequence.append(row)


GPIO.setmode(GPIO.BCM)
kit = MotorKit(address=0x6f, i2c=board.I2C(), steppers_microsteps=16)

middle_finger_note = "E2"
#current_note_position = 0
next_note_position = 0
current_middle_finger_note = "E2"

#initialize the servos and the relays
hm.initialize()

user_index = 1

detect_new_pitch = True
remaining_duration = 0

for i in range(1, len(phaser_note_sequence)):

    next_note = phaser_note_sequence[i][2]
    next_duration = int(float((phaser_note_sequence[i][4])))
    next_finger = int(float((phaser_note_sequence[i][6])))
    note_index = all_reachable_notes.index(middle_finger_note) #note index is the current middle finger note index
    current_range = [all_reachable_notes[note_index - 2], all_reachable_notes[note_index - 1], all_reachable_notes[note_index], all_reachable_notes[note_index + 1], all_reachable_notes[note_index + 2]]          #populate the list with the notes directly accessible by the hand without need to move
    next_next_note = phaser_note_sequence[i + 1][2]
    next_next_finger = int(phaser_note_sequence[i + 1][6])

    print("Next note: " + next_note)
    print("Middle Finger note:" + middle_finger_note)
    print(current_range)

    next_user_note = user_note_sequence[user_index][2]
    next_user_duration = int(float((user_note_sequence[user_index][4])))


    if next_note in current_range:
        if detect_new_pitch:
            user_index += 1
            detected_user_note = pd.detect_pitch(next_user_note)
            remaining_duration = next_user_duration
            if detected_user_note:
                if next_next_note not in current_range:
                    hm.play_note1(middle_finger_note, next_next_note, next_duration, next_finger, next_next_finger)
                    detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
                else:
                    hm.play_note0(next_duration, next_finger)
                    detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
        else:
            if next_next_note not in current_range:
                hm.play_note1(middle_finger_note, next_next_note, next_duration, next_finger, next_next_finger)
                detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
            else:
                hm.play_note0(next_duration, next_finger)
                detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)

    else:
        middle_finger_note = hm.move_hand_to_position(middle_finger_note, next_note, next_finger)
        print("Hand in position")
        next_next_note = phaser_note_sequence[i + 1][2]
        if detect_new_pitch:
            user_index += 1
            detected_user_note = pd.detect_pitch(next_user_note)
            remaining_duration = next_duration
            if detected_user_note:
                if next_next_note not in current_range:
                    hm.play_note1(middle_finger_note, next_next_note, next_duration, next_finger, next_next_finger)
                    detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
                else:
                    hm.play_note0(next_duration, next_finger)
                    detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
        else:
            if next_next_note not in current_range:
                hm.play_note1(middle_finger_note, next_next_note, next_duration, next_finger, next_next_finger)
                detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
            else:
                hm.play_note0(next_duration, next_finger)
                detect_new_pitch, remaining_duration = hm.subtract_durations(next_duration, remaining_duration)
