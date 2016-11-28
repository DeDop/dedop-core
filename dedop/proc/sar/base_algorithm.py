from ...util.parameter import Parameter
from ...conf import ConstantsFile, CharacterisationFile, ConfigurationFile


@Parameter('n_looks_stack', data_type=int)
@Parameter('zp_fact_range', data_type=int)
class BaseAlgorithm:
    """
    The base class from which all other algorithm classes
    inherit properties.

    This class is also used to define configuration
    parameters which are shared between multiple
    algorithms.
    """
    def __init__(self, chd: CharacterisationFile, cst: ConstantsFile, cnf: ConfigurationFile):
        """
        Initialise the BaseAlgorithm instance

        :param chd: the CHD data object
        :param cst: the CST data object
        """
        self.chd = chd
        self.cst = cst
        self.cnf = cnf

        self.collect_parameter_values()

    def collect_parameter_values(self) -> None:
        """
        set CNF parameter values
        """

        for param in Parameter.get_parameters(self.__class__).values():
            if param.value_set is not None:
                setattr(self, param.name, param.value_set)
            try:
                setattr(self, param.name, getattr(self.cnf, param.name))
            except:
                setattr(self, param.name, param.default_value)