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
        counts.append((row_counts > threshold).sum())
    counts = np.array(counts)
    # score with repeatness
    score = np.ones(np.shape(music)[0]) * 100
    score -= counts * 5
    return np.clip(score, a_min=0, a_max=100)


def rest(music:np.array):
    '''
    Args:
    music: 2D array
    '''
    # count length of continuous pitch
    counts = []
    mask = music != 0
    for row in mask:
        labeled_array, _ = label(row)
        row_counts = np.bincount(labeled_array)[1:] # remove 0
        counts.append((row_counts > 16).sum())
    counts = np.array(counts)
    # score with rest
    score = np.ones(np.shape(music)[0]) * 100
    score -= counts * 5
    return np.clip(score, a_min=0, a_max=100)


def melody_hold(music:np.array):
    '''
    Args:
    music: 2D array
    '''
    # Each measure is divided into four beats, 
    # with melodic notes on at least two beats
    music_1 = music.reshape((-1, 2)).sum(axis=1)
    music_1[music_1!=0] = 1
    music_2 = 4 - music_1.reshape((-1, 4)).sum(axis=1)
    music_2[music_2<3] = 0
    punishment = music_2.reshape((-1, 16)).sum(axis=1)
    assert np.shape(music)[0] == np.shape(punishment)[0]
    # score with rest
    score = np.ones(np.shape(music)[0]) * 100
    score -= punishment * 5
    return np.clip(score, a_min=0, a_max=100)


def rhythm_score(music:np.array, 
                 threshold_f:int = 12, 
                 weight_r:float = 0.3, weight_f:float = 0.3, weight_m:float = 0.4):
    '''
    Args:
    music: 2D array
    threshold_f: maximum counts of continuous fast pitch
    weight_r: weigh of rest score
    weight_f: weight of fast score
    weight_m: weight of melody_hold score
    '''
    assert len(np.shape(music)) == 2

    
    return rest(music)*weight_r + continuous_fast(music, threshold_f)*weight_f + melody_hold(music)*weight_m

