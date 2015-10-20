class Parameter:
    """
    The Parameter class is used to describe, validate,
     and convert parameter values.
    """

    def __init__(self, name, data_type=None, default_value=None, value_set=None, description=None, units=None):
        self._name = name
        if type(name) != str:
            raise ValueError('"name" must not be None')
        if data_type:
            self._data_type = data_type
        elif default_value:
            self._data_type = type(default_value)
        else:
            raise ValueError('"data_type" must not be None')
        self.default_value = default_value
        self.description = description
        self.units = units
        self.value_set = value_set

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type
