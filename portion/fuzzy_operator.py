import math


class FuzzyOperator:
    def __init__(self,rel_tol=0.0, abs_tol=0.0):
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def lt(self,a, b):
        return (a < b) and (not self.eq(a, b))


    def le(self,a, b):
        return (a < b) or (self.eq(a, b))


    def eq(self,a, b):
        return math.isclose(a, b, rel_tol=self.rel_tol, abs_tol=self.abs_tol)


    def ne(self,a, b):
        return not math.isclose(a, b, rel_tol=self.rel_tol, abs_tol=self.abs_tol)


    def ge(self,a, b):
        return (a > b) or (self.eq(a, b))


    def gt(self,a, b):
        return (a > b) and (not self.eq(a, b))


class ClassicOperator:
    # https://github.com/python/cpython/blob/3.8/Lib/operator.py
    @staticmethod
    def lt(a, b):
        "Same as a < b."
        return a < b

    @staticmethod
    def le(a, b):
        "Same as a <= b."
        return a <= b

    @staticmethod
    def eq(a, b):
        "Same as a == b."
        return a == b

    @staticmethod
    def ne(a, b):
        "Same as a != b."
        return a != b

    @staticmethod
    def ge(a, b):
        "Same as a >= b."
        return a >= b

    @staticmethod
    def gt(a, b):
        "Same as a > b."
        return a > b
