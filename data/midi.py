import mido
import numpy as np
from tqdm import tqdm

import sys
sys.path.append('..')
from definitions import *


def read_mid(path: str):
    '''
    Args:
        path: path to load midi file
    '''
    mid = mido.MidiFile(path)
    num = []
    pitch = []
    msgs = list(mid.tracks[1])
    msgs = msgs[1:-1]
    for msg in msgs:
        if msg.type == 'note_on':
            print(msg)
            n = msg.time // time
            if n == 0:
                continue
            p = msg.note
            num += [p] + [-1] * (n-1)
            pitch += [num2pitch[p]] 
            if n > 1:
                pitch += [num2pitch[-1] * (n-1)]
        # elif msg.type == 'note_off':
        #     n = msg.time // 120
        #     num += [0] * n
        #     pitch += ['0'] * n
    return num, pitch

num, pitch = read_mid('./问.mid')
print(num)
print(pitch)
