import numpy as np
from numpy.linalg import norm


def angle_between(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    get the angle between two vectors
    """
    arg = np.dot(vec1.flat, vec2.flat) /\
          (norm(vec1) * norm(vec2))
    if arg > 1:
        arg = 1

    return np.arccos(arg)
