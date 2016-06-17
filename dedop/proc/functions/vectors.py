import numpy as np
from numpy.linalg import norm


def angle_between(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return np.arccos(
        np.dot(vec1, vec2) /
        (norm(vec1) * norm(vec2))
    )[0, 0]
