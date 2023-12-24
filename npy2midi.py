import numpy as np
import mido
from pathlib import Path
from mido import MidiFile, MidiTrack, Message


# Example numpy array (representing the .npy data)
def npy2midi(res_path: Path, data):
    # Mapping from number to pitch
    npy_data = data.reshape(-1,8)
    # Create a new MIDI file and track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo (1
    # 20 BPM)
    tempo = mido.bpm2tempo(120)
    track.append(mido.MetaMessage("set_tempo", tempo=tempo))

    # Add notes to the track
    time_step = 480  # Duration of each time step in MIDI ticks (can be adjusted)

    # Revised loop to handle notes and rests
    for row in npy_data:
        time_since_last_note = 0  # Time accumulator for rests
        for note_number in row:
            if note_number > 0:  # Note
                # If there was a rest before this note, add accumulated time to the current note
                track.append(
                    Message(
                        "note_on",
                        note=note_number,
                        velocity=64,
                        time=time_since_last_note,
                    )
                )
                track.append(
                    Message("note_off", note=note_number, velocity=64, time=time_step)
                )
                time_since_last_note = 0
            else:  # Rest
                time_since_last_note += time_step
    # Save the MIDI file
    mid.save(res_path)