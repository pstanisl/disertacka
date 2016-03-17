from __future__ import print_function

import time

from functools import wraps
from numba import jit


# @jit
@jit(nogil=True)
# @jit(nopython=True, cache=True)
def get_index(l, x):
    """Get index of an item `x` in the list `l`. If the
    item is not in the list return `-1`.

    Examples:
        >>> l = [1, 2, 3, 4]
        >>> get_index(l, 1)
        0
        >>> get_index(l, 5)
        -1
    """
    return l.index(x) if x in l else -1


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('Total time running {}: {:.4f} seconds'.format(
            function.func_name, t1 - t0 ))
        return result
    return function_timer
