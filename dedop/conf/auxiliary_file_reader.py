from .auxiliary_errors import *
from .auxiliary_parameter import *

import json
from typing import Any, Sequence
import warnings


class AuxiliaryFileReader:
    """
    class for reading auxiliary files
    """
    # the _id field is the short ID of the file - e.g: CHD, CST ...
    # this is purely used to give context to error & warning messages
    _id = None
    _fileversion = 0


    def __init__(self, filename: str=None, **kwargs: Any):
        """
        The base class for auxiliary files. Reads the JSON data from
         a specified filename, or constructs it from the keyword
         arguments supplied to the constructor.
        """
        # create empty data dictionary
        self._data = {}

        # if a filename has been provided, read the data from the file
        if filename is not None:
            self._data = self._read_file(filename)

        # update the data dict with values from keyword arguments
        self._data.update(kwargs)

    @classmethod
    def _read_file(cls, filename: str) -> None:
        """
        reads JSON data from the specified filename and adds it
         to the data collection of the AuxiliaryFileReader
        """
        data = {}
        # open the JSON doc for reading
        with open(filename) as input_file:
            version = cls.get_version(input_file)

            if version != cls._fileversion:
                raise IncompatibleAuxiliaryFileError(cls._id, cls._fileversion, version)

            # get the data of each item in the JSON doc
            for name, param in json.load(input_file).items():
                # skip the metadata
                if name == "__metainf__":
                    continue
                # check if it's in our array of expected parameters,
                # and throw a warning if it isn't.
                if name not in cls._get_parameters():
                    warnings.warn(
                        UnknownParameterWarning(name, cls._id)
                    )
                # add the item to the dictionary
                data[name] = param['value']
        return data

    @staticmethod
    def get_version(file):
        # read file as JSON
        data = json.load(file)
        # return to start of file
        file.seek(0)

        if "__metainf__" not in data:
            # file predates metadata - version -1
            return -1
        return data["__metainf__"]["version"]

    @classmethod
    def _get_parameters(cls) -> Sequence[str]:
        """
        returns an iterable of all the parameters defined for
         this configuration file - used to check if we should
         warn about using an undefined parameter.
        """
        return (
            item.name for name, item in vars(cls).items() if\
                isinstance(item, AuxiliaryParameter)
        )

    def __getitem__(self, item: str) -> Any:
        """
        returns the value of the specified parameter
        """
        if item in self._get_parameters() and item in self._data:
            return self._data[item]
        raise MissingParameterError(item, self._id)