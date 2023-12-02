import os


# convert num to pitch
# 21-108 to pitch a0-c8
def num_to_pitch(num):
    alpha_dict = {0: 'A', 1: 'A#', 2: 'B', 3: 'C', 4: 'C#', 5: 'D', 6: 'D#', 7: 'E', 8: 'F', 
                  9: 'F#', 10: 'G', 11: 'G#'}
    if (num < 21) | (num > 108):
        print("warning, num out of range!")
        exit(1)
    num = num - 21
    alpha = num % 12  # a b c d e f g
    belta = num // 12  # 0-8
    if alpha > 2:
        belta = belta + 1
    pitch_str = alpha_dict[alpha] + str(belta)
    return pitch_str


#convert a vector to str
#C#4 0 -
def single_vec_to_str(vector):
    ret_str = []
    for num in vector:
        if num == 20:
            ret_str.append('-')
        elif num == 0:
            ret_str.append('0')
        else:
            word = num_to_pitch(num)
            ret_str.append(word)
    ret = ' '.join(ret_str)
    return ret