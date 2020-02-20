from abc import ABC
from math import isclose
from typing import List, Dict, Tuple, Callable

from yvain.fuzzy_set import FuzzySet, centroid, DefuzzificationMethod
from yvain.logical_systems import LogicalSystem, Zadeh
from yvain.membership_functions import MembershipFunction


class FuzzyVariable:
    def __init__(self, name: str, fuzzy_set: Dict[str, FuzzySet]):
        self.name = name
        self.fuzzy_set = fuzzy_set


class InvalidRuleError(Exception):
    pass


class FuzzyRule:
    def compile(self, inputs: Dict[str, FuzzyVariable]) -> Callable[[Dict[str, float], ], FuzzySet]:
        """
        Compile rule to plain python function with applies fuzzy on system inputs
        and outputs

        :param inputs: System inputs with symbolic names as dictionary key
        :return: Fuzzy set resulting from rule application
        """

        raise NotImplementedError


class UnaryFuzzyRule(FuzzyRule, ABC):
    def __init__(self, variable_name: str, variable_state: str):
        self.variable_name = variable_name
        self.variable_state = variable_state


class Is(UnaryFuzzyRule):
    """
    IF `variable_name` IS `variable_state`
    """

    def compile(self, inputs: Dict[str, FuzzyVariable]) \
            -> Callable[[Dict[str, float], ], FuzzySet]:
        variable = inputs.get(self.variable_name)
        if variable is None:
            raise InvalidRuleError(
                f"System input does not contain variable named {self.variable_name}"
            )

        state = variable.fuzzy_set.get(self.variable_state)
        if state is None:
            raise InvalidRuleError(
                f"Fuzzy variable {self.variable_name} cannot be member of set {self.variable_state}"
            )

        def output_membership(values: Dict[str, float]) -> FuzzySet:
            value = values.get(self.variable_name)
            if value is None:
                raise ValueError(
                    f"Input value for variable named {self.variable_name} is unknown"
                )
            membership = state.membership(value)
            return FuzzySet(lambda x: membership, state.logic)

        return output_membership


class BinaryFuzzyRule(FuzzyRule, ABC):
    def __init__(self, left_rule: FuzzyRule, right_rule: FuzzyRule):
        self.left_rule = left_rule
        self.right_rule = right_rule


class And(BinaryFuzzyRule):
    """
    `IF left_rule AND right_rule`
    """

    def compile(self, inputs: Dict[str, FuzzyVariable]) \
            -> Callable[[Dict[str, float], ], FuzzySet]:
        def output_membership(values: Dict[str, float]) -> FuzzySet:
            left = self.left_rule.compile(inputs)
            right = self.right_rule.compile(inputs)
            return left(values) & right(values)

        return output_membership


class Or(BinaryFuzzyRule):
    """
    `IF left_rule OR right_rule`
    """

    def compile(self, inputs: Dict[str, FuzzyVariable]) \
            -> Callable[[Dict[str, float], ], FuzzySet]:
        def output_membership(values: Dict[str, float]):
            left = self.left_rule.compile(inputs)
            right = self.right_rule.compile(inputs)
            return left(values) | right(values)

        return output_membership


class Implication:
    """
    `IF rule THEN variable_name IS variable_state`
    """

    def compile(self, inputs: Dict[str, FuzzyVariable], outputs: Dict[str, FuzzyVariable]) \
            -> Callable[[Dict[str, float], ], FuzzySet]:
        variable = outputs.get(self.variable_name)
        if variable is None:
            raise InvalidRuleError(
                f"System output does not contain variable named {self.variable_name}"
            )

        state = variable.fuzzy_set.get(self.variable_state)
        if state is None:
            raise InvalidRuleError(
                f"Fuzzy variable {self.variable_name} cannot be member of set {self.variable_state}"
            )

        def output_membership(values: Dict[str, float]) -> FuzzySet:
            left = self.rule.compile(inputs)
            return left(values) & state

        return output_membership

    def __init__(self, rule: FuzzyRule, variable_name: str, variable_state: str):
        self.rule = rule
        self.variable_name = variable_name
        self.variable_state = variable_state


class FuzzyRuleBuilder:
    def and_is(self, variable: str, state: str) -> 'FuzzyRuleBuilder':
        self.rule = And(self.rule, Is(variable, state))
        return self

    def or_is(self, variable: str, state: str) -> 'FuzzyRuleBuilder':
        self.rule = Or(self.rule, Is(variable, state))
        return self

    def then(self, variable: str, state: str) -> Implication:
        return Implication(self.rule, variable, state)

    def compute(self, output_function: Callable[[Dict[str, float]], float]) \
            -> 'OutputFunction':
        return OutputFunction(self.rule, output_function)

    def __init__(self, rule):
        self.rule = rule


def when(variable: str, state: str) -> FuzzyRuleBuilder:
    return FuzzyRuleBuilder(Is(variable, state))


class MamdaniSystem:
    @classmethod
    def empty(cls, logic: LogicalSystem = Zadeh()):
        return cls({}, {}, [], logic)

    def add_input(self, name: str, memberships: Dict[str, MembershipFunction]):
        self.inputs[name] = FuzzyVariable(name, {
            state: FuzzySet(membership, self.logic)
            for state, membership in memberships.items()
        })

    def add_output(self, name: str, memberships: Dict[str, MembershipFunction]):
        self.outputs[name] = FuzzyVariable(name, {
            state: FuzzySet(membership, self.logic)
            for state, membership in memberships.items()
        })

    def add_rule(self, fuzzy_rule: Implication):
        self.rule_set.append(fuzzy_rule)

    def run(self, values: Dict[str, float], universe: Tuple[float, float]) \
            -> Dict[str, float]:
        start, end = universe

        if start >= end:
            raise ValueError(
                f"Upper bound of universe ({end}) is lower than lower bound ({start})")

        output_sets = {}
        for rule in self.rule_set:
            fuzzy_result = rule.compile(self.inputs, self.outputs)(values)
            if rule.variable_name not in output_sets:
                output_sets[rule.variable_name] = fuzzy_result
            else:
                output_sets[rule.variable_name] |= fuzzy_result

        return {
            variable_name: self.defuzzify(fuzzy_set, start, end)
            for variable_name, fuzzy_set in output_sets.items()
        }

    def __init__(self, inputs: Dict[str, FuzzyVariable], outputs: Dict[str, FuzzyVariable],
                 rules: List[Implication], logic: LogicalSystem,
                 defuzzification_method: DefuzzificationMethod = centroid):
        self.inputs = inputs
        self.outputs = outputs
        self.rule_set = rules
        self.logic = logic
        self.defuzzify = defuzzification_method


class OutputFunction:
    """IF rule THEN f(x)"""

    def compile(self, inputs: Dict[str, FuzzyVariable]) -> Callable[[Dict[str, float]], Tuple[float, float]]:
        rule_weight = self.rule.compile(inputs)

        #  TODO: Code smell - we assume that rule is going to return constant function
        return lambda outs: (rule_weight(outs).membership(0), self.output_function(outs))

    def __init__(self, rule: FuzzyRule, output_function: Callable[[Dict[str, float]], float]):
        self.rule = rule
        self.output_function = output_function


class SugenoSystem:
    @classmethod
    def empty(cls, logic: LogicalSystem = Zadeh()):
        return cls({}, [], logic)

    def add_rule(self, fuzzy_rule: OutputFunction):
        self.rule_set.append(fuzzy_rule)

    def add_input(self, name: str, memberships: Dict[str, MembershipFunction]):
        self.inputs[name] = FuzzyVariable(name, {
            state: FuzzySet(membership, self.logic)
            for state, membership in memberships.items()
        })

    def run(self, values: Dict[str, float]) -> float:
        sum_of_weights = 0
        sum_of_results = 0

        for rule in self.rule_set:
            weight, result = rule.compile(self.inputs)(values)
            sum_of_weights += weight
            sum_of_results += weight * result

        if isclose(sum_of_weights, 0):
            return 0
        else:
            return sum_of_results / sum_of_weights

    def __init__(self, inputs: Dict[str, FuzzyVariable], rules: List[OutputFunction],
                 logic: LogicalSystem):
        self.inputs = inputs
        self.rule_set = rules
        self.logic = logic
