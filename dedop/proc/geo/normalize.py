from dedop.conf import ConstantsFile

def normalize(rads: float, cst: ConstantsFile) -> float:
    """
    limits the value of 'rads' to the range
     -pi <= rads <= pi
    """
    while rads < -cst.pi:
        rads += (2 * cst.pi)
    while rads > cst.pi:
        rads -= (2 * cst.pi)
    return rads
