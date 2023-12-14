import numpy as np

import sys
sys.path.append('..')
from definitions import *

chord_trans = [1,1,2,2,3,4,4,5,5,6,6,0] #将12音级暂时转化为0~6，其中1为do,...,6为la,0为si

def in5(a:int,b:int): # 在五和弦里
    if a == b or a == (b+2)%7 or a == (b+4)%7:
        return True
    return False

def in7(a:int,b:int): # 在七和弦里
    if(in5(a,b)):
        return True
    if a == (b+6)%7:
        return True
    return False

def calc(len:int,a:np.array,rate7:float,chord_B:float,rate7_penalty:float):
    '''
    chords:和弦库
    chords_type:和弦属性
    '''
    ans = 0.0
    (n,) = np.shape(chords)
    for i in range(len):
        a[i] %= 12
    for i in range(n):
        m = np.shape(chords)
        mnnum7 = 0.0
        mxnum7 = 0.0
        neq = False
        if len != m:
            continue
        for j in range(m):
            if in7(a[j],chords[i][j]):
                mxnum7 += 1
                if in5(a[j],chords[i][j]) == False:
                    mnnum7 += 1
            else:
                neq = True
                break
        if neq == True:
            continue
        mxnum7 /= len
        mnnum7 /= len
        nwans = 1.0
        if(chords_type[i] == 1): # A : 0 , B : 1
            nwans = chord_B
        if(mxnum7 < rate7):
            ans = ans * (1-(rate7-mxnum7)*rate7_penalty)
        if(mnnum7 > rate7):
            ans = ans * (1-(mnnum7 - rate7)*rate7_penalty)
        ans = max(ans,nwans)
    return ans

def chord_score(music:np.array,not_in_chord:float = 0.8,rate7:float = 0.25,chord_B:float = 0.9,rate7_penalty:float = 0.1):
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
                nw[i][j/8]=chord_trans[music[i][j]%12]
                continue
            if j!=0:
                if music[i][j-1]!=0:
                    nw[i][j/8]=chord_trans[music[i][j-1]%12]
                    continue
            for k in range(1,8):
                if music[i][j+k]!=0:
                    nw[i][j/8]=chord_trans[music[i][j+k]%12]
                    break

    for i in range(n):
        f = np.zeros(mm+1)
        f[0]=100
        for j in range(mm):
            f[j+1]=f[j]*not_in_chord
            for k in range(j):
                f[j+1]=max(f[j+1],f[k]*calc(j-k+1,nw[i][k:j],rate7,chord_B,rate7_penalty))
        score[i]=f[mm]

    return score
    pass
