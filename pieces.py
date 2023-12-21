# This code read the xml files for the selected pieces and provides the left and right hand measures as lists.
# The xml files for these pieces are the outputs of the pianoplayer algorithm, providing the optimal fingering sequence for playing.

import xml.etree.ElementTree as ET
import csv
import os

beginner = ['happy-birthday.xml', 'twinkle-twinkle-little-star.xml', 'mary-had-a-little-lamb.xml']
intermediate = ['ode-to-joy.xml', 'bella-ciao.xml', 'ma-fi-ward-byotlob-may.xml']

def save_to_csv_hand(hand_measures, piece_name):
    # CSV columns: Type (hand) - Note (step+octave as string) - Duration - Finger - Instruction
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, piece_name + '_hand.csv')
    header = ['Type', 'Note', 'Duration', 'Finger', 'Instruction']
    data_list = []

    for measure in hand_measures:
        for note in measure:
            data_list.append(['Hand', note['step'] + note['octave'],note['duration'],note['finger'], ''])


    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for row in data_list:
            csv_writer.writerow(row)

def save_to_csv_user(user_measures, piece_name):
    # CSV columns: Type (hand/user) - Note (step+octave as string) - Duration - Finger - Instruction
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, piece_name + '_user.csv')
    header = ['Type', 'Note', 'Duration', 'Finger', 'Instruction']

    data_list = []
    finger = ["thumb", "index", "middle finger", "ring finger", "pinky"]

    for measure in user_measures:
        for note in measure:
            if note['finger'] == None:
                instr = "Silence. Do not play any notes for " + str(note['duration']) + " seconds."
            else:
                instr = "Play note " + note['step'] + note['octave'] + " with your " + finger[int(note['finger'])-1] + " for " + str(note['duration']) + " seconds."
            data_list.append(['User', note['step'] + note['octave'],note['duration'],note['finger'],instr])


    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for row in data_list:
            csv_writer.writerow(row)


def parse_xml(piece):
    tree = ET.parse(piece)
    root = tree.getroot()
    data = {}

    for part_id in ["P1", "P2"]:
        part_data = []
        part = root.find(f".//part[@id='{part_id}']")
        if part is not None:
            for measure in part.findall(".//measure"):
                measure_data = []
                for note in measure.findall(".//note"):
                    rest = note.find("rest")
                    pitch = note.find("pitch")
                    step = pitch.find("step").text if pitch is not None and pitch.find("step") is not None else None
                    rotate = int(pitch.find("alter").text) if pitch is not None and pitch.find("alter") is not None else 0        # 1 -> right / -1 -> left / 0 -> no rotation
                    octave = pitch.find("octave").text if pitch is not None and pitch.find("octave") is not None else None
                    finger = note.find(".//notations/technical/fingering").text if note.find(".//notations/technical/fingering") is not None else None

                    if rest is not None:
                        step = 0; octave = 0; rotate = 0; finger = 0

                    duration_element = note.find("duration")
                    if duration_element is not None:
                        duration = int(duration_element.text)/10000
                    else:
                        duration = None

                    note_data = {
                        "step": step,
                        "octave": octave,
                        "duration": duration,
                        "finger": finger,
                        "rotate": rotate
                    }

                    measure_data.append(note_data)

                part_data.append(measure_data)

        data[part_id] = part_data

    return data


def process(level, piece_number):
    hand_measures = [] # left hand
    user_measures = [] # right hand

    if level == 'beginner':
        piece = beginner[piece_number-1]
    elif level == 'intermediate':
        piece = intermediate[piece_number-1]
    else: 
        return
    
    piece_name = piece[:-4]

    data = parse_xml(piece)
    hand_measures = data.get("P1", [])
    user_measures = data.get("P2", [])
    instructions = get_instructions(user_measures)
    return piece_name, hand_measures, user_measures, instructions


def get_instructions(user_measures):
    instructions = []; instructions_note = []
    finger = ["thumb", "index", "middle finger", "ring finger", "pinky"]
    for measure in user_measures:
        for note in measure:
            # If note[3] = finger = None -> rest
            if note['finger'] == None:
                instr = "Silence. Do not play any notes for " + str(note['duration']) + " seconds."
            else:
                instr = "Play note " + note['step'] + note['octave'] + " with your " + finger[int(note['finger'])-1] + " for " + str(note['duration']) + " seconds."
            instructions_note.append(instr)
        instructions.append(instructions_note)
        instructions_note = []
        instr = []
    return instructions
