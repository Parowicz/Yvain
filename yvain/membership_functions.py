"""
Predefined membership functions. Collection of parametrised functions
greatly simplifies design of fuzzy applications.
"""

from math import exp
from typing import Callable

MembershipFunction = Callable[[float, ], float]


class Triangle:
    """
    For triangular membership function `x` is member of fuzzy set only if
    it's greater than `a` and smaller than `c`. In this function x is fully
    member of fuzzy set only for `x = b`. Each value between `a - b` and `b - c`
    represent partial membership.
    """

    def __call__(self, x: float) -> float:
        if self.a <= x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x <= self.c:
            return (self.c - x) / (self.c - self.b)
        else:
            return 0

    def __init__(self, a: float, b: float, c: float):
        """
        :param a: Left corner of triangle
        :param b: Central corner of triangle
        :param c: Right corner of triangle
        :raise ValueError: if not `a < b < c`
        """
        if not a < b < c:
            raise ValueError(f"a < b < c relationship is not matched for a={a}, b={b}, c={c}")

        self.a: float = a
        self.b: float = b
        self.c: float = c


class Trapezoid:
    """
    For trapezoidal membership function `x` is member of fuzzy set only if
    it's greater than `a` and smaller than `d`. In this function x is fully
    member of fuzzy set when `b <= x <= c`. Each value between `a - b` and `c - d`
    represent partial membership.
    """

    def __call__(self, x: float) -> float:
        if self.a <= x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x <= self.c:
            return 1
        elif self.c <= x <= self.d:
            return (self.d - x) / (self.d - self.c)
        else:
            return 0

    def __init__(self, a: float, b: float, c: float, d: float):
        """
        :param a: Left bottom corner of trapezoid
        :param b: Left top corner of trapezoid
        :param c: Right top corner of trapezoid
        :param d: Right bottom corner of trapezoid
        :raise ValueError: if not `a < b < c < d`
        :return: Trapezoidal function with vertexes at `a, b, c, d`
        """

        if not a < b < c < d:
            raise ValueError(
                f"a < b < c < d relationship is not matched for a={a}, b={b}, c={c}, d={d}")

        self.a = a
        self.b = b
        self.c = c
        self.d = d


class Gaussian:
    """
    Gaussian function with mean = `mu` and standard deviation = `sigma`.
    This function has it center at `mu` and `x = mu` is only point where `x` is
    fully member of fuzzy set. Increasing `sigma` parameter increases width and slope of
    the function.
    """

    def __call__(self, x: float) -> float:
        return exp(-0.5 * (((x - self.mu) / self.sigma) ** 2))

    def __init__(self, mu: float, sigma: float):
        """
        :param mu: Mean, function center
        :param sigma: Standard deviation, width and slope of the function
        """

        self.mu = mu
        self.sigma = sigma


class Bell:
    """
    Generalized bell curve with center at 'mu'. 'sigma' parameter is
    responsible for width of the function and `gamma` is related to
    width of bell plateau
    """

    def __call__(self, x: float) -> float:
        return 1 / (1 + (abs((x - self.mu) / self.sigma) ** (2 * self.gamma)))

    def __init__(self, mu: float, sigma: float, gamma: float):
        """
        :param mu: Function center
        :param sigma: Slope and width of bell
        :param gamma: Slope of bell and width of bell plateau
        """

        self.mu = mu
        self.sigma = sigma
        self.gamma = gamma


class Sigmoid:
    """
    S-shaped function with slope center at 'a'. `b` parameter controls skewness of slope
    and direction of the function.
    When `b < 0` then left side values are fully member of fuzzy set and slope decreases membership to 0.
    When `b > 0` then left side is not member of fuzzy set and slope increases membership to 1.
    """

    def __call__(self, x: float) -> float:
        return 1 / (1 + exp(- self.b * (x - self.a)))

    def __init__(self, a: float, b: float):
        """
        :param a: Center of slope
        :param b: Skewness and direction of slope
        """

        self.a = a
        self.b = b
