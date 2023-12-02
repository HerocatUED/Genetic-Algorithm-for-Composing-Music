import numpy as np

pitch_map = {
    'c': 0, 
    '#c': 1, 
    'd': 2, 
    '#d': 3, 
    'e': 4, 
    'f': 5, 
    '#f': 6, 
    'g': 7, 
    '#g': 8, 
    'a': 9, 
    '#a': 10, 
    'b': 11, 
}

def notes2pitches(notes):
    pichtes = []
    for note in notes:
        if note == '0':
            pichtes.append('rest')
        elif note == '-':
            pichtes.append('hold')
        else:
            family = int(note[-1])
            level = pitch_map[note[:-1]]
            pichtes.append((family - 4) * 12 + level)
    return pichtes

def notes2codes(notes):
    codes = []
    for note in notes:
        if note == '0':
            codes.append(0)
        elif note == '-':
            codes.append(20)
        else:
            family = int(note[-1])
            level = pitch_map[note[:-1]]
            codes.append((family + 1) * 12 + level)
    return np.array(codes, dtype=np.int32)

def codes2piches(codes):
    pitches = []
    for code in codes.tolist():
        if code == 0:
            pitches.append('rest')
        elif code == 20:
            pitches.append('hold')
        else:
            pitches.append(code - 60)
    return pitches

def tone2shift(tone):
    family = int(tone[-1])
    level = pitch_map[tone[:-1].lower()]
    return (family - 4) * 12 + level
