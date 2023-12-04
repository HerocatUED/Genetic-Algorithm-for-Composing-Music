# convert to pitch from numbers recorded in midi file
num2pitch = {
    -1: '-', # 延时符号
    0: '0', # 休止符号
    # 2
    36: 'C2',
    38: 'D2',
    40: 'E2',
    41: 'F2',
    43: 'G2',
    45: 'A2',
    47: 'B2',
    # 3
    48: 'C3',
    50: 'D3',
    52: 'E3',
    53: 'F3',
    55: 'G3',
    57: 'A3',
    59: 'B3',
    # 4
    60: 'C4',
    62: 'D4',
    64: 'E4',
    65: 'F4',
    67: 'G4',
    69: 'A4',
    71: 'B4',
    # 5
    72: 'C5',
    74: 'D5',
    76: 'E5',
    77: 'F5',
    79: 'G5',
    81: 'A5',
    83: 'B5',
    # 6
    84: 'C6',
    86: 'D6',
    88: 'E6',
    89: 'F6',
    91: 'G6',
    93: 'A6',
    95: 'B6',
}

time = 240 # 八分音符在midi中对应的时间