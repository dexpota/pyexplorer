from termcolor import colored
import inspect


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
