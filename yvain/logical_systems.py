from math import isclose, log
from typing import Optional

from yvain.membership_functions import MembershipFunction


# TODO:
# Hamacher
# Aczel-Alsina
# Sugeno-Weber
# Dubois-Prade
# Yu


class LogicalSystem:
    """
    Logical system describes T-Norm, T-Conorm and negation used in fuzzy set operations.
    Instead of whole sets `LogicalSystem` operates on membership functions.
    """

    def complement(self, membership: MembershipFunction) -> MembershipFunction:
        """
        Strong negation. Fuzzy set resulting from this operation will have
        all memberships reversed - i.e. element with full membership will not belong
        to fuzzy set anymore and elements that was previously not in fuzzy set will
        gain full membership. Intermediate memberships will change proportionally

        :param membership: :math:`\\mu`
        :return: :math:`\\mu\\prime(x)=1 - \\mu(x)`
        """

        return lambda x: 1 - membership(x)

    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        raise NotImplementedError

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        By default t-conorm is defined by they'r correlation with t-norm. For performance and
        precision reasons it should be overridden in subclass (if possible)

        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x) = \\neg(\\mu_1(x) and \\mu_2(x))`
        """

        return self.complement(
            self.t_norm(self.complement(membership_a), self.complement(membership_b)))


class Zadeh(LogicalSystem):
    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x)=min(\\mu_1(x), \\mu2(x))`
        """

        return lambda x: min(membership_a(x), membership_b(x))

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x)=max(\\mu_1(x), \\mu2(x))`
        """

        return lambda x: max(membership_a(x), membership_b(x))


class Drastic(LogicalSystem):
    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x)` = If :math:`\\mu_1(x) = 1`
                 or :math:`\\mu_2(x) = 1` then return 1 else 0
        """

        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            if isclose(a, 1):
                return b
            elif isclose(b, 1):
                return a
            else:
                return 0

        return norm

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x)` = If :math:`\\mu_1(x) = 0`
                 or :math:`\\mu_2(x) = 0` then return 0 else 1
        """

        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            if isclose(a, 0):
                return b
            elif isclose(b, 0):
                return a
            else:
                return 1

        return norm


class Product(LogicalSystem):
    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x) = \\mu_1(x) * \\mu_2(x)`
        """

        return lambda x: membership_a(x) * membership_b(x)

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x) = \\mu_1(x) + \\mu_2(x) - \\mu_1(x) * \\mu_2(x)`
        """

        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            return a + b - a * b

        return norm


class Lukasiewicz(LogicalSystem):
    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x) = max(0, \\mu_1(x)) + \\mu_2(x) - 1)`
        """

        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            return max(0, a + b - 1)

        return norm

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1`
        :param membership_b: :math:`\\mu_2`
        :return: :math:`\\mu\\prime(x) = min(\\mu_1(x)) + \\mu_2(x), 1)`
        """

        return lambda x: min(membership_a(x) + membership_b(x), 1)


class Fodor(LogicalSystem):
    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1(x)`
        :param membership_b: :math:`\\mu_2(x)`
        :return: :math:`\\mu\\prime(x)` = If :math:`\\mu_1(x) + \\mu_2(x) > 1`
                then return :math:`min(\\mu_1(x), \\mu_2(x))` else 0
        """

        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            if a + b > 1:
                return min(a, b)
            else:
                return 0

        return norm

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        """
        :param membership_a: :math:`\\mu_1(x)`
        :param membership_b: :math:`\\mu_2(x)`
        :return: :math:`\\mu\\prime(x)` = If :math:`\\mu_1(x) + \\mu_2(x) < 1`
                then return :math:`max(\\mu_1(x), \\mu_2(x))` else 1
        """

        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            if a + b < 1:
                return max(a, b)
            else:
                return 1

        return norm


class ParametrizedLogicalSystem(LogicalSystem):
    @property
    def p(self):
        return self._p

    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        if self.__logic is not None:
            return self.__logic.t_norm(membership_a, membership_b)
        else:
            return self._t_norm(membership_a, membership_b)

    def t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        if self.__logic is not None:
            return self.__logic.t_conorm(membership_a, membership_b)
        else:
            return self._t_conorm(membership_a, membership_b)

    def _t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        raise NotImplementedError

    def _t_conorm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        return super(ParametrizedLogicalSystem, self).t_conorm(membership_a, membership_b)

    def _inherit_logic(self) -> Optional[LogicalSystem]:
        return None

    def __init__(self, p):
        self._p = p
        self.__logic = self._inherit_logic()


class Frank(ParametrizedLogicalSystem):
    def _t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            pa = (self.p ** a) - 1
            pb = (self.p ** b) - 1
            return log(1 + ((pa * pb) / (self.p - 1)), self.p)

        return norm

    def _inherit_logic(self) -> Optional[LogicalSystem]:
        if self.p < 0:
            raise ValueError("In Frank logic 'p' have to be lesser than 0")

        if self.p == 0:
            return Zadeh()
        elif self.p == 1:
            return Product()
        elif self.p == float("inf"):
            return Lukasiewicz()


class ShweizerSklar(ParametrizedLogicalSystem):
    def _t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            return max(0, ((a ** self.p) + (b ** self.p) - 1)) ** (1 / self.p)

        return norm

    def _inherit_logic(self) -> Optional[LogicalSystem]:
        if self.p == float("-inf"):
            return Zadeh()
        elif self.p == 0:
            return Product()
        elif self.p == float("inf"):
            return Drastic()


class Yager(ParametrizedLogicalSystem):
    def _t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            return max(0, 1 - ((1 - a) ** self.p + (1 - b) ** self.p) ** (1 / self.p))

        return norm

    def _inherit_logic(self) -> Optional[LogicalSystem]:
        if self.p < 0:
            raise ValueError("In Yager logic `p` cannot be lesser than 0")

        if self.p == 0:
            return Drastic()
        elif self.p == float("inf"):
            return Zadeh()


class Dombi(ParametrizedLogicalSystem):
    def _t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        def norm(x):
            a = membership_a(x)
            b = membership_b(x)

            if isclose(a, 0) or isclose(b, 0):
                return 0
            else:
                ap = ((1 / a) - 1) ** self.p
                bp = ((1 / b) - 1) ** self.p
                return 1 / (1 + ((ap + bp) ** (1 / self.p)))

        return norm

    def _inherit_logic(self) -> Optional[LogicalSystem]:
        if self.p < 0:
            raise ValueError("In Dombi logic `p` cannot be lesser than 0")

        if self.p == 0:
            return Drastic()
        elif self.p == float("inf"):
            return Zadeh()
