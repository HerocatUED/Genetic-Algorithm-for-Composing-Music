import mido
from tqdm import tqdm


def read_mid(path: str):
    '''
    Args:
        path: path to load midi file
    '''
    mid = mido.MidiFile(path)
    for i, track in tqdm(enumerate(mid.tracks), desc=f'loading midi from {path}'):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)



def num2pitch(yin):
    return {
        # 3
        '48': 'C3',
        '50': 'D3',
        '52': 'E3',
        '53': 'F3',
        '55': 'G3',
        '57': 'A3',
        '59': 'B3',
        # 4
        '60': 'C4',
        '62': 'D4',
        '64': 'E4',
        '65': 'F4',
        '67': 'G4',
        '69': 'A4',
        '71': 'B4',
        # 5
        '72': 'C5',
        '74': 'D5',
        '76': 'E5',
        '77': 'F5',
        '79': 'G5',
        '81': 'A5',
        '83': 'B5',
    }
    