****************
Logical Systems
****************

Logical system extends boolean logic operator into fuzzy domain.
`And` operator is mapped by `t-norm` while `Or` operation is substituted by `t-conorm`.
Negation operator is fuzzy domain is commonly referred as `complement` and most of the times
is defined as :math:`1 - \mu(x)`

Fuzzy Negation
##############
.. plot:: plots/logical_systems/complementary_mf.py

Defined as :math:`1 - \mu(x)` or not complement operation should always negate membership,
i.e each full member of fuzzy set should be casted outside of that set and each non-member
should become full member. Partial memberships should be resolved analogously.

Fuzzy `And` and `Or`
####################

.. plot:: plots/logical_systems/zadeh.py

Each logical system have to define at least they own t-norm (t-conorm may be skipped,
because it can be easily deduced using relation with t-norm). T-Norm should behave semantically
similar to `and`/intersection operator. T-Conorm analogously have to be defined as implementation
of `or`/union operator (if you decide to define it on your own).

Parametrized logical systems
############################

There are logical systems that allow parametrisation of they'r t-norm and t-conorm behaviour
(complement operator is most of the times untouched). Most of the times parametrised systems
are depend on single parameter `p`. Popular pater is such systems is to use other system when
value of `p` reach some edge case (like `0`, `inf`, `-inf`)


For example we can take `Dombi` system with parameter can vary in range [0,inf]. Each figure represents
t-norm and t-conorm combining 3 membership functions with different value of `p`.

For `p` values close to zero we are getting results similar to `Drastic` system:

.. plot:: plots/logical_systems/dombi_with_p_0_dot_1.py
.. plot:: plots/logical_systems/drastic.py

While increasing `p` values leads to result similar with `Zadeh` ones:

.. plot:: plots/logical_systems/dombi_with_p_1.py

.. plot:: plots/logical_systems/dombi_with_p_4.py

In fact `Dombi` system is explicitly defined to be `Drastic` at :math:`p=0` and Zadeh at :math:`p=\infty`.
Intermediate values works analogously, i.e. values closer to zero works similar to `Drastic` while
values closer to infinity works more similarly to `Zadeh`.

Custom logical systems
######################

Each logical system should inherit from LogicalSystem class. Only method you have to
override is t_norm as t_conorm is implemented in LogicalSystem using general relationship between
t_norm and t_conorm. `complement` function will persist same for most of the systems, you don't have
to worry about it.

As an example `Zadeh` logic can be implemented as:

.. literalinclude:: examples/custom_zadeh.py

T-Norm same as t-conorm have to be implemented as higher order function with transforms
two input membership functions into new one.

In fact this library does override t_conorm but this is not required. Resulting system will work same
no matter if t-conorm was overridden or not:

.. plot:: plots/logical_systems/custom_zadeh.py



Predefined logical systems
##########################


.. automodule:: yvain.logical_systems
    :members:
    :private-members:

