"""
Experimental code demonstrating how to implemen t a PyQt tree model
"""

from abc import ABCMeta, abstractmethod
import sys

from PyQt5 import QtCore, QtWidgets
import netCDF4


class NcNode(metaclass=ABCMeta):
    def __init__(self, parent_node, element, row_index):
        self._parent_node = parent_node
        self._element = element
        self._row_index = row_index

    def parent(self):
        return self._parent_node

    def element(self):
        return self._element

    def row_index(self):
        return self._row_index

    def child(self, row):
        return None

    def child_count(self):
        return 0

    def column_count(self):
        return 1

    @abstractmethod
    def data(self, column):
        return None


class NcGroupingNode(NcNode):
    def __init__(self, parent_node, element, row_index, grouping_name):
        super().__init__(parent_node, element, row_index)
        self.grouping_name = grouping_name

    def data(self, column):
        return self.grouping_name


class NcAttributesNode(NcGroupingNode):
    def __init__(self, parent_node, element, row_index):
        super().__init__(parent_node, element, row_index, 'Attributes')
        # Lookup attribute names
        self.attribute_names = element.ncattrs()

    def child_count(self):
        return len(self.attribute_names)

    def child(self, row):
        return NcAttributeNode(self, self.element(), row, self.attribute_names[row])


class NcAttributeNode(NcNode):
    def __init__(self, parent_node, element, index, attribute_name):
        super().__init__(parent_node, element, index)
        self.attribute_name = attribute_name

    def column_count(self):
        return 4

    def data(self, column):
        if column == 0:
            return self.attribute_name
        attr = self.element.getncattr(self.attribute_name)
        if column == 1:
            return str(attr.dtype)
        if column == 2:
            return str(attr.dimensions)
        if column == 3:
            return str(attr.getValue()) if attr.size == 1 else '[...]'
        return None


class NcGroupsNode(NcGroupingNode):
    def __init__(self, parent_node, element, index):
        super().__init__(parent_node, element, index, 'Groups')
        self.group_names = [g[0] for g in element.groups]

    def child_count(self):
        return len(self.group_names)

    def child(self, row):
        return NcGroupNode(self, self.element.groups[self.group_names[row]], row)


class NcGroupNode(NcNode):
    def __init__(self, parent_node, group, index):
        super().__init__(parent_node, group, index)

    def data(self, column):
        return self.element().name

    def child_count(self):
        return 3

    def child(self, row):
        if row == 0:
            return NcAttributesNode(self, self.element(), row)
        elif row == 1:
            return NcGroupsNode(self, self.element(), row)
        elif row == 2:
            return NcVariablesNode(self, self.element(), row)
        return None


class NcVariablesNode(NcGroupingNode):
    def __init__(self, parent_node, element, index):
        super().__init__(parent_node, element, index, 'Variables')
        self.variable_names = [v[0] for v in element.variables]

    def child_count(self):
        return len(self.variable_names)

    def child(self, row):
        return NcVariableNode(self, row, self.element().variables[self.variable_names[row]])


class NcVariableNode(object):
    def __init__(self, parent, variable, row):
        self.parent = parent
        self.variable = variable
        self.row = row

    def child_count(self):
        return 0

    def child(self, row):
        # return NcAttributesNode(self, self.element(), row)
        return None

    def column_count(self):
        return 4

    def data(self, column):
        if column == 0:
            return self.variable.name
        elif column == 1:
            return str(self.variable.dtype)
        elif column == 2:
            return str(self.variable.dimensions)
        elif column == 3:
            return str(self.variable.getValue()) if self.variable.size == 1 else '[...]'
        return None

    def row_index(self):
        return self.row

    def parent_node(self):
        return self.parent


class NcDatasetNode(object):
    def __init__(self, parent, dataset):
        self.parent = parent
        self.dataset = dataset
        self.variabes = []
        self.variabe_nodes = []
        row = 0
        for k in dataset.variables:
            v = dataset.variables[k]
            self.variabes.append(v)
            self.variabe_nodes.append(NcVariableNode(self, v, row))
            row += 1

    def column_count(self):
        return 1

    def data(self, column):
        import os
        return os.path.basename(self.dataset.filepath())

    def row_index(self):
        return self.parent.datasets.index(self.dataset)

    def child_count(self):
        return len(self.variabe_nodes)

    def child(self, row):
        return self.variabe_nodes[row]

    def parent_node(self):
        return self.parent


class NcDatasetsNode(object):
    def __init__(self):
        self.datasets = []
        self.dataset_nodes = []

    def add_dataset(self, dataset):
        self.datasets.append(dataset)
        self.dataset_nodes.append(NcDatasetNode(self, dataset))

    def child_count(self):
        return len(self.datasets)

    def child(self, row):
        return self.dataset_nodes[row]

    def column_count(self):
        return 1

    def data(self, column):
        return "Datasets"

    def row_index(self):
        return 0

    def parent_node(self):
        return None


class NcDatasetTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(NcDatasetTreeModel, self).__init__(parent)
        self.root_node = NcDatasetsNode()

    def addDataset(self, dataset):
        # n = len(self.root_node.datasets)
        # self.beginInsertRows(self.index(n, 0), n, n)
        self.root_node.add_dataset(dataset)
        # self.endInsertRows()

    def removeDataset(self, dataset):
        datasets = self.root_node.datasets
        row = datasets.index(dataset)
        if row >= 0:
            self.beginRemoveRows(self.index(row, 0))
            datasets.remove()
            self.endRemoveRows()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if parent.isValid():
            parent_node = parent.internalPointer()
        else:
            parent_node = self.root_node
        child_node = parent_node.child(row)
        if child_node:
            return self.createIndex(row, column, child_node)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        child_node = index.internalPointer()
        parent_node = child_node.parent_node()
        if parent_node == self.root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row_index(), 0, parent_node)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if parent.isValid():
            parent_node = parent.internalPointer()
        else:
            parent_node = self.root_node
        return parent_node.child_count()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.root_node.column_count()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        node = index.internalPointer()
        return node.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        # return self.super().flags(index)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Type"
            elif section == 2:
                return "Dim"
            elif section == 3:
                return "Value"
        return None


def main():
    app = QtWidgets.QApplication(sys.argv)
    model = NcDatasetTreeModel()
    model.addDataset(netCDF4.Dataset('data/S6_P4_SIM_RAW_L1A__20210929T064000_20210929T064019_T02.nc'))
    model.addDataset(netCDF4.Dataset('data/S6_P4_SIM_RMC_L1A__20210929T064000_20210929T064019_T02.nc'))
    view = QtWidgets.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Datsets Tree Model")
    view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    view.setUniformRowHeights(True)
    # view.setHeaderHidden(True)
    view.show()
    sys.exit(app.exec_())


# check if I'm invoked as script
if __name__ == "__main__":
    main()
