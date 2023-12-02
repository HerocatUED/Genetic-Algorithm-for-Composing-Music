import time
from pysinewave import SineWave

def play_pitches(pichtes, dt):
    sinewaves = {}
    for pitch in pichtes:
        if type(pitch) == int:
            sinewaves[str(pitch)] = SineWave(pitch=pitch)
    for pitch in pichtes:
        print(pitch + 60 if type(pitch) == int else pitch)
        if pitch == 'rest':
            if 'sinewave' in locals():
                sinewave.stop()
                del sinewave
        elif pitch == 'hold':
            pass
        else:
            if 'sinewave' in locals():
                sinewave.stop()
                del sinewave
            sinewave = sinewaves[str(pitch)]
            sinewave.play()
        time.sleep(dt)
    if 'sinewave' in locals():
        sinewave.stop()
        del sinewave