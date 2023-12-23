# 使用遗传算法生成音乐，包括和弦、旋律、节奏等评分
import sys
import os
import numpy as np

sys.path.append("./fitness_functions")
from fitness_functions import fitness_function
from fitness_functions.chord import chord_score
from fitness_functions.melody import melody_score
from fitness_functions.rhythm import rhythm_score
from data.midi import read_mid
from pathlib import Path
from torch.utils.tensorboard.writer import SummaryWriter
from tqdm import tqdm


def main(data_dir: Path, save_path: Path,max_iters:int):
    # read midis
    print("Reading midi files...")
    midi_paths = list(data_dir.glob("*.mid"))

    musics = np.stack([read_mid(path) for path in midi_paths], axis=0)

    print(musics.shape)
    
    
    mididx = 14
    music = musics[mididx].copy()
    idx = music ==0
    music = music % 12 + 1
    music[idx] = 0
    print(music)    
    
    # calculate fitness
    print("Calculating fitness...")
    fitness = fitness_function(musics)
    chord_losses = chord_score(musics)
    melody_losses = melody_score(musics)
    rhythm_losses = rhythm_score(musics)
    for path, fit, chord_loss, melody_loss, rhythm_loss in zip(
        midi_paths, fitness, chord_losses, melody_losses, rhythm_losses
    ):
        print(
            f"{path.name:\u3000<11} [fit: {fit:7.3f}], [chord: {chord_loss:7.3f}], [melody: {melody_loss:7.3f}], [rhythm: {rhythm_loss:7.3f}]"
        )

    # iter loops
    
    for iter in tqdm(range(max_iters)):
        
    #writer = SummaryWriter(log_dir=os.path.join('experiments', args.exp_name, 'logs'))
    # calculate fitness


if __name__ == "__main__":
    # 存放midi文件的路径
    data_dir = Path("../mididata")
    save_path = Path("./result")
    save_path.mkdir(parents=True, exist_ok=True)

    main(data_dir=data_dir, save_path=save_path,max_iters=50)
