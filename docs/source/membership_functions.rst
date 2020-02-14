********************
Membership functions
********************
Fuzzy logic is extending boolean true/false by adding term of partial membership.
Membership function is element with allows us to grade membership of element to fuzzy set.

# TODO:

Creating membership function
############################

Any function with take float as an argument and returns value from range of [0, 1] can
serve as membership function. One of the simples membership function is singleton - this membership
function return 1 when x is equal to given value, 0 otherwise.

::

    from math import isclose
    def singleton_at_5(x):
        return 1 if isclose(x, 5) else 0

When possible it's not wise to declare membership functions this way. Popular membership functions
are parametrised and they'r creation should be abstracted into higher order function:

::

    from math import isclose
    def singleton(at):
        return lambda x: 1 if isclose(x, at) else 0



or simple class with overloaded `__call__`:

::

    from math import isclose
    class Singleton:
        def __call__(self, x):
            return 1 if isclose(self.at, x) else 0

        def __init__(self, at):
            self.at = at

Both form are equivalent but this library prefer second form. In Python classes are flexible and
expandable.

Predefined membership functions
###############################

Triangular
**********

.. plot:: plots/membership_functions/simple_triangle.py

.. currentmodule:: yvain.membership_functions
.. autoclass:: Triangle


Trapezoid
*********

.. plot:: plots/membership_functions/simple_trapeze.py

.. currentmodule:: yvain.membership_functions
.. autoclass:: Trapezoid


Gaussian
********

.. plot:: plots/membership_functions/simple_gaussian.py

.. currentmodule:: yvain.membership_functions
.. autoclass:: Gaussian


Bell
****

.. plot:: plots/membership_functions/simple_bell.py

.. currentmodule:: yvain.membership_functions
.. autoclass:: Bell


Sigmoid
*******

.. plot:: plots/membership_functions/simple_sigmoid.py

.. currentmodule:: yvain.membership_functions
.. autoclass:: Sigmoid