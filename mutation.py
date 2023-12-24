import numpy as np
import random
from definitions import *

def cross_over(music1, music2):
    music1 = music1.copy()
    music2 = music2.copy()
    # 遗传算子使用的是单点交叉，即随机选取一个位置，将两个音乐在该位置进行交换
    # 但注意为了避免过大的混乱，我们对小节进行对齐，所以这里的交叉点应该是小节的位置
    # 改成半小节
    cross_point = random.randint(0, music1.shape[0] // 4 - 1) * 4
    music1[cross_point:], music2[cross_point:] = (
        music2[cross_point:],
        music1[cross_point:],
    )
    return music1, music2


def reflection(music):
    a0 = music[0]
    return 2*a0 - music


def inversion(music):
    return music[::-1]


def shift(music):
    d = random.randint(0, 3)
    return music + d

def mutate(music, mutation_rate):
    # 对每一个小节，均存在一个变异的概率，如果变异，则对该小节随机使用倒影/逆行/移调变换
    for i in range(music.shape[0] // 8):
        if random.random() < mutation_rate:
            m = music[i * 8 : (i + 1) * 8] // 12
            r = music[i * 8 : (i + 1) * 8] % 12
            # 转换成0-6
            mutated = random.choice([reflection, inversion, shift])(chord_trans[r])
            m1 = mutated // 7
            r1 = mutated % 7
            music[i * 8 : (i + 1) * 8] = (m + m1) * 12 + reverse_trans[r1]
    return music

