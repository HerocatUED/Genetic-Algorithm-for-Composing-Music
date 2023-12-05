import numpy as np

import sys
sys.path.append('..')
from definitions import *


def chord_score(music:np.array,rate7:float= 0.3,not_in_chord:float = 0.8,chord_B = 0.9,rate7_penalty:float = 0.1):
    '''
    Args:
    music: 2D array
    fi : 截止到第i-1个位置的最高分
    rate7 : 最佳的七和弦的比例
    rate7_penalty : 七和弦比例偏差导致的扣分程度
    chord_B : B和弦走向的扣分系数
    not_in_chord : 一个小节无法匹配进和弦的扣分系数
    '''
    (n,m) = np.shape(music)
    mm:int = m/8
    nw = np.zeros((n,mm))
    score = np.zeros(n)
    for i in range(n):
        for j in range(0,m,8):
            if music[i][j]!=0 :
                nw[i][j/8]=music[i][j]
                continue
            if j!=0:
                if music[i][j-1]!=0:
                    nw[i][j/8]=music[i][j-1]
                    continue
            for k in range(1,8):
                if music[i][j+k]!=0:
                    nw[i][j/8]=music[i][j+k]
                    break

    for i in range(n):
        f = np.zeros(mm+1)
        f[0]=100
        for j in range(mm):
            f[j+1]=f[j]*not_in_chord
            for k in range(j):
                f[j+1]=max(f[j+1],f[k]*calc(k,j,nw[i][k:j]))
        score[i]=f[mm]

    return score
    pass
