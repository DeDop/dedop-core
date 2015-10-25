import sys

from PyQt5.QtWidgets import QApplication

from dedop.gui.mainwindow import MainWindow


def main(args=None):
    if not args:
        args = sys.argv[1:]
    print(">> Welcome to the DeDop GUI! <<")
    print("args =", args)
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

    app = QApplication(args)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# check if I'm invoked as script
if __name__ == "__main__":
    main()
