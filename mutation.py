import numpy as np
import random


def cross_over(music1, music2):
    music1 = music1.copy()
    music2 = music2.copy()
    # 遗传算子使用的是单点交叉，即随机选取一个位置，将两个音乐在该位置进行交换
    # 但注意为了避免过大的混乱，我们对小节进行对齐，所以这里的交叉点应该是小节的位置
    cross_point = random.randint(0, music1.shape[0] // 8 - 1) * 8
    music1[cross_point:], music2[cross_point:] = (
        music2[cross_point:],
        music1[cross_point:],
    )
    return music1, music2


def reflection(music):
    return music


def inversion(music):
    return music[::-1]


def shift(music):
    return music


def mutate(music, mutation_rate):
    # 对每一个小节，均存在一个变异的概率，如果变异，则对该小节随机使用倒影/逆行/移调变换
    for i in range(music.shape[0] // 8):
        if random.random() < mutation_rate:
            music[i * 8 : (i + 1) * 8] = random.choice([reflection, inversion, shift])(
                music[i * 8 : (i + 1) * 8]
            )
    return music

