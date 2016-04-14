from ...util.parameter import Parameter

@Parameter('n_looks_stack')
@Parameter('zp_fact_range')
class BaseAlgorithm:
    def __init__(self, chd, cst):
        self.chd = chd
        self.cst = cst