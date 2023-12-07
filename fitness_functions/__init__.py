import numpy as np

from melody import melody_score
from chord import chord_score
from rhythm import rhythm_score

def fitness_function(music:np.array):
    '''
    Args:
    music: 2D array
    '''
    assert len(np.shape(music)) == 2
    
    return melody_score(music) + chord_score(music) + rhythm_score(music)
