import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QIcon, QKeySequence)

from dedop.gui.mainwindow import MainWindow


def main(args=None):
    if not args:
        args = sys.argv[1:]
    print(">> Welcome to the DeDop GUI! <<")
    print("args =", args)
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

    app = QApplication(args)

    app_icon = QIcon()
    for sz in (16, 24, 32, 48, 64, 128, 256):
        app_icon.addFile('dedop/gui/res/icons/dedop-%s.png' % sz, QSize(sz, sz))
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# check if I'm invoked as script
if __name__ == "__main__":
    main()
