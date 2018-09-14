

def extract_module_information(module):
    type_name = type(module).__name__
    module_name = module.__name__
    doc = module.__doc__

    if not doc:
        doc = "no docstring"

    return type_name, module_name, doc


def extract_attribute_information(attribute):
    type_name = type(attribute).__name__
    attribute_name = attribute.__name__
    doc = attribute.__doc__

    if not doc:
        doc = "no docstring"

    return type_name, attribute_name, doc
