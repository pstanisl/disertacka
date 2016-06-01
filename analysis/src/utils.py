import codecs

from json import loads
from os.path import basename, splitext


def clean_mlf_content(content):
    return content.split()[-1] if content else ''


def clean_mlf_key(key):
    # Remove all quotation marks.
    key = loads(key)
    # Get only end of the path.
    key = basename(key)
    # Remove file extension.
    return splitext(key)[0]


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

    with codecs.open(path, encoding=encoding) as mlf_file:
        for line in mlf_file.readlines():
            # Remove white space from the beginning and the end.
            line = line.strip()
            # Skip empty line or comments.
            if not line or line.startswith('#'):
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
