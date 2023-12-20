# convert to pitch from numbers recorded in midi file
num2pitch = {
    -1: "-",  # 延时符号
    0: "0",  # 休止符号
    # 2
    36: "C2",
    38: "D2",
    40: "E2",
    41: "F2",
    43: "G2",
    45: "A2",
    47: "B2",
    # 3
    48: "C3",
    50: "D3",
    52: "E3",
    53: "F3",
    55: "G3",
    57: "A3",
    59: "B3",
    # 4
    60: "C4",
    62: "D4",
    64: "E4",
    65: "F4",
    67: "G4",
    69: "A4",
    71: "B4",
    # 5
    72: "C5",
    74: "D5",
    76: "E5",
    77: "F5",
    79: "G5",
    81: "A5",
    83: "B5",
    # 6
    84: "C6",
    86: "D6",
    88: "E6",
    89: "F6",
    91: "G6",
    93: "A6",
    95: "B6",
}

# 八分音符在midi中对应的时长
time_unit = 240

# 音乐片段数组表示的长度：16小节每小节8个八分音符
music_length = int(16 * 8)
# 算上前后两个空小节
padded_length = int(18 * 8)

# chords : 和弦枚举 chords_type：0/1表示A/B和弦
chords = [
    [1, 6, 4, 5],
    [1, 1, 1, 1],
    [6, 6, 6, 6],
    [1, 5, 1, 5],
    [1, 5, 6, 3, 4, 5, 1, 1],
    [1, 5, 6, 3, 4, 1, 2, 5],
    [1, 5, 6, 3, 4, 1, 4, 5],
    [1, 4, 6, 4],
    [1, 4, 6, 5],
    [1, 3, 6, 3],
    [4, 5, 3, 6, 2, 2, 5, 5],
    [6, 4, 5, 1],
    [6, 4, 2, 3],
    [4, 5, 3, 6],
    [2, 5, 1, 1],
    [1, 4, 5, 1],
    [1, 5, 5, 1],
    [6, 4, 1, 5],
    [6, 2, 3, 6],
    [4, 5, 6, 6],
    [4, 5, 1, 1],
    [4, 3, 6, 6],
    [2, 3, 6, 6],
    [2, 5, 1, 6],
    [6, 2, 5, 1],
    [6, 1, 2, 3],
    [6, 1, 2, 6],
    [6, 6, 2, 6],
    [1, 2, 5, 1, 6, 2, 5, 5],
    [1, 1, 6, 6, 4, 4, 5, 5],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [6, 6, 6, 6, 6, 6, 6, 6],
    [1, 1, 5, 5, 1, 1, 5, 5],
    [1, 1, 4, 4, 6, 6, 4, 4],
    [1,1, 4,4, 6,6, 5,5],
    [1,1, 3,3, 6,6, 3,3],
    [6,6, 4,4, 5,5, 1,1],
    [6,6, 4,4, 2,2, 3,3],
    [4,4, 5,5, 3,3, 6,6],
    [2,2, 5,5, 1,1, 1,1],
    [1,1, 4,4, 5,5, 1,1],
    [1,1, 5,5, 5,5, 1,1],
    [6,6, 4,4, 1,1, 5,5],
    [6,6, 2,2, 3,3, 6,6],
    [4,4, 5,5, 6,6, 6,6],
    [4,4, 5,5, 1,1, 1,1],
    [4,4, 3,3, 6,6, 6,6],
    [2,2, 3,3, 6,6, 6,6],
    [2,2, 5,5, 1,1, 6,6],
    [6,6, 2,2, 5,5, 1,1],
    [6,6, 1,1, 2,2, 3,3],
    [6,6, 1,1, 2,2, 6,6],
    [6,6, 6,6, 2,2, 6,6],
    [1,1, 5,5, 2,2, 4,4],
    [1,1,5,5, 6,6, 3,3],
    [1, 5, 2, 4],
    [1, 5, 6, 3],
]
chords_type = [
    0,
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,

    0,
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]
