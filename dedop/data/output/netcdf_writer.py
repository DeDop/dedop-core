import netCDF4 as nc
from collections import OrderedDict
from enum import Enum
import os
import numpy as np

from typing import Sequence, Tuple, Any, Union, Dict
from abc import ABCMeta, abstractmethod
from ...version import __version__


Name = Union[str, Enum]


class NetCDFWriter(metaclass=ABCMeta):
    """
    base class for writing output netCDF files
    """

    class VariableDescriptor:
        """
        an instance of this class describes the dimensions and
        properties of a variable to be written to a netCDF file.

        this class is used by NetCDFWriters to create the
        variable instances
        """
        def __init__(self, name: str, data_type: type, dimensions: Sequence[int],
                     long_name: str, fill_value: Any=None, **attrs: Any):
            """
            :param name: the short id of the variable
            :param data_type: the output data format
            :param dimensions: the dimensions of the variable
            :param long_name: the long name of the variable
            :param fill_value: optional default value for unspecified indices
            :param attrs: any extra metadata attributes to create
            """
            # set compulsory netcdf properties
            self.name = name
            self.data_type = data_type
            self.dimensions = dimensions

            # set netcdf attributes
            self.attrs = attrs
            # long_name is entered as an attribute, so we add it to the dict
            self.attrs["long_name"] = long_name

            # set properties
            self.props = {}
            if fill_value is not None:
                self.props["fill_value"] = fill_value

        def set_property(self, name: str, value: Any) -> None:
            """
            adds or sets a property

            :param name: the name of the property
            :param value: the value to set
            """
            self.props[name] = value

        def set_properties(self, **props: Any) -> None:
            """
            adds or sets multiple properties

            :param props: keyword/value pairs of properties
            """
            self.props.update(props)

        def get_properties(self) -> Dict[str, Any]:
            """
            gets the property keyword arguments needed by the
            createVariable method of a netCDF document

            :return: dictionary of properties
            """
            return self.props.copy()

        def get_attributes(self) -> Dict[str, Any]:
            """
            gets the extra metadata attributes to be set
            by the setncattrs method of a netCDF variable instance

            :return: dictionary of attributes
            """
            return self.attrs.copy()

    def __init__(self, filename: str):
        """
        initialize the NetCDFWriter instance

        :param filename: the path of the file to write to
        """

        self._file_path = filename

        folder = os.path.dirname(filename)
        os.makedirs(folder, exist_ok=True)

        self._root = nc.Dataset(filename, 'w', format="NETCDF4")

        self._dimensions = OrderedDict()
        self._variables = OrderedDict()

        self.dimensions = {}
        self.variables = {}
        self.output_index = 0

        # TODO (forman, 20160715): add standard metadata attributes here
        # see http://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html#_attributes
        # some of these attributes may be user-defined and put in a configuration file (CNF?):
        # e.g. 'title', 'institution', 'source', 'references', and 'comment'.

        # added by forman 20160715
        self._root.software_name = 'dedop'
        self._root.software_version = __version__

    @property
    def file_path(self):
        return self._file_path

    def __enter__(self):
        """
        enables use of 'with' statements to ensure file
        is closed after operations are performed

        :return: the current document
        """
        self.output_index = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        called at the end of a with statement, regardless of
        an errors raised inside the block. ensures the file
        is closed

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.close()

    def define_dimension(self, dimension_name: Name, size: int=None) -> None:
        """
        Add a new dimension to the dimension definitions

        :param dimension_name:
        :param size:
        :return:
        """
        self._dimensions[dimension_name] = size

    def define_variable(self, variable_name: Name, data_type: type, dimensions: Sequence[int],
                        *attr_pairs: Tuple[str, Any], **attrs: Any) -> None:
        """
        Add a new variable to the variable definitions

        :param variable_name:
        :param data_type:
        :param dimensions:
        :param attrs:
        :return:
        """
        pairs = [
            ('data_type', data_type),
            ('dimensions', dimensions)
        ] + list(attr_pairs)
        self._variables[variable_name] = OrderedDict(
            pairs
        )
        self._variables[variable_name].update(attrs)


    def get_dimension_size(self, dimension_name: Name) -> int:
        """
        returns the size of the specified dimension

        :param dimension_name: the name of the dimension
        :return: int or None - length of dimension
        """
        return self._dimensions[dimension_name]

    def get_variable_descriptor(self, variable_name: Name) -> VariableDescriptor:
        """
        return the variable descriptor instance for
        the specified variable

        :param variable_name: the name of the variable
        :return: a VariableDescriptor instance
        """
        # get variable info
        data = self._variables[variable_name]
        # get data type and dimensions
        dtype = data.pop("data_type")
        dims = data.pop("dimensions")
        long = data.pop("long_name", None)

        # get variable properties if any are defined
        props = data.pop("properties", None)

        # create variable descriptor instance
        desc = self.VariableDescriptor(
            variable_name, dtype, dims, long,
            **data
        )
        # set properties if any were defined
        if props is not None:
            desc.set_properties(**props)

        # return the variable descriptor
        return desc

    def open(self):
        """
        create the dimensions & variables, and reset the record index
        :return:
        """
        self.create_all_dimensions()
        self.create_all_variables()

        self.output_index = 0



    def create_all_dimensions(self, *only: Name) -> None:
        """
        creates all the dimensions specified in the class'
        '_dimensions' field, or only those specified in
        the 'only' argument

        :param only: if present, an iterable of the names of dimensions to create
        """
        for dim_name in self._dimensions:
            # check if dimension is required
            if not only or dim_name in only:
                # get size of dimension
                size = self.get_dimension_size(dim_name)

                # create dimension
                dim = self.create_dimension(
                    dim_name, size
                )
                # set attribute
                setattr(self, dim.name, dim)

    def create_all_variables(self, *only: Name) -> None:
        """
        creates all the variables specified in the class'
        '_variables' field, or only those specified in the
        'only' argument

        :param only: list of variables to create
        """
        for var_name in self._variables:
            # check if the variable is required
            if not only or var_name in only:
                # get the variable properties
                desc = self.get_variable_descriptor(var_name)

                # create the variable
                var = self.create_variable(
                    var_name, desc
                )
                # set attribute
                setattr(self, var.name, var)

    def create_dimension(self, name: Name, size: int=None) -> nc.Dimension:
        """
        Add a new dimension to the netCDF file

        :param name: the name of the dimension to create
        :param size: the length of the dimension (unlimited if None)
        :return: the netcdf dimension object
        """
        if isinstance(name, Enum):
            str_name = name.value
        else:
            str_name = name

        dim = self._root.createDimension(str_name, size)

        self.dimensions[name] = dim

        return dim

    def create_variable(self, name: Name, variable_description: VariableDescriptor) -> nc.Variable:
        """
        Adds a new variable to the netCDF file

        :param name: the id of the variable
        :param variable_description: the VariableDescriptor instance
        """
        if isinstance(name, Enum):
            str_name = name.value
        else:
            str_name = name

        # convert the list of dimension Enum instances from the
        # VariableDescription into the names of the Dimension objects
        # from the root document.
        dimensions = tuple(
            self.dimensions[dim_name].name for
                dim_name in variable_description.dimensions
        )
        # create a new variable in the root document. The constructor
        # doesn't let us set attributes here, we have to do that below.
        var = self._root.createVariable(
            str_name, variable_description.data_type,
            dimensions, **variable_description.get_properties()
        )
        # get the dict of attributes
        attdict = variable_description.get_attributes()

        for name, value in attdict.items():
            # check if the variable is a tuple of strings - we use these for
            # options such as 'flag_meaning'.
            # if it is, we need to concatenate it with separating
            # spaces. otherwise, the parser will concatenate it
            # without.
            if isinstance(value, tuple) and any(isinstance(item, str) for item in value):
                value = " ".join(value)

            # here we check if the attribute is a string, and if so
            # we encode it into bytes representation. This is because
            # otherwise netCDF4 will write it as a string-format
            # attribute, which isn't supported by some older netCDF parsers.
            if isinstance(value, str):
                value = value.encode()
            var.setncattr(name, value)

        return var

    def close(self) -> None:
        """
        close the netCDF file
        """
        self._root.close()

    def get_variable(self, varname: str) -> nc.Variable:
        return getattr(self, varname)

    @abstractmethod
    def write_record(self, **record_values: Any) -> None:
        """
        writes values to the output file

        :param record_values:
        """
        for varname, value in record_values.items():
            var = self.get_variable(varname)
            ndims = len(var.shape)

            if value is None:
                continue
            try:
                if ndims == 3:
                    dim_1, dim_2 = value.shape
                    var[self.output_index, :dim_1, :dim_2] = value[:, :]
                elif ndims == 2:
                    var[self.output_index, :len(value)] = value[:]
                elif ndims == 1:
                    var[self.output_index] = value
                else:
                    raise WriteError("Number of dimensions not supported", value.shape)
            except Exception as err:
                raise WriteError(
                    "error while writing {} at index {}".format(
                        varname, self.output_index
                    ),
                    err
                )

        self.output_index += 1

    def write_globals(self, **global_attrs) -> None:
        """
        write values of global attributes to the netCDF file
        """
        for global_name, value in global_attrs.items():
            self.write_global(global_name, value)

    def write_global(self, global_name: str, value: str=None) -> None:
        if value is None:
            value = 'Not available'
        self._root.setncattr(global_name, value)


class WriteError(Exception):
    def __init__(self, desc: str, child: Exception):
        self.desc = desc
        self.child = child

    def __repr__(self) -> str:
        return "{}:\n{}".format(self.desc, self.child)
