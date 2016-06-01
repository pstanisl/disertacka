import codecs


def load_mlf(path, *, encoding='utf-8'):
    """Load and clean mlf file.

    Args:
        path: path to the mlf file
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        tuple: filename + list of words
    """
    with codecs.open(path, encoding=encoding) as mlf_file:
        for line in mlf_file.readlines():
            # Remove white space from the beginning and the end.
            line = line.strip()
            # Skip empty line.
            if not line:
                continue
            # Skip comments.
            if line.startswith('#'):
                continue
            yield line
