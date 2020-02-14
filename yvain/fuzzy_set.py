"""
Fuzzy set abstractions and utilities
"""

from math import ceil
from typing import Callable

from yvain.logical_systems import LogicalSystem, Zadeh
from yvain.membership_functions import MembershipFunction


def _integrate(function: Callable[[float, ], float],
               start: float, end: float, n: int) -> float:
    """
    Calculate defined integral of given `function` in range of
    [start, end]

    :param function: Function to integrate
    :param start: Left bound
    :param end: Right bound
    :param n: Number of parabolas used to compute integral
    :raise ValueError: When n is not even
    :raise ValueError: When start is greater or equal to end
    :return: Field of area under given `function`
    """
    if n % 2 != 0:
        raise ValueError("In Simpson rule n have to be even")
    if start >= end:
        raise ValueError(
            f"Upper bound ({end}) is lesser or equal to lower ({start})")

    step = (end - start) / n

    _sum = function(start) + function(end)
    for i in range(1, n):
        if i % 2 == 0:
            _sum += 2 * function(start + i * step)
        else:
            _sum += 4 * function(start + i * step)

    return (step / 3) * _sum


class FuzzySet:
    """
    Fuzzy set if extension of classical one where each element
    is described by degree of membership instead of classical `member/not a member`
    """

    def membership(self, x: float) -> float:
        """
        Membership describes in what degree given element belongs to fuzzy set.
        When membership is equal to 1 we can say that element is fully member of
        fuzzy set. Analogously when membership is equal to 0 then given element is
        not a member of fuzzy set.

        :param x: We are searching degree of truth of this element
        :return: Degree of membership of given `x`
        """

        return self.membership_function(x)

    def complement(self) -> 'FuzzySet':
        """
        Negation operator. Fuzzy set resulting from this operation will have
        all memberships reversed - i.e. element with full membership will not belong
        to fuzzy set anymore and elements that was previously not in fuzzy set will
        gain full membership. Intermediate memberships will change proportionally

        :return: Complementary fuzzy set where all memberships are reversed
        """

        return FuzzySet(self.logic.complement(self.membership_function),
                        self.logic)

    def intersection(self, other_set: 'FuzzySet') -> 'FuzzySet':
        """
        :param other_set: Second fuzzy set
        :return: Common part of `self` and `other_set`
        """

        return FuzzySet(self.logic.t_norm(self.membership_function, other_set.membership_function),
                        self.logic)

    def union(self, other_set: 'FuzzySet') -> 'FuzzySet':
        """
        :param other_set: Second fuzzy set
        :return: Union of `self` and `other_set`
        """

        return FuzzySet(
            self.logic.t_conorm(self.membership_function, other_set.membership_function),
            self.logic)

    __invert__ = complement
    __or__ = union
    __and__ = intersection

    def __init__(self, membership_function: MembershipFunction,
                 logic: LogicalSystem = Zadeh()):
        """
        :param membership_function: Function describing degree of membership of each element in domain
        :param logic: Norms used to perform intersection, union and negation
        """

        self.membership_function = membership_function
        self.logic = logic


DefuzzificationMethod = Callable[[FuzzySet, float, float], float]


def centroid(fuzzy_set: FuzzySet, start: float, end: float) -> float:
    """
    :param fuzzy_set: Set to defuzzify
    :param start: Universe lowest value
    :param end: Universe highest value
    :return: Center of mass for given fuzzy set
    """

    n = int(ceil(end - start)) * 100

    field = _integrate(fuzzy_set.membership, start, end, n)
    x_field = _integrate(lambda x: x * fuzzy_set.membership(x), start, end, n)

    return x_field / field
