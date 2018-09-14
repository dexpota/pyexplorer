from argparse import ArgumentParser
from .interactive import interactive
from .pyexplorer import dir_filter, import_module, process_attribute, attribute_format, module_format, extract, extract_package
from .utilities import find_innermost_module
import logging
import __builtin__

logger = logging.getLogger(__name__)


def parse_args():
    """
    Parse command line arguments
    :return: an object of command line arguments
    """
    parser = ArgumentParser()
    # noinspection PyTypeChecker
    parser.add_argument("module", type=str, nargs="?", help="Module or package name.")
    parser.add_argument("-a", action="store_true", help="Show everything inside the module/package.")
    # noinspection PyTypeChecker
    parser.add_argument("--level", type=int, default=0, help="List all methods inherited up to this level.")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.module is None:
        logger.debug("module is None, starting interactive session.")
        interactive()
        return

    # list of filtering functions
    filters = []
    if not args.a:
        filters.append(dir_filter)

    # <package>.<module>.<function> -> "<package>.<module>", "<function>"
    module_package_name, attribute_name = find_innermost_module(args.module)

    if args.debug:
        assert ".".join(filter(lambda s: s != "", [module_package_name, attribute_name])) == args.module

    if not module_package_name:
        attribute = getattr(__builtin__, args.module)
        c = process_attribute(attribute, lambda x: all([f(x) for f in filters]))
        formatter = attribute_format
    else:
        module_package = import_module(module_package_name)
        if not attribute_name:
            module_package = import_module(module_package_name)

            if hasattr(module_package, "__path__"):
                c = extract_package(module_package, lambda x: all([f(x) for f in filters]))
            else:
                c = extract(module_package, lambda x: all([f(x) for f in filters]))

            formatter = module_format
        else:
            parent_scope = module_package
            for i in range(attribute_name.count(".") + 1):
                attribute_name = attribute_name.split(".")[i]
                attribute = getattr(parent_scope, attribute_name)
                parent_scope = attribute

            c = process_attribute(attribute, lambda x: all([f(x) for f in filters]))
            formatter = attribute_format

    formatter(c)


if __name__ == "__main__":
    main()
