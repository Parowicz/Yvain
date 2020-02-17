*************
Fuzzy systems
*************

There are two main categories of fuzzy systems - Mamdani and Sugeno systems.
In Mamdani system everything is encoded using fuzzy variables - fuzzy output forces
us to perform defuzzification (with may be quite expansive). In Sugeno system implication
rule have form of crisp function with simplifies calculus and gives more flexibility for
price of intuitiveness.

Immortal example of fuzzy system usage is calculating tip % based on food and
service quality. We can create empty Mamdani system using:

::

    from yvain.fuzzy_system import MamdaniSystem
    system = MamdaniSystem.empty()


Fuzzy variable
##############

Fuzzy variable allow us to describe linguistic terms. In classical system we would simply
describe that service can be rated in range of [0, 10]. Fuzzy logic allow us to describe
service using fuzzy terms as "poor", "good or "excellent"

::

    from yvain.membership_functions import Gaussian
    system.add_input("service", {
        "poor": Gaussian(0, 1.5),
        "good": Gaussian(5, 1.5),
        "excellent": Gaussian(10, 1.5),
    })

.. plot:: plots/fuzzy_systems/service.py

For purpose of example we will also add second input variable, with allows us to rate food:

::

    from yvain.membership_functions import Trapezoid
    system.add_input("food", {
        "rancid": Trapezoid(-2, 0, 2, 4),
        "delicious": Trapezoid(7, 9, 11, 13),
    })

.. plot:: plots/fuzzy_systems/food.py

As we mentioned before Mamdani system will also feature fuzzy output. We can add fuzzy outputs
to our system in similar way as adding inputs:

::

    from yvain.membership_functions import Triangle
    system.add_output("tip", {
        "cheap": Triangle(0, 5, 10),
        "average": Triangle(7.5, 12.5, 17.5),
        "generous": Triangle(15, 20, 25),
    })

.. plot:: plots/fuzzy_systems/tip.py

Fuzzy rules
###########

Another important think in fuzzy system is to describe relationships between inputs and outputs.
Such relationships are called `rules`. Fuzzy rules in Mamdani system are formulated as
`IF service is good THEN tip is average`, we are also allowed to use operators known from boolean logic
like `AND`, `OR`. In this library fuzzy rule can be build via fluent api starting from `when` function:


::

    from yvain.fuzzy_system import when
    system.add_rule(when("service", "good").then("tip", "average"))


Mamdani system rule always have to end with `.then` method call and there can be only one such call per rule.
`OR` and `AND` operators are chained via `.or_is` and `.and_is` methods. Those methods does always take
two arguments - variable and state.


::

    system.add_rule(when("service", "poor").or_is("food", "rancid").then("tip", "cheap"))


::

    system.add_rule(when("service", "excellent").or_is("food", "delicious").then("tip", "generous"))

Having all variables and rules added to the system we can use it by simply calling `.run` method.
This method will require dictionary mapping variable to crisp value. This value will be fuzzified,
rules are going to be applied and we will get mapping from output variable to crisp value (our result).

::

    print(system.run({"service": 3, "food": 8}, (0, 25)))
