import numpy as np

from .melody import melody_score
from .chord import chord_score
from .rhythm import rhythm_score


def fitness_function(music: np.array):
    """
    Args:
    music: 2D array
    """
    assert len(np.shape(music)) == 2

    score =  melody_score(music) + chord_score(music, debug_mode=0)*0.5 + rhythm_score(music)
    # out_of_range_mask = (music < 36) | (music > 95)
    # print(out_of_range_mask)
    # out_of_range_mask = np.any(out_of_range_mask)
    # print(out_of_range_mask)
    # score[out_of_range_mask] = 0
    return score


__all__ = [
    'melody_score', 
    'chord_score', 
    'rhythm_score', 
    'fitness_function'
]

classes = __all__