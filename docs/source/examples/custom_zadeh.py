from yvain.logical_systems import LogicalSystem
from yvain.membership_functions import MembershipFunction


class MyZadeh(LogicalSystem):
    def t_norm(self, membership_a: MembershipFunction, membership_b: MembershipFunction) \
            -> MembershipFunction:
        return lambda x: min(membership_a(x), membership_b(x))
