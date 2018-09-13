import os
from glob import glob
from importlib import import_module
from termcolor import colored
import inspect
import types


def module_format(contents):
    contents = map(lambda c: (colored(c[0], "green"), colored(c[1], "red"), c[2]), contents)

    max_type_length = len(max(contents, key=lambda item: len(item[0]))[0]) + 1
    max_name_length = len(max(contents, key=lambda item: len(item[1]))[1]) + 1

    for type_name, name, doc in contents:
        if doc:
            doc = inspect.cleandoc(doc).splitlines()
            docstring = "{} ...".format(doc[0])
        else:
            docstring = "no docstring"

        print("{0:>{type_length}} {1:<{name_length}}: {2}".format(
            type_name,
            name,
            docstring,
            type_length=max_type_length,
            name_length=max_name_length))
    return


def attribute_format(contents):
    for type_name, name, doc in contents:
        print("{} {}\n\t{}".format(
            colored(type_name, "green"),
            colored(name, "red"),
            "\n\t".join(inspect.cleandoc(doc).splitlines())
        ))
        print("")
    return


def extract(module, attribute_filter):
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


def extract_package(package, attribute_filter):
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


def process_attribute(attribute, attribute_filter):
    if (isinstance(attribute, types.FunctionType)
        or isinstance(attribute, types.BuiltinFunctionType)
        or isinstance(attribute, types.MethodType)
        or isinstance(attribute, types.BuiltinMethodType)):
        type_name = type(attribute).__name__
        doc = attribute.__doc__
        if not doc:
            doc = "no docstring"

        return [(type_name, attribute.__name__, doc)]
    elif isinstance(attribute, types.TypeType) or isinstance(attribute, types.ClassType):
        attributes = extract(attribute, attribute_filter)
        return attributes
    elif isinstance(attribute, types.ObjectType):
        attributes = extract(attribute, attribute_filter)
        return attributes
    else:
        return [(type(attribute).__name__, attribute, "no doc")]


def _check_base_classes(_class, _method_name, current, depth):
    if current == depth:
        return _method_name in _class.__dict__

    for base in _class.__bases__:
        if _method_name in base.__dict__:
            return True
        if current < depth and _check_base_classes(base, _method_name, current + 1, depth):
            return True
    return False


def method_filter(item, _class, depth=0):
    return _check_base_classes(_class, item, 0, depth)


def dir_filter(item):
    """
    Accept each item which doesn't start with _
    :type item: str
    :param item: a string item to filter
    :return: true if item doesn't start with _
    """
    return not item.startswith("_")


