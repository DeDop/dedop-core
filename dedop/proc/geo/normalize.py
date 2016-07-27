def normalize(rads, cst):
    while rads < -cst.pi:
        rads += (2 * cst.pi)
    while rads > cst.pi:
        rads -= (2 * cst.pi)
    return rads