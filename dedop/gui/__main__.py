import sys


def _main(args=None):
    if not args:
        args = sys.argv[1:]
    print(">> Welcome to the DeDop GUI! <<")
    print("args =", args)
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.


# check if I'm invoked as script
if __name__ == "__main__":
    _main()
