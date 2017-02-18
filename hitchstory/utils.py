from copy import deepcopy


def to_underscore_style(text):
    """Changes "Something like this" to "something_like_this"."""
    text = text.lower().replace(" ", "_").replace("-", "_")
    return ''.join(x for x in text if x.isalpha() or x.isdigit() or x == "_")


def replace_parameter(thing, param_name, param):
    """
    Replace parameter name in (( and )) with value in step arguments and preconditions.
    """
    if type(thing) is str:
        if "(( {0} ))".format(param_name) in str(thing):
            return thing.replace("(( {0} ))".format(str(param_name)), str(param))
        else:
            return thing
    else:
        if thing.is_sequence():
            new_thing = deepcopy(thing)

            for i, item in enumerate(thing):
                new_thing[i] = replace_parameter(item, param_name, param)

            return new_thing
        elif thing.is_mapping():
            new_thing = deepcopy(thing)

            for key, value in thing.items():
                new_thing[key] = replace_parameter(value, param_name, param)

            return new_thing
        else:
            return replace_parameter(str(thing), param_name, param)
