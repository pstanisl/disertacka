from os.path import abspath, dirname, join
import sys
# Get SRC directory path.
SRC_DIR = abspath(join(dirname(__file__), '..'))
# Add src dir into PATHs.
sys.path.append(SRC_DIR)
