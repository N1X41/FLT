from constatn import *
from variable import *
from equationPart import *


def process_equation(equation):
    variables = []
    constants = []
    leftPart = EquationPart([])
    rightPart = EquationPart([])
    side = True
    for part in equation.split("="):
        for char in part:
            if char.isalpha() and char.isupper():
                constant = Constant(char)
                if constant.name not in [c.name for c in constants]:
                    constants.append(constant)
                if side:
                    leftPart.equation.append(constant)
                else:
                    rightPart.equation.append(constant)
            elif char.isalpha():
                variable = Variable(char)
                if variable.name not in [v.name for v in variables]:
                    variables.append(variable)
                if side:
                    leftPart.equation.append(variable)
                else:
                    rightPart.equation.append(variable)
        side = False

    return variables, constants, leftPart, rightPart


def simplification(left, right, consts):
    if len(left.equation) > 0 and len(right.equation) > 0:
        if isinstance(left.equation[0], Constant) and isinstance(right.equation[0], Constant) and \
                left.equation[0].name == right.equation[0].name:
            left.equation.pop(0)
            right.equation.pop(0)
            return simplification(left, right, consts)
        else:
            if isinstance(left.equation[-1], Constant) and isinstance(right.equation[-1], Constant) and \
                    left.equation[-1].name == right.equation[-1].name:
                left.equation.pop()
                right.equation.pop()
                return simplification(left, right, consts)
            else:
                return left, right
    else:
        return left, right


def solv(left, right, vars, consts):
    result = simplification(left, right, consts)
    if result is not None:
        left, right = result
    return left, right
