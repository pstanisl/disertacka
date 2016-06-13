import codecs

from json import loads
from os.path import basename, splitext


def clean_mlf_content(content):
    """Clean mlf content line from useless values. Only
    the last value is not useless.

    Args:
        content: string with a part of the mlf content.

    Returns:
        string: cleaned content.

    Examples:
        >>> clean_mlf_content('00 01 A')
        'A'
        >>> clean_mlf_content('B')
        'B'
        >>> clean_mlf_content('')
        ''
    """
    return content.split()[-1] if content else ''


def clean_mlf_key(key):
    """Clean mlf key. In the most cases it is file path in quotes. Method
    returns basename without file extension.

    Args:
        key: string with file path in quotes

    Examples:
        >>> clean_mlf_key('"*/name.ext"')
        'name'
        >>> clean_mlf_key('"*\\\\name"')
        'name'
    """
    # Remove all quotation marks.
    key = loads(key.replace('\\', '/'))
    # Get only end of the path.
    key = basename(key)
    # Remove file extension.
    return splitext(key)[0]


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


def load_mlf(path, *, encoding='utf-8'):
    """Load and clean mlf file.

    Args:
        path: path to the mlf file
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        tuple: filename + list of cleaned content
    """
    key = None
    content = []

    # with codecs.open(path, encoding=encoding) as mlf_file:
    for line in load_file(path, encoding=encoding):
        # Skip comments in mlf file
        if line.startswith('#'):
            continue
        # Get key -> line with file path
        if line.startswith('"'):
            key = clean_mlf_key(line)
            # Skip adding key into content list.
            continue
        # End of a content block in the file.
        if line.startswith('.'):
            yield key, content
            # Reset loaded values.
            content = []
            key = None
            # Continue with next path of the mlf.
            continue
        # Remove useless content.
        line = clean_mlf_content(line)
        # Add content line into the list.
        content.append(line)


def load_mlf_to_dict(path, *, encoding='utf-8'):
    """Load mlf and transform content into dictionary, where
    'key' is and filename from mlf segment and dict values is
    a list with mlf segment content.

    Args:
        path: path to the mlf file
        encoding: encoding of the content in the file (default=utf-8)

    Returns:
        dict: mlf segments
    """
    ret = {}

    for key, content in load_mlf(path, encoding=encoding):
        if (key not in ret):
            ret[key] = []

        ret[key] += content

    return ret
