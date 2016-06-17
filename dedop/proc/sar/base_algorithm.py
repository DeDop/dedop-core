from ...util.parameter import Parameter
from ...conf import ConstantsFile, CharacterisationFile


@Parameter('n_looks_stack', default_value=481)
@Parameter('zp_fact_range', default_value=2)
class BaseAlgorithm:
    """
    The base class from which all other algorithm classes
    inherit properties.

    This class is also used to define configuration
    parameters which are shared between multiple
    algorithms.
    """
    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile):
        """
        Initialise the BaseAlgorithm instance

        :param chd: the CHD data object
        :param cst: the CST data object
        """
        self.chd = chd
        self.cst = cst

        self.collect_parameter_values()

    def collect_parameter_values(self) -> None:
        """

        :return:
        """

        for param in Parameter.get_parameters(self.__class__).values():
            if param.value_set is not None:
                setattr(self, param.name, param.value_set)
            else:
                setattr(self, param.name, param.default_value)