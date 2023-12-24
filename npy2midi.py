import mido
import numpy as np
from pathlib import Path
from definitions import *

npypath = Path("./result/final_population.npy")
data = np.load(npypath)
print(data[0].reshape(-1,8))