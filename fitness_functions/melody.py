import numpy as np

import sys
sys.path.append('..')
from definitions import *
from utils import replace_delay


def repeatness(music:np.array, threshold:float):
    '''
    Args:
    music: 2D array
    threshold: maximum rate for repeatness
    '''
    # calculate repeatness
    music_num = np.shape(music)[0]
    max_rate = np.zeros(music_num)
    for i in range(music_num):
        _, counts = np.unique(music[i], return_index=False, return_inverse=False, return_counts=True)
        max_rate[i] = np.max(counts) / music_length
    # score with repeatness
    score = np.ones(music_num) * 100
    score[max_rate>threshold] *= (1 - max_rate[max_rate>threshold]) 
    return np.clip(score, a_min=0, a_max=100)


def fluctuation(music:np.array, threshold:float):
    '''
    Args:
    music: 2D array
    threshold: maximum average fluctuation
    '''
    # padding
    music_1 = np.pad(music, ((0,0),(1,0)), 'constant', constant_values=0)
    music_2 = np.pad(music, ((0,0),(0,1)), 'constant', constant_values=0)
    # calculate fluctuation
    det_music = (music_2 - music_1)[:, 1:-1]
    det_music[det_music>36] = 0 # consider rest pitch
    avg_fluctuation = np.sum(np.abs(det_music), axis=1) / music_length
    max_fluctuation = np.max(music, axis=1) - np.min(music, axis=1)
    # score with fluctuation
    score = np.ones( np.shape(music)[0]) * 100
    score[avg_fluctuation>threshold] -= avg_fluctuation[avg_fluctuation>threshold] * 5
    score[max_fluctuation>12] -= max_fluctuation[max_fluctuation>12] * 5
    return np.clip(score, a_min=0, a_max=100)


def melody_score(
    music:np.array, 
    threshold_r:float = 0.4, threshold_f:float = 3, 
    weight_r:float = 1, weight_f:float = 1):
    '''
    Args:
    music: 2D array
    threshold_r: maximum rate for repeatness
    threshold_f: maximum average fluctuation
    weight_r: weigh of repeatness score
    weight_f: weight of fluction score
    '''
    assert len(np.shape(music)) == 2

    music_1 = replace_delay(music)
    
    return repeatness(music_1, threshold_r)*weight_r + fluctuation(music, threshold_f)*weight_f
    
    