import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message
from midi import read_mid


def npy2midi(data, res_path):
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
    for note_number in data:
        if note_number > 0:  # Note
            # If there was a rest before this note, add accumulated time to the current note
            track.append(Message('note_on', note=note_number, velocity=64, time=time_since_last_note))
            track.append(Message('note_off', note=note_number, velocity=64, time=time_step))
            time_since_last_note = 0
        else:  # Rest
            time_since_last_note += time_step
    # Save the MIDI file
    mid.save(res_path)

def test():
    result = np.load('./result/final_population.npy')
    npy2midi(result[0], './result/outputmusic0.mid')
    readed = read_mid('./result/outputmusic0.mid', 1)
    readed = np.expand_dims(readed, axis=0)
    from fitness_functions import chord_score
    chord_score(readed, debug_mode=1)