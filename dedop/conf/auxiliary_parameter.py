from .auxiliary_errors import *
import numpy as np


class AuxiliaryParameter:
    """
    this is a variable descriptor class. It exists to link
    internal auxiliary parameter names with those used in the
    JSON documents.

    This also enables the code in the AuxiliaryFileReader base
    class to distinguish easily which members of the child classes
    that define parameters - this allows us to e.g: throw a warning
    if an input file defines an unexpected parameter
    """
    def __init__(self, parameter_name: str, doc_string: str=None, param_type: type=None,
                 cast_type=None, optional: bool=False, default_value=None):
        """
        create a new parameter definition.
         parameter_name is the name of the value in the JSON document
        """
        self.name = parameter_name
        if doc_string is not None:
            self.__doc__ = doc_string
        self.type = param_type
        if cast_type is not None:
            self.cast = cast_type
        elif self.type is not None:
            self.cast = self.type
        else:
            self.cast = None

        self.optional = optional or (default_value is not None)
        self.default = default_value
        self._cache = {}

    def __get__(self, instance: "AuxiliaryFileReader", instance_type: type=None):
        """
        if the AuxiliaryParameter is accessed as a member of an
         instance, this method will return the value of the parameter
         it represents.
        if this is accessed from a class rather than an instance, then
         it returns itself. This is similar to the behaviour of the
         built-in @parameter decorator class.
        """
        if instance is None:
            return self

        if instance in self._cache:
            return self._cache[instance]

        value = self._retreive_value(instance)

        if self.cast is not None and value is not None:
            value = self.cast(value)

        if self.type is not None and not isinstance(value, self.type):
            raise ParameterTypeError(self.name, self.type, type(value))

        self._cache[instance] = value
        return value

    def _retreive_value(self, instance):
        """
        retrieves the value of the parameter from the parent
         AuxiliaryFileReader instance.
        """
        try:
            return instance[self.name]
        except MissingParameterError:
            if self.optional:
                return self.default
            raise


class AuxiliaryParameterArray(AuxiliaryParameter):
    """
    converts a list of values in an auxiliary JSON file into a numpy array
    """
    def __init__(self, parameter_name: str, doc_string: str=None, param_type: type=None,
                 shape=None, optional: bool=False, default_value=None):
        """
        create a new parameter definition.
         parameter_name is the name of the value in the JSON document
        """
        self.name = parameter_name
        if doc_string is not None:
            self.__doc__ = doc_string
        self.type = param_type
        self.shape = shape
        if self.type is not None:
            self.cast = self.type
        else:
            self.cast = None

        self.optional = optional or (default_value is not None)
        self.default = default_value

    def __get__(self, instance: "AuxiliaryFileReader", instance_type: type=None):
        """
        if the AuxiliaryParameter is accessed as a member of an
         instance, this method will return the value of the parameter
         it represents.
        if this is accessed from a class rather than an instance, then
         it returns itself. This is similar to the behaviour of the
         built-in @parameter decorator class.
        """
        if instance is None:
            return self

        value = self._retreive_value(instance)

        if value is not None:
            value = np.asarray(value, dtype=self.type)
            if self.shape is not None:
                value = np.reshape(value, self.shape)

        return value
