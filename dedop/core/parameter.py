class Parameter:
    """
    The Parameter class is used to describe, validate, and convert parameter values.
    """

    def __init__(self, name,
                 default_value=None,
                 data_type=None,
                 description=None,
                 value_set=None,
                 units=None,
                 position=0):
        self._name = name
        if type(name) != str or len(name) == 0:
            raise ValueError('name must not be None or empty')
        if data_type:
            self._data_type = data_type
        elif default_value is not None:
            self._data_type = type(default_value)
        else:
            raise ValueError('data_type must not be None')
        if not isinstance(self._data_type, type):
            raise ValueError('data_type must be an instance of type')
        self.default_value = default_value
        """ The parameter's default value. Default value is None. """
        self.description = description
        """ The parameter's description. Default value is None. """
        self.value_set = value_set
        """ The parameter's value set. Default value is None. """
        self.is_bound_to_value_set = value_set
        """ True, if the parameter value must be one of the value_set values. Default value is False. """
        self.units = units
        """ The parameter value's physical units. Default value is None. """
        self.position = position
        """ The parameter's position which can be used for sorting if it is a positional value. Default value is 0. """

    @property
    def name(self):
        """ The parameter's name. """
        return self._name

    @property
    def data_type(self):
        """ The parameter's data type. Must be an instance of the type class."""
        return self._data_type

    def __str__(self):
        return self._name

    def __call__(self, annotated_class):
        if 'parameters' not in annotated_class.__dict__:
            annotated_class.parameters = dict()
        annotated_class.parameters[self.name] = self
        return annotated_class

    @staticmethod
    def get_parameter(clazz, name):
        if hasattr(clazz, 'parameters') and name in clazz.parameters:
            return clazz.parameters[name]
        for base in clazz.__bases__:
            parameter = Parameter.get_parameter(base, name)
            if parameter:
                return parameter
        return None

    @staticmethod
    def get_parameters(clazz):
        """
        Get a dictionary that maps names to Parameter descriptors or nested Parameter dictionaries.
        The dictionary is collected from the given clazz' hierarchy.
        Per-class parameter descriptor dictionaries are retrieved by looking up the class attribute
        'parameters' which must be a dictionary if it exists.
        :param clazz: A class
        :return: A dictionary of possibly nested Parameter instances
        """
        return Parameter._collect_parameters_from_class(clazz, dict())

    @staticmethod
    def _collect_parameters_from_class(clazz, parameters):
        if clazz != object:
            for base in clazz.__bases__:
                parameters = Parameter._collect_parameters_from_class(base, parameters)
            if hasattr(clazz, 'parameters'):
                parameters.update(clazz.parameters)
        return parameters
