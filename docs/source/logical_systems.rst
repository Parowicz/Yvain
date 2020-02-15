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

Parametrized logical systems
############################

Custom logical systems
######################

Predefined logical systems
##########################


.. automodule:: yvain.logical_systems
    :members:
