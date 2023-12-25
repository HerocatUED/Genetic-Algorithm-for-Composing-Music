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

    return melody_score(music) + chord_score(music, debug_mode=0)*0.5 + rhythm_score(music)


__all__ = [
    'melody_score', 
    'chord_score', 
    'rhythm_score', 
    'fitness_function'
]

classes = __all__