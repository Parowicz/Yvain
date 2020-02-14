from yvain.logical_systems import *
from yvain.membership_functions import Triangle
import pytest

_TRIANGLE_UNIVERSE = [
    Triangle(0, 5, 10),
    Triangle(5, 10, 15),
    Triangle(10, 15, 20)
]

_LOGICS = [
    Zadeh(), Drastic(), Product(), Lukasiewicz(), Fodor(),
    Frank(2), ShweizerSklar(2), Yager(2), Dombi(2)
]


@pytest.mark.parametrize("logic", _LOGICS)
def test_demorgan_triple(logic):
    ors = _TRIANGLE_UNIVERSE[0]
    ands = logic.complement(_TRIANGLE_UNIVERSE[0])

    for mf in _TRIANGLE_UNIVERSE[1:]:
        ors = logic.t_conorm(ors, mf)
        ands = logic.t_norm(ands, logic.complement(mf))

    ors = logic.complement(ors)

    for i in range(20):
        assert ands(i) == pytest.approx(ors(i))


@pytest.mark.parametrize("logic", _LOGICS)
def test_sum_of_fx_and_complemented_fx_should_be_equal_to_one(logic):
    for mf in _TRIANGLE_UNIVERSE:
        complement_mf = logic.complement(mf)

        for i in range(20):
            assert (mf(i) + complement_mf(i)) == pytest.approx(1)
