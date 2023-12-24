import numpy as np
import mido
from pathlib import Path
from mido import MidiFile, MidiTrack, Message

path = Path("./result/final_population.npy")
data = np.load(path)
print(data[0].reshape(-1, 8))
