from ruamel.yaml.comments import CommentedMap, CommentedSeq


def to_underscore_style(text):
    """Changes "Something like this" to "something_like_this"."""
    text = text.lower().replace(" ", "_").replace("-", "_")
    return ''.join(x for x in text if x.isalpha() or x.isdigit() or x == "_")


def replace_parameter(thing, param_name, param):
    """
    Replace parameter name in (( and )) with value in step arguments and preconditions.
    """
    if type(thing) is list or type(thing) is CommentedSeq:
        return [replace_parameter(item, param_name, param) for item in thing]
    elif type(thing) is dict or type(thing) is CommentedMap:
        return {
            key: replace_parameter(value, param_name, param)
            for key, value in thing.items()
        }
    elif type(thing) is str:
        if "(( {0} ))".format(param_name) in thing:
            return thing.replace("(( {0} ))".format(param_name), param)
        else:
            return thing
    else:
        return thing
