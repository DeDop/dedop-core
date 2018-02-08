__author__ = 'DeDop Development Team'


def _fix_46():
    import os.path
    import sys
    # See https://github.com/DeDop/dedop-core/issues/46
    extra_path = os.path.join(sys.prefix, 'site-packages')
    if os.path.isdir(extra_path) and extra_path not in sys.path:
        sys.path.append(extra_path)


_fix_46()
