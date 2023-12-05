import numpy as np
from definitions import *

def replace_delay(music:np.array):
    '''
    Function: 
    replace -1 with pitch.
    e.g. 76, -1, -1 will be replaced by 76, 76, 76
    Args:
    music: 2D array
    '''
    assert len(np.shape(music)) == 2
    mask = music == -1
    pos = np.where(mask, np.roll(music, 1, axis=1), 0)
    values_to_replace = np.maximum.accumulate(pos, axis=1)
    result = np.where(mask, values_to_replace, music)
    return result

