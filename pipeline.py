# 使用遗传算法生成音乐，包括和弦、旋律、节奏等评分
import sys
import os
import random

import numpy as np
from tqdm import tqdm
from pathlib import Path
from torch.utils.tensorboard.writer import SummaryWriter

from midi import read_mid
from fitness_functions import *
from mutation import *


def main(
    data_dir: Path,
    save_path: Path,
    max_iters: int = 50,
    max_melody_num: int = 100,
    min_fitness: float = 130,
    mutation_rate: float = 0.01,
    mode=1,
):
    # read midis
    print("Reading midi files...")
    midi_paths = list(data_dir.glob("*.mid"))
    musics = np.stack([read_mid(path) for path in midi_paths], axis=0)

    print(musics.shape)
    # print(musics[0]) # 16*8

    if mode == 0:
        # calculate fitness
        print("Calculating fitness...")
        fitness = fitness_function(musics)
        chord_losses = chord_score(musics, debug_mode=0)
        melody_losses = melody_score(musics)
        rhythm_losses = rhythm_score(musics)
        results = zip(midi_paths, fitness, chord_losses, melody_losses, rhythm_losses)
        results = sorted(results, key=lambda x: x[1], reverse=True)
        for path, fit, chord_loss, melody_loss, rhythm_loss in results:
            print(
                f"{path.name:\u3000<11} [fit: {fit:7.3f}], [chord: {chord_loss:7.3f}], [melody: {melody_loss:7.3f}], [rhythm: {rhythm_loss:7.3f}]"
            )
        return

    # init population
    initial_population = musics[random.sample(range(musics.shape[0]), 10)].copy()

    writer = SummaryWriter(log_dir=Path("./result/logs"))
    # 设置最大留存旋律的数目阈值和最小适合度函数的阈值
    max_melody_num = 100
    min_fitness = 130
    # iter loops
    for iter in tqdm(range(max_iters)):
        cross_over_population = []
        print(initial_population.shape)
        for i in range(initial_population.shape[0]):
            for j in range(i + 1, initial_population.shape[0]):
                r1,r2 = cross_over(initial_population[i], initial_population[j])
                cross_over_population.append(r1)                 
                cross_over_population.append(r2)
        cross_over_population = np.array(cross_over_population)
        # mutation
        for i in range(cross_over_population.shape[0]):
            mutate(cross_over_population[i], mutation_rate)
        # calculate fitness
        fitness = fitness_function(cross_over_population)
        idx = fitness >= min_fitness
        cross_over_population = cross_over_population[idx]
        fitness = fitness[idx]
        # sort and select
        idx = np.argsort(fitness)[::-1]
        cross_over_population = cross_over_population[idx]
        fitness = fitness[idx]
        # update population
        initial_population = cross_over_population[:max_melody_num]
        # write_log
        writer.add_scalar("fitness/fitness", fitness.mean(), iter)
    # save
    np.save(save_path / "final_population.npy", initial_population)

    writer.close()


if __name__ == "__main__":
    # 存放midi文件的路径
    data_dir = Path("./data")
    save_path = Path("./result/")
    save_path.mkdir(parents=True, exist_ok=True)

    main(data_dir=data_dir, save_path=save_path, max_iters=50)
