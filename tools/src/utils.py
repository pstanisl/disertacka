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


def save_file(path, data, *, encoding='uft-8'):
    """Save items from an iterator into a file. On the end of the
    file is empty line.

    Args:
        path: path to the output file
        data: an iterator with content
        encoding: encoding of the output file
    """
    with codecs.open(path, 'w', encoding=encoding) as target:
        for item in data:
            target.write('{}\n'.format(item))
