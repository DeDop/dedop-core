class UnknownParameterWarning(Warning):
    def __init__(self, parameter: str, file: str=None):
        """
        create a new UnknownParameterWarning

        this class should be used when an AUX file contains a
         definition for a parameter that is not expected to
         exist in the file.
        """
        # construct the message string
        message =\
            "{} file contains unknown parameter: {}".format(file, parameter)
        # init. base class Warning with message
        super().__init__(message)


class MissingParameterError(Exception):
    def __init__(self, parameter: str, file: str=None):
        """
        create a new MissingParameterError

        this class should be used when trying to read an AUX
         parameter that does not exist inside the specified file.
        """
        # construct the message string
        message = \
            "{} file does not contain a definition for parameter: {}".format(file, parameter)
        # init. base class Exception with message
        super().__init__(message)


class ParameterTypeError(TypeError):
    def __init__(self, parameter: str, expected_type: type, actual_type: type):
        """
        create a new ParameterTypeError

        used to indicate that the value of parameter did
         not match its expected type
        """
        # create message string
        message = \
            "Incorrect type: expected type of {} is {} (got {})".format(
                parameter, expected_type, actual_type
            )
        # init TypeError
        super().__init__(message)


class IncompatibleAuxiliaryFileError(Exception):
    def __init__(self, file: str, expected_version: float, actual_version: float):
        """
        create a new IncompatibleAuxiliaryFileError

        used to indicate that the file selected is not compatible
          with the current version of DeDop
        """
        # create version text
        if actual_version < 0:
            version = "an unknown version"
        else:
            version = "version {}".format(actual_version)
        # create message
        message = \
            "The file \"{}\" is {} which is not compatible with the current version ({})\n" \
            "  Use the command \"dedop config upgrade\" to update to the current version.".format(
                file, version, expected_version
            )
        # init with message
        super().__init__(message)