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
