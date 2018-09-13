from importlib import import_module


def find_innermost_module(full_qualifier):
    """
    This function find the innermost module or package specified inside module_path.

    >>> find_innermost_module("logging.config.fileConfig")
    ('logging.config', 'fileConfig')

    >>> find_innermost_module("logging.config")
    ('logging.config', '')

    >>> find_innermost_module("logging")
    ('logging', '')

    :type full_qualifier: str
    :param full_qualifier: A string representing a package, a module or an attribute inside one of them.
    :return: A tuple where the first element is the module or package name and the second element is an empty string or
    an the attribute name
    """

    module_package = ""
    attribute = ""

    for i in range(full_qualifier.count(".") + 1):
        try:
            module_package = full_qualifier.rsplit('.', i)[0]
            _ = import_module(module_package)
            attribute = ".".join(full_qualifier.rsplit('.', i)[1:])
            break
        except ImportError:
            module_package = ""
            attribute = ""

    return module_package, attribute
