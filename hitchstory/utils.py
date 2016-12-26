def to_underscore_style(text):
    """Changes "Something like this" to "something_like_this"."""
    text = text.lower().replace(" ", "_").replace("-", "_")
    return ''.join(x for x in text if x.isalpha() or x.isdigit() or x == "_")


def replace_parameter(precondition, param_name, param):
    if type(precondition) is list:
        return [replace_parameter(item, param_name, param) for item in precondition]
    elif type(precondition) is dict:
        return {key: replace_parameter(value, param_name, param) for key, value in precondition.items()}
    elif type(precondition) is str:
        if "(( {0} ))".format(param_name) in precondition:
            return precondition.replace("(( {0} ))".format(param_name), param)
        else:
            return precondition
    else:
        return precondition
