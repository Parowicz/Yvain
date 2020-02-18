import pytest

from yvain.fuzzy_set import FuzzySet
from yvain.fuzzy_system import MamdaniSystem, when, FuzzyVariable
from yvain.membership_functions import Gaussian, Trapezoid, Triangle


def test_when_then_rule_cuts_output_at_input_membership():
    small_mf = Gaussian(150, 4)
    cheap_center = 175
    cheap_mf = Triangle(150, cheap_center, 200)
    input_variable = FuzzyVariable("size", {
        "small": FuzzySet(small_mf),
        "large": FuzzySet(Gaussian(180, 4))
    })
    output_variable = FuzzyVariable("clothing cost", {
        "cheap": FuzzySet(cheap_mf),
        "expansive": FuzzySet(Triangle(200, 250, 400))
    })

    rule = when("size", "small").then("clothing cost", "cheap").compile({
        "size": input_variable}, {"clothing cost": output_variable})

    assert rule({"size": 150}).membership(cheap_center) == pytest.approx(small_mf(150))
    assert rule({"size": 20}).membership(cheap_center) == pytest.approx(small_mf(20))
    assert rule({"size": 140}).membership(cheap_center) == pytest.approx(small_mf(140))


def test_r_sets_example():
    #  R Sets is R library

    system = MamdaniSystem.empty()
    system.add_input("service", {
        "poor": Gaussian(0, 1.5),
        "good": Gaussian(5, 1.5),
        "excellent": Gaussian(10, 1.5),
    })
    system.add_input("food", {
        "rancid": Trapezoid(-2, 0, 2, 4),
        "delicious": Trapezoid(7, 9, 11, 13),
    })

    system.add_output("tip", {
        "cheap": Triangle(0, 5, 10),
        "average": Triangle(7.5, 12.5, 17.5),
        "generous": Triangle(15, 20, 25),
    })
    system.add_rule(
        when("service", "poor").or_is("food", "rancid").then("tip", "cheap")
    )
    system.add_rule(
        when("service", "good").then("tip", "average")
    )
    system.add_rule(
        when("service", "excellent").or_is("food", "delicious").then("tip", "generous")
    )

    system_output = system.run({"service": 3, "food": 8}, (0, 25))
    assert system_output["tip"] == pytest.approx(14.89, 0.1)
