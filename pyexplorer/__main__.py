from argparse import ArgumentParser
from .interactive import interactive
from .pyexplorer import dir_filter, import_module, process_attribute, attribute_format, module_format, extract, extract_package
import logging
import __builtin__

logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser()
    # noinspection PyTypeChecker
    parser.add_argument("module", type=str, nargs="?", help="Module or package name.")
    parser.add_argument("-a", action="store_true", help="Show everything inside the module/package.")
    # noinspection PyTypeChecker
    parser.add_argument("--level", type=int, default=0, help="List all methods inherited up to this level.")
    parser.add_argument("--debug", action="store_true", default=False, help="Debug mode.")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.module is None:
        logger.debug("module is None, starting interactive session.")
        interactive()
        return

    filters = []
    if not args.a:
        filters.append(dir_filter)

    for i in range(args.module.count(".") + 1):
        try:
            module_package_name = args.module.rsplit('.', i)[0]
            _ = import_module(module_package_name)
            local_path = ".".join(args.module.rsplit('.', i)[1:])
            break
        except ImportError:
            module_package_name = ""
            local_path = ""

    if args.debug:
        assert ".".join(filter(lambda s: s != "", [module_package_name, local_path])) == args.module

    if not module_package_name:
        attribute = getattr(__builtin__, args.module)
        c = process_attribute(attribute, lambda x: all([f(x) for f in filters]))
        formatter = attribute_format
    else:
        pass # try import global_path
        module_package = import_module(module_package_name)
        if not local_path:
            module_package = import_module(module_package_name)

            if hasattr(module_package, "__path__"):
                c = extract_package(module_package)
            else:
                c = extract(module_package, lambda x: all([f(x) for f in filters]))

            formatter = module_format
        else:
            parent_scope = module_package
            for i in range(local_path.count(".") + 1):
                attribute_name = local_path.split(".")[i]
                attribute = getattr(parent_scope, attribute_name)
                parent_scope = attribute

            c = process_attribute(attribute, lambda x: all([f(x) for f in filters]))
            formatter = attribute_format

    formatter(c)


if __name__ == "__main__":
    main()
