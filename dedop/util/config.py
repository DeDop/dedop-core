import os.path

DEFAULT_CONFIG_FILE = os.path.join('~', '.dedop', 'config.py')
_LOCAL_CONFIG_FILE = 'dedop-config.py'

_CONFIG = None


def get_config_path(name: str, default=None):
    """
    Get the ``str`` value of the configuration parameter *name* which is expected to be a path.
    Any tilde character '~' in the value will be expanded to the current user's home directory.

    :param name: The name of the configuration parameter.
    :param default: The default value, if *name* is not defined.
    :return: The value
    """
    value = get_config_value(name, default=default)
    return os.path.expanduser(str(value)) if value is not None else None


def get_config_value(name: str, default=None):
    """
    Get the value of the configuration parameter *name*.

    :param name: The name of the configuration parameter.
    :param default: The default value, if *name* is not defined.
    :return: The value
    """
    if not name:
        raise ValueError('name must be given')
    return get_config().get(name, default)


def get_config():
    """
    Get the global DeDop configuration.

    :return: A mutable dictionary containing any Python objects.
    """
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = {}

        default_config_file = os.path.expanduser(DEFAULT_CONFIG_FILE)
        if not os.path.exists(default_config_file):
            try:
                write_default_config_file()
            except (IOError, OSError) as error:
                print('warning: failed to create %s: %s' % (default_config_file, str(error)))

        if os.path.isfile(default_config_file):
            try:
                _CONFIG = read_python_config(default_config_file)
            except Exception as error:
                print('warning: failed to read %s: %s' % (default_config_file, str(error)))

        local_config_file = os.path.expanduser(_LOCAL_CONFIG_FILE)
        if os.path.isfile(local_config_file):
            try:
                local_config = read_python_config(local_config_file)
                _CONFIG.update(local_config)
            except Exception as e:
                print('warning: failed to read %s: %s' % (local_config_file, str(e)))

    return _CONFIG


def read_python_config(file):
    """
    Reads a configuration *file* which may contain any Python code.

    :param file: Either a configuration file path or a file pointer.
    :return: A dictionary with all the variable assignments made in the configuration file.
    """

    fp = open(file, 'r') if isinstance(file, str) else file
    try:
        config = {}
        code = compile(fp.read(), file if isinstance(file, str) else '<NO FILE>', 'exec')
        exec(code, None, config)
        return config
    finally:
        if fp is not file:
            fp.close()


def write_default_config_file() -> str:
    default_config_file = os.path.expanduser(DEFAULT_CONFIG_FILE)
    default_config_dir = os.path.dirname(default_config_file)
    if default_config_dir and not os.path.exists(default_config_dir):
        os.mkdir(default_config_dir)
    with open(default_config_file, 'w') as fp:
        import pkgutil
        template_data = pkgutil.get_data('dedop.util', 'config-template.py')
        text = template_data.decode("utf-8")
        # TODO (forman, 20160727): copy text files so that '\n' is replaced by OS-specific line separator??
        # from io import StringIO
        # sio = StringIO(text)
        # text = sio.readlines()
        # sio.close()
        fp.write(text)
    return default_config_file
