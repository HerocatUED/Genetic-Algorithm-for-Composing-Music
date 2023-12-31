import mido
import numpy as np

from definitions import *


def read_mid(path: str, mode :int = 0):
    '''
    Args:
        path: path to load midi file
        mode: 0 if original, 1 if we saved
    '''
    mid = mido.MidiFile(path)
    num = [] # e.g. [76, 74, 0, 74]
    pitch = [] # e.g. ['E5', 'D5', '0', 'D5]
    msgs = list(mid.tracks[1])[1:-1]
    # convert
    for msg in msgs:
        if msg.type == 'note_off':
            n = msg.time // time_unit
            if n == 0: continue
            p = msg.note
            num += [p] + [-1] * (n-1)
            pitch += [num2pitch[p]] 
            if n > 1: pitch += [num2pitch[-1] * (n-1)]
        elif msg.type == 'note_on':
            n = msg.time // time_unit
            num += [0] * n
            pitch += ['0'] * n
    # pad the music to 18*8
    music = np.array(num,dtype=int)
    current_length = np.shape(num)[0]
    if mode == 0:
        music = np.pad(music, (0, padded_length-current_length), 'constant', constant_values=0)
        return music[8:17*8] # cutout the first and last
    else: return music

