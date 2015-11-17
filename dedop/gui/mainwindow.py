import json

import netCDF4
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QIcon, QKeySequence)
from PyQt5.QtWidgets import (QAction, QDockWidget, QTabWidget,
                             QDesktopWidget, QListWidget, QMainWindow, QMessageBox, QTextEdit, QTreeView)

from dedop.gui.io import IO
from dedop.gui.preferences import Preferences

APP_NAME = 'DeDop'
APP_VERSION = '0.1'

APP_TITLE = APP_NAME + ' ' + APP_VERSION


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.preferences = Preferences('gui')
        self.preferences.load()

        self.configDocument = dict()
        self.configFile = None

        self.centralWidget = QTabWidget()
        self.centralWidget.addTab(QTextEdit(), 'Data Browser')
        self.centralWidget.addTab(QTextEdit(), 'Processing')
        self.centralWidget.addTab(QTextEdit(), 'Analysis')
        self.setCentralWidget(self.centralWidget)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        self.setWindowIcon(self.getIcon('dedop-128.png'))

        self.newConfig()

        self.configIO = IO(self, 'DeDop Configurations (*.dedop)', 'last_dirs.config')
        self.productIO = IO(self, 'Altimeter Data Products (*.*)', 'last_dirs.product')

        bounds = self.preferences.get('window.bounds')
        if bounds:
            self.setGeometry(*bounds)
        else:
            self.center()

    def updateTitle(self):
        if self.configFile:
            docName = self.configFile
        else:
            docName = '<not-saved>'
        self.setWindowTitle('%s - %s' % (docName, APP_TITLE))

    def newConfig(self):
        self.configDocument = dict()
        self.configFile = None
        self.updateTitle()

    def closeConfig(self):
        self.configDocument = dict()
        self.configFile = None
        self.updateTitle()

    def openConfigImpl(self, filename):
        with open(filename, 'r') as fp:
            self.configDocument = json.load(fp)
        self.configFile = filename
        self.updateTitle()
        self.statusBar().showMessage("Opened '%s'" % filename, 2000)

    def openConfig(self):
        self.configIO.open(APP_NAME + ' - Open Configuration', self.openConfigImpl)

    def saveConfigImpl(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.configDocument, fp, indent='    ', sort_keys=True)
        self.configFile = filename
        self.updateTitle()
        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def saveConfigAs(self):
        self.configIO.saveAs(APP_NAME + ' - Save Configuration', self.saveConfigImpl, self.configFile)

    def saveConfig(self):
        self.configIO.save(APP_NAME + ' - Save Configuration', self.saveConfigImpl, self.configFile)

    def openDataProductImpl(self, filename):
        self.dataProductsTree.addItem(filename)
        self.statusBar().showMessage("Opened '%s'" % filename, 2000)

    def openDataProduct(self):
        self.productIO.open(APP_NAME + ' - Open Data Product', self.openDataProductImpl)

    def closeDataProduct(self):
        data_products_list = self.dataProductsTree
        items = data_products_list.selectedItems()
        for item in items:
            data_products_list.takeItem(data_products_list.row(item))

    def undo(self):
        pass

    def redo(self):
        pass

    def plugins(self):
        pass

    def help(self):
        pass

    def about(self):
        QMessageBox.about(self, "About %s" % APP_TITLE,
                          "<b>DeDop</b> - A User Configurable Tool for Processing Delay Doppler Altimeter Data.\n"
                          + "DeDop stands for <b>De</b>lay <b>Do</b>ppler (Altimeter) <b>P</b>rocessor.")

    def showMatplotlibFigure(self):
        import dedop.gui.mpinteg as mpinteg
        dialog = mpinteg.Window(self)
        dialog.show()

    def createActions(self):
        self.newConfigAction = QAction(self.getIcon('actions/document-new.svg'), "&New Configuration",
                                       self, shortcut=QKeySequence.New,
                                       statusTip="Create a new configuration", triggered=self.newConfig)

        self.openConfigAction = QAction(self.getIcon('actions/document-open.svg'), "&Open Configuration...", self,
                                        shortcut=QKeySequence.Open,
                                        statusTip="Open a configuration", triggered=self.openConfig)

        self.saveConfigAction = QAction(self.getIcon('actions/document-save.svg'), "&Save Configuration", self,
                                        shortcut=QKeySequence.Save,
                                        statusTip="Save the current configuration", triggered=self.saveConfig)

        self.saveConfigAsAction = QAction(self.getIcon('actions/document-save-as.svg'), "Save Configuration &As...",
                                          self,
                                          shortcut=QKeySequence.SaveAs,
                                          statusTip="Save the current configuration with a new name",
                                          triggered=self.saveConfigAs)

        self.closeConfigAction = QAction("&Close Configuration",
                                         self,
                                         shortcut=QKeySequence.Close,
                                         statusTip="Close the current configuration",
                                         triggered=self.closeConfig)

        self.openDataProductAction = QAction("&Open Altimeter Data Product...", self,
                                             shortcut="Ctrl+Shift+O",
                                             statusTip="Open an altimeter data product", triggered=self.openDataProduct)

        self.closeDataProductAction = QAction("&Close Altimeter Data Product", self,
                                              shortcut="Ctrl+Shift+C",
                                              statusTip="Closes the selected altimeter data product",
                                              triggered=self.closeDataProduct)

        self.undoAction = QAction(self.getIcon('actions/edit-undo.svg'), "&Undo", self,
                                  shortcut=QKeySequence.Undo,
                                  statusTip="Undo the last editing action", triggered=self.undo)

        self.redoAction = QAction(self.getIcon('actions/edit-redo.svg'), "&Redo", self,
                                  shortcut=QKeySequence.Redo,
                                  statusTip="Redo the last editing action", triggered=self.redo)

        self.quitAction = QAction("&Quit", self, shortcut="Ctrl+Q",
                                  statusTip="Quit the application", triggered=self.close)

        self.matplotlibAction = QAction("&Matplotlib Example...", self,
                                        shortcut="Ctrl+M",
                                        statusTip="Open a dialog displaying a matplotlib figure",
                                        triggered=self.showMatplotlibFigure)

        self.pluginsAction = QAction(self.getIcon('apps/system-software-update.svg'), "&Plugins...", self,
                                     shortcut="Ctrl+P",
                                     statusTip="Open the application's plugin manager", triggered=self.plugins)

        self.helpAction = QAction(self.getIcon('apps/help-browser.svg'), "&Help Topics", self,
                                  statusTip="Launch the online Help System",
                                  triggered=self.help)

        self.aboutAction = QAction("&About DeDop", self,
                                   statusTip="Show the application's About box",
                                   triggered=self.about)

    @staticmethod
    def getIcon(name):
        return QIcon('dedop/gui/res/icons/' + name)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newConfigAction)
        self.fileMenu.addAction(self.openConfigAction)
        self.fileMenu.addAction(self.saveConfigAction)
        self.fileMenu.addAction(self.saveConfigAsAction)
        self.fileMenu.addAction(self.closeConfigAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openDataProductAction)
        self.fileMenu.addAction(self.closeDataProductAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.toolsMenu.addAction(self.matplotlibAction)
        self.toolsMenu.addAction(self.pluginsAction)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.helpAction)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutAction)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newConfigAction)
        self.fileToolBar.addAction(self.openConfigAction)
        self.fileToolBar.addAction(self.saveConfigAction)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.undoAction)
        self.editToolBar.addAction(self.redoAction)

        self.helpToolBar = self.addToolBar("Help")
        self.helpToolBar.addAction(self.helpAction)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        from dedop.gui.nctreemodel import NcDatasetTreeModel
        self.dataProductsTreeModel = NcDatasetTreeModel()

        testFiles = ['data/S6_P4_SIM_RAW_L1A__20210929T064000_20210929T064019_T02.nc',
                     'data/S6_P4_SIM_RMC_L1A__20210929T064000_20210929T064019_T02.nc']
        for f in testFiles:
            import os
            if os.path.exists(f):
                self.dataProductsTreeModel.addDataset(netCDF4.Dataset(f))

        dock = QDockWidget("Data Products", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dataProductsTree = QTreeView(dock)
        self.dataProductsTree.setModel(self.dataProductsTreeModel)
        dock.setWidget(self.dataProductsTree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Layers", self)
        self.layersList = QListWidget(dock)
        self.layersList.addItems([])
        dock.setWidget(self.layersList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        dock.setVisible(False)

        dock = QDockWidget("Output", self)
        self.outputTextEdit = QTextEdit()
        dock.setWidget(self.outputTextEdit)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        dock.setVisible(False)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            bounds = self.frameGeometry()
            self.preferences.set('window.bounds', [bounds.x(), bounds.y(), bounds.width(), bounds.height()])
            self.preferences.store()
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
