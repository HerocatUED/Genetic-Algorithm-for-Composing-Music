import numpy as np

import sys
sys.path.append('..')
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


def repeatness(music:np.array, threshold:float):
    '''
    Args:
    music: 2D array
    threshold: maximum repeatness
    '''
    # calculate repeatness
    music_num = np.shape(music)[0]
    max_rate = np.zeros(music_num*16)
    music1 = music.reshape((-1, 8)).copy()
    for i in range(music_num*16):
        _, counts = np.unique(music1[i], return_index=False, return_inverse=False, return_counts=True)
        max_rate[i] = np.max(counts)/8
    max_rate[max_rate<threshold] = 0
    max_rate = max_rate.reshape((-1, 16)).sum(axis=1)
    # score with repeatness
    score = np.ones(music_num) * 100
    score[max_rate>threshold] -= max_rate * 5
    return np.clip(score, a_min=0, a_max=100)


def fluctuation(music:np.array, nonzero_cnt: int, threshold:float, threshold_2:float):
    '''
    Args:
    music: 2D array
    nonzero_cnt: num of nonzero
    threshold: maximum average fluctuation
    threshold_2: maximum fluctuation
    '''
    # padding
    music_1 = np.pad(music, ((0,0),(1,0)), 'constant', constant_values=0)
    music_2 = np.pad(music, ((0,0),(0,1)), 'constant', constant_values=0)
    # calculate fluctuation
    det_music = np.abs((music_2 - music_1)[:, 1:-1])
    # det_music[det_music>36] = 0 # consider rest pitch
    avg_fluctuation = np.sum(det_music, axis=1) / nonzero_cnt
    det_music[det_music<=threshold_2] = 0
    det_music[det_music>0] = 1
    max_fluctuation = np.sum(det_music, axis=1)
    # score with fluctuation
    score = np.ones( np.shape(music)[0]) * 100
    score[avg_fluctuation>threshold] -= avg_fluctuation[avg_fluctuation>threshold] * 5
    score -= max_fluctuation * 3
    return np.clip(score, a_min=0, a_max=100)


def melody_score(
    music:np.array, 
    threshold_r:float = 0.5, threshold_f:float = 3, threshold_m:float = 6,
    weight_r:float = 0.3, weight_f:float = 0.7):
    '''
    Args:
    music: 2D array
    threshold_r: maximum rate for repeatness
    threshold_f: maximum average fluctuation
    threshold_m: maximum fluctuation
    weight_r: weigh of repeatness score
    weight_f: weight of fluction score
    '''
    assert len(np.shape(music)) == 2
    
    music_1 = replace_delay(music, -1)
    music_2 = replace_delay(music_1, 0)
    nonzero_cnt = np.count_nonzero(music_1, axis=1)

    score = repeatness(music_1, threshold_r)*weight_r + fluctuation(music_2, nonzero_cnt, threshold_f, threshold_m)*weight_f
    out_of_range_mask = (music_2 < min_pitch) | (music_2 > max_pitch)
    out_of_range_mask = np.any(out_of_range_mask, axis=1)
    score[out_of_range_mask] = 0
    return score
    
    