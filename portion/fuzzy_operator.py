import math
#from .const import inf


__rel_tol__ = 1e-11
__abs_tol__ = 1e-13


def lt(a, b, rel_tol=__rel_tol__, abs_tol=__abs_tol__):
    a, b = float(a), float(b)
    return (a < b) and (not eq(a, b, rel_tol=rel_tol, abs_tol=abs_tol))


def le(a, b, rel_tol=__rel_tol__, abs_tol=__abs_tol__):
    a, b = float(a), float(b)
    return (a < b) or (eq(a, b, rel_tol=rel_tol, abs_tol=abs_tol))


def eq(a, b, rel_tol=__rel_tol__, abs_tol=__abs_tol__):
    a, b = float(a), float(b)
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def ne(a, b, rel_tol=__rel_tol__, abs_tol=__abs_tol__):
    a, b = float(a), float(b)
    return not math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def ge(a, b, rel_tol=__rel_tol__, abs_tol=__abs_tol__):
    a, b = float(a), float(b)
    return (a > b) or (eq(a, b, rel_tol=rel_tol, abs_tol=abs_tol))


def gt(a, b, rel_tol=__rel_tol__, abs_tol=__abs_tol__):
    a, b = float(a), float(b)
    return (a > b) and (not eq(a, b, rel_tol=rel_tol, abs_tol=abs_tol))




"""
# https://github.com/python/cpython/blob/3.8/Lib/operator.py
def lt(a, b):
    "Same as a < b."
    return a < b

def le(a, b):
    "Same as a <= b."
    return a <= b

def eq(a, b):
    "Same as a == b."
    return a == b

def ne(a, b):
    "Same as a != b."
    return a != b

def ge(a, b):
    "Same as a >= b."
    return a >= b

def gt(a, b):
    "Same as a > b."
    return a > b
"""
