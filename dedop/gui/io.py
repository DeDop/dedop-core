#!/usr/bin/env python


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMessageBox)
import os

class IO:
    def __init__(self, parent, fileFilter, lastDirKey):
        self.parent = parent
        self.fileFilter = fileFilter
        self.lastDirKey = lastDirKey

    def open(self, openTitle, openAction):
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
            openAction(filename)
        except IOError as e:
            QMessageBox.warning(self.parent, openTitle,
                                "Cannot open file %s:\n%s." % (filename, str(e.exception)))
        finally:
            QApplication.restoreOverrideCursor()

    def save(self, saveTitle, saveAction, filename=None):
        if filename:
            self._save(saveTitle, saveAction, filename)
        else:
            self.saveAs(saveTitle, saveAction)

    def saveAs(self, saveTitle, saveAction, filename=None):
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
