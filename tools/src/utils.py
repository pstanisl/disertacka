import codecs

def load_file(path, *, encoding='utf-8'):
    """Load raw text content of the file.

    Args:
        path: path to the file
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        str: non empty lines
    """
    with codecs.open(path, encoding=encoding) as input_file:
        for line in input_file.readlines():
            # Remove whitechars, line endings, etc. from the
            # beginning and the end of a line.
            line = line.strip()
            # Skip empty lines.
            if not line:
                continue
            yield line