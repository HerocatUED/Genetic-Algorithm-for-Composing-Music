import numpy as np
import random

# 杂交水稻


def crossOver(x, y):
    temp = len(x) / 8
    m = np.random.randint(1, temp+1)
    place = m * 8
    result = np.append(x[:place], y[place:])
    return result

# 平移变换

# def tone_shift():
#     arr = np.array(txt_to_tone()) - 60
#     return arr

def shift(x, n):
    return np.where(x >= 21, x+n, x)

# 随机平移


def randomShift(x):
    return shift(x, random.randint(-12, 12))

# 逐个随机平移


def randomChange(x):
    m = np.random.random(x.shape[0])*2-1
    # m = np.where(m > 0.8)
    mask1 = (m > 0.8) & (m < 1)
    mask2 = (m > 0.6) & (m < 0.8)
    mask3 = (m > -1.0) & (m < -0.8)
    mask4 = (m > -0.8) & (m < -0.6)
    m = np.zeros_like(x)
    m[mask1] = 2
    m[mask2] = 1
    m[mask3] = -1
    m[mask4] = -2
    m = m+x
    return np.where(x >= 21, m, x)

# 倒影变换


def shadow(x, n):
    return np.where(x >= 21, n-x, x)

# 围绕中央c倒影


def c_shadow(x):
    return shadow(x, 120)


def centered_shadow(x):
    center = np.max(np.where(x >= 21, x, 60))+np.min(np.where(x >= 21, x, 60))
    return shadow(x, center)

# 向中间靠拢


def centering(x):
    mask = x >= 21
    center = np.average(x[mask])
    y = x[mask]-center
    x[mask] = np.where(y > 12, x[mask]-12, x[mask])
    x[mask] = np.where(y < -12, x[mask]+12, x[mask])
    return x

# 逆行变换


def reverse(x):
    return x[::-1]


def nearest_CAGED(x):
    y = x % 12
    delta = np.zeros_like(x)
    delta[(y == 1) | (y == 3) | (y == 8)] = -1 + (np.random.rand(((y == 1) | (y == 3) | (y == 8)).sum()) > 0.5) * 2
    delta[(y == 5) | (y == 10)] = -1
    delta[(y == 6) | (y == 11)] = 1
    return x + delta


def nearest_Cmaj(x):
    y = x % 12
    delta = np.zeros_like(x)
    delta[(y == 1) | (y == 3) | (y == 8)] = -1 + (np.random.rand(((y == 1) | (y == 3) | (y == 8)).sum()) > 0.5) * 2
    delta[(y == 10)] = -1
    delta[(y == 6)] = 1
    return x + delta


def nearest_Cmin(x):
    y = x % 12
    delta = np.zeros_like(x)
    delta[(y == 1) | (y == 4) | (y == 9) | (y == 11)] = -1 + (np.random.rand(((y == 1) | (y == 4) | (y == 9) | (y == 11)).sum()) > 0.5) * 2
    delta[(y == 6)] = 1
    return x + delta


# 靠拢变换


def clamp_CAGED(x):
    return np.where(x >= 21, nearest_CAGED(x), x)


def clamp_Cmaj(x):
    return np.where(x >= 21, nearest_Cmaj(x), x)


def clamp_Cmin(x):
    return np.where(x >= 21, nearest_Cmin(x), x)


def section_operate(x):
    p1 = random.random()
    p2 = random.random()
    p3 = random.random()
    p4 = random.random()
    if p1 > 0.8:
        x = reverse(x)
    if p2 > 0.8:
        x = centered_shadow(x)
    if p3 > 0.6:
        x = randomChange(x)

    return x


def random_operate(x):
    x1 = section_operate(x[0:8])
    x2 = section_operate(x[8:16])
    x3 = section_operate(x[16:24])
    x4 = section_operate(x[24:32])
    return centering(np.concatenate([x1, x2, x3, x4]))
