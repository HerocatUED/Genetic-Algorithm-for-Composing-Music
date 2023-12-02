import os


# mapping to number 21-108
def sound_map(sound):
    alpha_dict = {'a': 0, 'b': 2, 'c': 3, 'd': 5, 'e': 7, 'f': 8, 'g': 10}
    bias = 0
    if sound[0] == '#':
        bias = 1
        
    if sound[0+bias] not in alpha_dict:
        #print(sound)
        #print('alpha error!')
        return -1
    else:
        num = int(sound[1+bias])
        if (sound[0+bias] != 'a') & (sound[0+bias] != 'b'):
            num = num - 1
        value = alpha_dict[sound[0+bias]] + num * 12 + 21
    if value + bias < 21 | value + bias > 108:
        print(sound)
        print('value error!')
        return -1
    return value + bias


# convert a single line to vector
def music_to_vector(pitch):
    vec = []
    for sound in pitch:
        if sound == ' ':
            continue
        elif sound[0] == '-':
            vec.append(20)
            continue
        elif sound[0] == '0':
            vec.append(0)
            continue
        else:
            # a0-c8
            ret = sound_map(sound)
            if ret == -1:
                continue
            vec.append(ret)

    if len(vec) != 32:
        print(vec)
        print(len(vec))
        exit(1)
    return vec


# convert music.txt to vector
def txt_to_vector():
    cnt = 0
    vec_list = []

    with open('.\data\music.txt') as file:
        contents = file.readlines()
        for line in contents:
            cnt = cnt + 1
            pitch = line.split(' ')
            vec = music_to_vector(pitch)
            vec_list.append(vec)
    return vec_list


# convert tone.txt to vector
def txt_to_tone():
    vec_list = []

    with open('./data/tone.txt') as file:
        contents = file.readlines()
        for line in contents:
            line = line.lower()
            vec = sound_map(line)
            vec_list.append(vec)
    return vec_list