import numpy as np

import sys

sys.path.append("..")
from definitions import *

def in5(a, b):  # 在五和弦里
    if a == b or a == (b + 2) % 7 or a == (b + 4) % 7:
        return True
    return False


def in7(a, b):  # 在七和弦里
    if in5(a, b):
        return True
    if a == (b + 6) % 7:
        return True
    return False


def calc(
    length: int, a: np.ndarray, rate7: float, chord_B: float, rate7_penalty: float, b: np.ndarray
):
    """
    chords:和弦库
    chords_type:和弦属性
    """
    ans = 0.0
    a = a % 12
    id = 0
    cnt = -1
    for chord, chord_type in zip(chords, chords_type):
        # Fixed by hzj
        cnt = cnt + 1
        m = len(chord)
        mnnum7 = 0.0
        mxnum7 = 0.0
        neq = False
        if length != m:
            continue
        for j in range(m):
            if in7(a[j], chord[j]):
                mxnum7 += 1
                if in5(a[j], chord[j]) == False:
                    mnnum7 += 1
            else:
                if b[j]==0 or j != m-1:
                    neq = True
                    break
        if neq == True:
            continue
        mxnum7 /= length
        mnnum7 /= length
        nwans = 1.0
        if chord_type == 1:  # A : 0 , B : 1 # Fixed definitions.py by hzj
            nwans = chord_B
        if mxnum7 < rate7:
            nwans = nwans * (1 - (rate7 - mxnum7) * rate7_penalty)
        if mnnum7 > rate7:
            nwans = nwans * (1 - (mnnum7 - rate7) * rate7_penalty)
        if(nwans > ans):
            ans = nwans
            id = cnt
    return (ans,id)


def chord_score(
    music: np.ndarray,
    not_in_chord: float = 0.8,
    rate7: float = 0.25,
    chord_B: float = 0.9,
    rate7_penalty: float = 0.1,
    debug_mode: int = 1
):
    """
    Args:
    music: 2D array
    fi : 截止到第i-1个位置的最高分
    rate7 : 最佳的七和弦的比例
    rate7_penalty : 七和弦比例偏差导致的扣分程度
    chord_B : B和弦走向的扣分系数
    not_in_chord : 一个小节无法匹配进和弦的扣分系数
    """
    (n, m) = np.shape(music)
    mm = m // 8
    nw = np.zeros((n, mm))
    tags = np.zeros((n,mm))
    score = np.zeros(n)
    # Fixed by hzj 
    for i in range(n):
        for j in range(0, m, 8):
            if music[i][j] != 0:
                nw[i][j // 8] = chord_trans[music[i][j] % 12]
                continue
            if music[i][j] == 0 and music[i][j+1] == 0 and \
            music[i][j+2] == 0 and music[i][j+3] == 0 and music[i][j+7]==0:
                tags[i][j//8]=1
            if j != 0:
                if music[i][j - 1] != 0:
                    nw[i][j // 8] = chord_trans[music[i][j - 1] % 12]
                    continue
            for k in range(1, 8):
                if music[i][j + k] != 0:
                    nw[i][j // 8] = chord_trans[music[i][j + k] % 12]
                    break
        
        f = np.zeros(mm + 1)
        lst1 = np.zeros(mm + 1,dtype=int)
        lst2 = np.zeros(mm + 1,dtype=int)
        f[0] = 100
        for j in range(mm):
            f[j + 1] = f[j] * not_in_chord
            lst2[j+1] = j
            if(j==3 or j==7 or j==11 or j==15):
                for k in range(j):
                    if j == 11 and k == 4:
                        continue
                    (val,id) =  calc(j - k + 1, nw[i][k : j + 1], rate7, chord_B, rate7_penalty,tags[i][k:j+1])
                    if(f[k] * val > f[j+1]):
                        f[j + 1] = f[k] * val
                        lst1[j+1] = id
                        lst2[j+1] = k
        if debug_mode == 1:
            print('*Period %d:' %(i))
            nww = mm
            while nww != 0:
                print('%d to %d' %(lst2[nww],nww),chords[lst1[nww]])
                nww = lst2[nww]
        score[i] = f[mm]

    return score
