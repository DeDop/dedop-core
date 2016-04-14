from ...util.parameter import Parameter

@Parameter('n_looks_stack', data_type=float)
@Parameter('zp_fact_range', data_type=float)
class BaseAlgorithm:
    def __init__(self, chd, cst):
        self.chd = chd
        self.cst = cst