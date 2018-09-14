from .extract import extract_module_information, extract_attribute_information
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
            c = extract_module_information(m)

            if attribute_filter(module_name):
                contents.append(c)
        except:
            # todo log this error.
            pass

    return contents


def discovery_module(module, attribute_filter):
    dir_result = dir(module)

    contents = []
    for attribute_name in filter(attribute_filter, dir_result):
        attribute_object = getattr(module, attribute_name)

        c = extract_attribute_information(attribute_object)
        contents.append(c)
    return contents
