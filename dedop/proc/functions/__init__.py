import numpy as np
from numpy.linalg import norm

__all__ = ["angle_between"]

def angle_between(vec1, vec2):
    return np.arccos(
        np.dot(vec1, vec2) /
        (norm(vec1) * norm(vec2))
    )
