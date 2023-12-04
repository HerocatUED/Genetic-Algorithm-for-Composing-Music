import numpy as np

import sys
sys.path.append('..')
from definitions import *


def repeatness(music:np.array, threshold:float = 0.5):
    '''
    Args:
    music: 2D array
    threshold: maximum rate for repeatness
    '''
    assert len(np.shape(music)) == 2
    # calculate repeatness
    music_num = np.shape(music)[0]
    max_rate = np.zeros(music_num)
    for i in range(music_num):
        _, counts = np.unique(music[i], return_index=False, return_inverse=False, return_counts=True)
        max_rate[i] = np.max(counts) / music_length
    # score with repeatness
    score = np.ones(music_num) * 100
    score[max_rate>threshold] *= (1 - max_rate[max_rate>threshold]) 
    return score

def fluctuation(music:np.array, threshold:float = 3):
    '''
    Args:
    music: 2D array
    threshold: maximum average fluctuation
    '''
    assert len(np.shape(music)) == 2
    # padding
    music_num = np.shape(music)[0]
    music_1 = np.pad(music, ((0,0),(1,0)), 'constant', constant_values=0)
    music_2 = np.pad(music, ((0,0),(0,1)), 'constant', constant_values=0)
    # calculate fluctuation
    det_music = (music_2 - music_1)[:, 1:-1]
    avg_fluctuation = np.sum(np.abs(det_music), axis=1) / music_length
    max_fluctuation = np.max(music, axis=1) - np.min(music, axis=1)
    # score with fluctuation
    score = np.ones(music_num) * 100
    score[avg_fluctuation>threshold] -= avg_fluctuation[avg_fluctuation>threshold] * 5
    score[max_fluctuation>12] -= max_fluctuation[max_fluctuation>12] * 5
    return score
    