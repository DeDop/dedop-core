import netCDF4 as nc
from collections import OrderedDict
from enum import Enum

class NetCDFWriter:
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
        def __init__(self, name, data_type, dimensions, long_name, fill_value=None, **attrs):
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

        def set_property(self, name, value):
            """
            adds or sets a property

            :param name: the name of the property
            :param value: the value to set
            """
            self.props[name] = value

        def set_properties(self, **props):
            """
            adds or sets multiple properties

            :param props: keyword/value pairs of properties
            """
            self.props.update(props)

        def get_properties(self):
            """
            gets the property keyword arguments needed by the
            createVariable method of a netCDF document

            :return: dictionary of properties
            """
            return self.props.copy()

        def get_attributes(self):
            """
            gets the extra metadata attributes to be set
            by the setncattrs method of a netCDF variable instance

            :return: dictionary of attributes
            """
            return self.attrs.copy()

    def __init__(self, filename):
        """
        initialize the NetCDFWriter instance

        :param filename: the path of the file to write to
        """
        self._root = nc.Dataset(
            filename, 'w', format="NETCDF4"
        )
        self._dimensions = OrderedDict()
        self._variables = OrderedDict()

        self.dimensions = {}
        self.variables = {}

    def __enter__(self):
        """
        enables use of 'with' statements to ensure file
        is closed after operations are performed

        :return: the current document
        """
        return self._root

    def __exit__(self, exc_type, exc_val, exc_tb):
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

    def define_dimension(self, dimension_name, size):
        """
        Add a new dimension to the dimension definitions

        :param dimension_name:
        :param size:
        :return:
        """
        self._dimensions[dimension_name] = size

    def define_variable(self, variable_name, data_type, dimensions, *attr_pairs, **attrs):
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


    def get_dimension_size(self, dimension_name):
        """
        returns the size of the specified dimension

        :param dimension_name: the name of the dimension
        :return: int or None - length of dimension
        """
        return self._dimensions[dimension_name]

    def get_variable_descriptor(self, variable_name):
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

    def create_all_dimensions(self, *only):
        """
        creates all the dimensions specified in the class'
        '_dimensions' field, or only those specified in
        the 'only' argument

        :param only: if present, an iterable of the names of dimensions to create
        :return: an iterable of the dimension objects created
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
                # yield the new dimension object
                yield dim

    def create_all_variables(self, *only):
        """
        creates all the variables specified in the class'
        '_variables' field, or only those specified in the
        'only' argument

        :param only: list of variables to create
        :return: an iterable of the variable objects created
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
                # yield the new variable object
                yield var

    def create_dimension(self, name, size=None):
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

    def create_variable(self, name, variable_description):
        """
        Adds a new variable to the netCDF file

        :param name: the id of the variable
        :param variable_description: the VariableDescriptor instance
        """
        if isinstance(name, Enum):
            str_name = name.value
        else:
            str_name = name

        dimensions = tuple(
            self.dimensions[dim_name].name for
                dim_name in variable_description.dimensions
        )

        var = self._root.createVariable(
            str_name, variable_description.data_type,
            dimensions, **variable_description.get_properties()
        )
        var.setncatts(
            variable_description.get_attributes()
        )

        return var

    def close(self):
        """
        close the netCDF file
        """
        self._root.close()
