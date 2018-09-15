from .extract import extract_basic_information
from termcolor import colored
import inspect


def module_format(entity):
    type_name, entity_name, entity_docstring = extract_basic_information(entity)

    if entity_docstring:
        entity_docstring = inspect.cleandoc(entity_docstring).splitlines()
        firstline = "{} ...".format(entity_docstring[0])
    else:
        firstline = "no docstring"

    print("{0} {1}: {2}".format(
        type_name,
        entity_name,
        firstline))


def attribute_format(entity):
    type_name, entity_name, entity_docstring = extract_basic_information(entity)

    if entity_docstring is None:
        entity_docstring = "No docstring"

    print("{} {}\n\t{}".format(
        colored(type_name, "green"),
        colored(entity_name, "red"),
        "\n\t".join(inspect.cleandoc(entity_docstring).splitlines())
    ))
    print("")
