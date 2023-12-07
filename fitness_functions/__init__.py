import numpy as np

from melody import melody_score
from chord import chord_score
from rhythm import rhythm_score

import sys
sys.path.append('..')
from definitions import *

chord_trans = [0,2,4,5,7,9,11]

def chord_init():
    (n,m)=np.shape(chords)
    for i in range(n):
        for j in range(m):
            chords[i][j]=chord_trans[chords[i][j]]
    return

def fitness_function(music:np.array):
    '''
    Args:
    music: 2D array
    '''
    assert len(np.shape(music)) == 2
    
    return melody_score(music) + chord_score(music) + rhythm_score(music)
