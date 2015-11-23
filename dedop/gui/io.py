#!/usr/bin/env python


import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMessageBox)


class IO:
    """
    Support class allowing to easily implement configurable open & save-as file selection actions.
    """

    def __init__(self, parent, fileFilter, lastDirKey):
        """
        Constructor.
        :param parent: The parent widget.
        :param fileFilter: A file filter.
        :param lastDirKey: The key of the user preference that stores the last directory visited.
        :return:
        """
        self.parent = parent
        self.fileFilter = fileFilter
        self.lastDirKey = lastDirKey

    def open(self, openTitle, openAction):
        """
        Bring up a file open dialog.

        :param openTitle: The dialog title
        :param openAction: The action to be performed.
        :return: The selected filename or *None*.
       """
        preferences = self.parent.preferences
        lastDir = preferences.get(self.lastDirKey, '.')
        filename, _ = QFileDialog.getOpenFileName(self.parent, openTitle, lastDir, self.fileFilter)
        if not filename:
            return None

        lastDir = os.path.dirname(filename)
        if lastDir:
            preferences.set(self.lastDirKey, lastDir)

        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            return openAction(filename)
        except IOError as e:
            QMessageBox.warning(self.parent, openTitle,
                                "Cannot open file %s:\n%s." % (filename, str(e.exception)))
            return None
        finally:
            QApplication.restoreOverrideCursor()

    def save(self, saveTitle, saveAction, filename=None):
        """
        Optionally bring up a file save-as dialog and perform the *saveAction*.

        :param saveTitle: The dialog title
        :param saveAction: The save action to be performed.
        :param filename: The initial filename.
        :return: The selected filename or *None*.
        """
        if filename:
            return self._save(saveTitle, saveAction, filename)
        else:
            return self.saveAs(saveTitle, saveAction)

    def saveAs(self, saveTitle, saveAction, filename=None):
        """
        Bring up a file save-as dialog. Loop while user selected an already existing file and rejects to overwrite it.

        :param saveTitle: The dialog title
        :param saveAction: The save action to be performed.
        :param filename: The initial filename.
        :return: The selected filename or *None*.
        """
        cont = True
        while cont:
            preferences = self.parent.preferences
            lastDir = preferences.get(self.lastDirKey, '.')
            filename, _ = QFileDialog.getSaveFileName(self.parent, saveTitle, lastDir, self.fileFilter)
            if not filename:
                return None

            lastDir = os.path.dirname(filename)
            if lastDir:
                preferences.set(self.lastDirKey, lastDir)

            if os.path.isfile(filename):
                reply = QMessageBox.question(self.parent, saveTitle,
                                             "File %s\nalready exists.\nOverwrite it?",
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                             QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    cont = False
                elif reply == QtGui.QMessageBox.Cancel:
                    return None
                else:
                    cont = True
            else:
                cont = False

        return self._save(saveTitle, saveAction, filename)

    def _save(self, saveTitle, saveAction, filename):
        try:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            saveAction(filename)
            return filename
        except IOError as e:
            QMessageBox.warning(self.parent, saveTitle,
                                "Failed to save file %s:\n%s." % (filename, str(e.exception)))
            return None
        finally:
            QApplication.restoreOverrideCursor()
