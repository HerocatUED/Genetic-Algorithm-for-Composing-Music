import numpy as np
from scipy.ndimage import label

import sys
sys.path.append('..')
from definitions import *


def continuous_fast(music:np.array, threshold:int):
    '''
    Args:
    music: 2D array
    threshold: maximum counts of continuous fast pitch
    '''
    # count length of continuous fast pitch
    counts = []
    mask = (music != 0) & (music != -1)
    for row in mask:
        labeled_array, _ = label(row)
        row_counts = np.bincount(labeled_array)[1:] # remove 0
        counts.append((row_counts >= threshold).sum())
    counts = np.array(counts)
    # score with repeatness
    score = np.ones(np.shape(music)[0]) * 100
    score -= counts * 10
    return np.clip(score, a_min=0, a_max=100)


def rest(music:np.array, threshold: float):
    '''
    Args:
    music: 2D array
    threshold: maximum counts of continuous non-rest pitch
    '''
    # count length of continuous pitch
    counts = []
    mask = music != 0
    for row in mask:
        labeled_array, _ = label(row)
        row_counts = np.bincount(labeled_array)[1:] # remove 0
        counts.append((row_counts >= threshold).sum())
    counts = np.array(counts)
    # score with rest
    score = np.ones(np.shape(music)[0]) * 100
    score -= counts * 10
    return np.clip(score, a_min=0, a_max=100)


def melody_hold(music:np.array):
    '''
    Args:
    music: 2D array
    '''
    # Each measure is divided into four beats, 
    # with melodic notes on at least two beats
    music_1 = music.reshape((-1, 2)).copy()
    music_1[music_1!=0] = 1
    # 反拍
    reverse = np.zeros(np.shape(music_1)[0])
    mask = np.logical_and(music_1[:, 0]==0, music_1[:, 1]==1)
    reverse[mask] = 1
    reverse = reverse.reshape(-1, 4).sum(axis=1)
    reverse[reverse<2] = 0
    punishment_reverse = np.square(reverse)
    punishment_reverse = punishment_reverse.reshape(-1, 16).sum(axis=1) * 2
    # 至少两拍有音
    hold = music_1.sum(axis=1)
    hold = 4 - hold.reshape((-1, 4)).sum(axis=1)
    hold[hold<3] = 0
    punishment_hold = hold.reshape((-1, 16)).sum(axis=1) * 5
    punishment = punishment_hold + punishment_reverse
    assert np.shape(music)[0] == np.shape(punishment)[0]
    # score with rest
    score = np.ones(np.shape(music)[0]) * 100
    score -= punishment
    return np.clip(score, a_min=0, a_max=100)


def rhythm_score(music:np.array, 
                 threshold_r:int = 16, threshold_f:int = 5, 
                 weight_r:float = 0.15, weight_f:float = 0.15, weight_m:float = 0.7):
    '''
    Args:
    music: 2D array
    threshold_f: maximum counts of continuous fast pitch
    weight_r: weigh of rest score
    weight_f: weight of fast score
    weight_m: weight of melody_hold score
    '''
    assert len(np.shape(music)) == 2

    return rest(music, threshold_r)*weight_r + continuous_fast(music, threshold_f)*weight_f + melody_hold(music)*weight_m

