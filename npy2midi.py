import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message
from midi import read_mid

# Example numpy array (representing the .npy data)
npy_data = np.array([
    [76,  0, 76,  0, 76,  0, 77, 76],
    [ 0,  0,  0,  0,  0, 76, 74, 72],
    [64,  0, 69,  0, 67,  0, 64, 67],
    [ 0,  0,  0,  0,  0,  0, 67, 69],
    [72,  0,  0,  0, 69,  0, 67,  0],
    [64,  0, 67, 64,  0,  0, 60, 62],
    [ 0,  0, 64,  0,  0,  0, 64,  0],
    [65, 64, 62, 65, 64,  0, 60,  0],
    [55,  0, 60,  0, 60,  0, 64,  0],
    [65,  0, 64,  0, 62,  0, 60, 62],
    [64,  0, 69,  0, 67,  0, 64, 67],
    [ 0,  0,  0,  0,  0,  0, 67, 69],
    [72,  0,  0,  0, 69,  0, 67,  0],
    [65,  0, 64,  0, 62,  0, 60, 62],
    [64,  0, 64,  0, 64,  0, 64,  0],
    [60,  0, 57,  0, 60,  0, 62, 62]
]).reshape((-1))

# Mapping from number to pitch
num2pitch = {
    -1: "-",  # 延时符号
    0: "0",  # 休止符号
    36: "C2", 38: "D2", 40: "E2", 41: "F2", 43: "G2", 45: "A2", 47: "B2",
    48: "C3", 50: "D3", 52: "E3", 53: "F3", 55: "G3", 57: "A3", 59: "B3",
    60: "C4", 62: "D4", 64: "E4", 65: "F4", 67: "G4", 69: "A4", 71: "B4",
    72: "C5", 74: "D5", 76: "E5", 77: "F5", 79: "G5", 81: "A5", 83: "B5",
    84: "C6", 86: "D6", 88: "E6", 89: "F6", 91: "G6", 93: "A6", 95: "B6",
}

def np2midi(npy_data, save_path):
    # Create a new MIDI file and track
    mid = MidiFile()
    track_ = MidiTrack()
    track = MidiTrack()
    mid.tracks.append(track_)
    mid.tracks.append(track)

    # Set tempo (120 BPM)
    tempo = mido.bpm2tempo(120)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Add notes to the track
    time_step = 240  # Duration of each time step in MIDI ticks (can be adjusted)

    # Revised loop to handle notes and rests
    time_since_last_note = 0  # Time accumulator for rests
    for note_number in npy_data:
        if note_number > 0:  # Note
            # If there was a rest before this note, add accumulated time to the current note
            track.append(Message('note_on', note=note_number, velocity=64, time=time_since_last_note))
            track.append(Message('note_off', note=note_number, velocity=64, time=time_step))
            time_since_last_note = 0
        else:  # Rest
            time_since_last_note += time_step
    # Save the MIDI file
    mid.save(save_path)


np2midi(npy_data, './your_midi_file.mid')
readed = read_mid('./your_midi_file.mid', 1)
