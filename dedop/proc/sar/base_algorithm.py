from ...util.parameter import Parameter
from ...conf import chd, cst

@Parameter('n_looks_stack')
@Parameter('zp_fact_range')
class BaseAlgorithm:
    def __init__(self):
        self.chd = chd
        self.cst = cst