from yvain.fuzzy_system import MamdaniSystem, when
from yvain.membership_functions import Gaussian, Trapezoid, Triangle

if __name__ == '__main__':
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

    print(system.run({"service": 3, "food": 8}, (0, 25)))
