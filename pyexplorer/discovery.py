from importlib import import_module
from glob import glob
import os


def discovery_package(package, attribute_filter):
    """
    Extract from a package
    :param package:
    :param attribute_filter:
    :return:
    """
    package_path = package.__path__[0]
    modules = glob("{}/*.so".format(package_path)) + glob("{}/*.py".format(package_path))

    contents = []
    for module in modules:
        module_name = os.path.splitext(os.path.basename(module))[0]
        full_module_name = package.__name__ + "." + os.path.splitext(os.path.basename(module))[0]
        try:
            m = import_module(full_module_name)
            type_name = type(m).__name__
            doc = m.__doc__

            if not doc:
                doc = "no docstring"

            if attribute_filter(module_name):
                contents.append((type_name, full_module_name, doc))
        except:
            pass

    return contents


def discovery_module(module, attribute_filter):
    dir_result = dir(module)

    contents = []
    for result in filter(attribute_filter, dir_result):
        obj = getattr(module, result)
        type_name = type(obj).__name__
        doc = obj.__doc__
        if not doc:
            doc = "no docstring"

        contents.append((type_name, result, doc))
    return contents