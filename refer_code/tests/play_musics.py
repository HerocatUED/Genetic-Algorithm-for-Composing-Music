import os
import sys

os.chdir(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.realpath('.'))

import argparse
import time
from pysinewave import SineWave
from utils.conversions import *
from utils.manipulation import *
from utils.player import play_pitches

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', type=int, default=13)
    parser.add_argument('--in_c', type=bool, default=True)
    parser.add_argument('--dt', type=float, default=0.2)
    args = parser.parse_args()

    # load musics
    with open('data/music.txt', 'r') as f:
        musics = f.readlines()
    notes = musics[args.i].split()
    codes = notes2codes(notes)
    
    # load tones
    with open('data/tone.txt', 'r') as f:
        tones = f.readlines()
    tone = tones[args.i].strip()
    
    # to c
    if args.in_c:
        codes = shift(codes, tone2shift(tone))
    
    # convert format
    pichtes = codes2piches(codes)
    
    # play pitches
    play_pitches(pichtes, args.dt)
