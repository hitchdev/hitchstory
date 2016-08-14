def to_underscore_style(text):
    """Changes "Something like this" to "something_like_this"."""
    text = text.lower().replace(" ", "_").replace("-", "_")
    return ''.join(x for x in text if x.isalpha() or x.isdigit() or x == "_")
