import numpy as np
from definitions import *

def replace_delay(music:np.array, pitch:int=-1):
    '''
    Function: 
    replace -1 with pitch before it.
    e.g. 76, -1, -1 will be replaced by 76, 76, 76
    Args:
    music: 2D array
    pitch to be replaced, defalut to -1
    '''
    assert len(np.shape(music)) == 2
    result = music.copy()
    while(np.shape(result[result==pitch])[0] > 0):
        mask = result == pitch
        result = np.where(mask, np.roll(result, 1, axis=1), result)
    return result