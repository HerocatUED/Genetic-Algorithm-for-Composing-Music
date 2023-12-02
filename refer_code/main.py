import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.realpath('.'))

import shutil
import argparse
import random
import numpy as np
from tqdm import tqdm
from utils.conversions import notes2codes
from utils.manipulation import *
from utils.fitness_function import initial_parameter, fitness_function
from torch.utils.tensorboard.writer import SummaryWriter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_name', type=str, default='exp_3')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--n_iters', type=int, default=100)
    parser.add_argument('--population', type=int, default=100)
    args = parser.parse_args()
    
    # save config
    
    os.makedirs(os.path.join('experiments', args.exp_name), exist_ok=True)
    output_file = open(os.path.join('experiments', args.exp_name, 'output.txt'), 'w')
    output_file.write(str(args) + '\n')
    
    # random seed
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    # initialize population
    
    with open('data/music.txt', 'r') as f:
        musics = f.readlines()
    initial_population = np.stack([notes2codes(music.split()) for music in musics])
    tone = tone_shift()
    for i in range(initial_population.shape[0]):
        initial_population[i]=shift(initial_population[i],-tone[i])
    print(f'loaded musics: {len(initial_population)}')
    
    population = np.tile(initial_population, [int(np.ceil(args.population / len(initial_population)).item()), 1])[:args.population]
    print(f'initial population: {args.population}')
    
    np.save(os.path.join('experiments', args.exp_name, 'initial_population.npy'), population)
    
    # genetic algorithm loop
    
    if os.path.exists(os.path.join('experiments', args.exp_name, 'logs')):
        shutil.rmtree(os.path.join('experiments', args.exp_name, 'logs'))
    os.makedirs(os.path.join('experiments', args.exp_name, 'logs'), exist_ok=True)
    writer = SummaryWriter(log_dir=os.path.join('experiments', args.exp_name, 'logs'))
    
    for step in tqdm(range(1, args.n_iters + 1), desc='surviving'):
        
        # augment population
        augmented_population = np.concatenate([
            population, 
            np.stack([random_operate(codes) for codes in population]), 
        ])
        indices = np.random.permutation(2 * args.population)
        parent1_indices = indices[:args.population]
        parent2_indices = indices[args.population:]
        children = np.stack([crossOver(augmented_population[parent1_indices[index]], augmented_population[parent2_indices[index]]) for index in range(args.population)])
        augmented_population = np.concatenate([augmented_population, children])
        
        # evaluate fitness
        fitness_scores = np.array([fitness_function(codes, initial_parameter) for codes in augmented_population])
        ranks = np.argsort(fitness_scores)
        
        # choose best
        # population = augmented_population[np.random.choice(len(augmented_population), args.population)]
        population = augmented_population[ranks[-args.population:]]
        
        # log fitness
        writer.add_scalar('fitness/fitness', fitness_scores.mean(), step)
    
    # save results
    np.save(os.path.join('experiments', args.exp_name, 'final_population.npy'), population)
