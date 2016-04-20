from ...util.parameter import Parameter

@Parameter('n_looks_stack', data_type=float)
@Parameter('zp_fact_range', data_type=float)
class BaseAlgorithm:
    """
    THhe base class from which all other algorithm classes
    inherit properties.

    This class is also used to define configuration
    parameters which are shared between multiple
    algorithms.
    """
    def __init__(self, chd, cst):
        """
        Initialise the BaseAlgorithm instance

        :param chd: the CHD data object
        :param cst: the CST data object
        """
        self.chd = chd
        self.cst = cst