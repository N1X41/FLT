import copy

from constatn import *
from variable import *
from equationPart import *
from system import *


def process_equation(system):
    variables = []
    constants = []
    new_system = System([])
    for equation in system.system:
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
        new_system.system.append((leftPart, rightPart))

    return variables, constants, new_system


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


def splitting_by_length(system, vars, consts):
    new_system = copy.deepcopy(system)
    for equation in system.system:
        lenght = min(len(equation[0].equation), len(equation[1].equation)) - 1
        while lenght > 0:
            state = True
            for var in vars:
                if [elem.name for elem in equation[0].equation[:lenght]].count(var.name) != \
                        [elem.name for elem in equation[1].equation[:lenght]].count(var.name):
                    state = False
                    break
            for const in consts:
                if [elem.name for elem in equation[0].equation[:lenght]].count(const.name) != \
                        [elem.name for elem in equation[1].equation[:lenght]].count(const.name):
                    state = False
                    break
            if state:
                new_system.system.append((EquationPart(equation[0].equation[:lenght])
                                          , EquationPart(equation[1].equation[:lenght])))
                new_system.system.append((EquationPart(equation[0].equation[lenght:])
                                          , EquationPart(equation[1].equation[lenght:])))
                lenght = 0
            else:
                lenght -= 1
                if lenght == 0:
                    lenght = min(len(equation[0].equation), len(equation[1].equation)) - 1
                    while lenght > 0:
                        state = True
                        print("abc"[-2:])
                        for var in vars:
                            if [elem.name for elem in equation[0].equation[-lenght:]].count(var.name) != \
                                    [elem.name for elem in equation[1].equation[-lenght:]].count(var.name):
                                state = False
                                break
                        for const in consts:
                            if [elem.name for elem in equation[0].equation[-lenght:]].count(const.name) != \
                                    [elem.name for elem in equation[1].equation[-lenght:]].count(const.name):
                                state = False
                                break
                        if state:
                            new_system.system.append((EquationPart(equation[0].equation[:-lenght])
                                                      , EquationPart(equation[1].equation[:-lenght])))
                            new_system.system.append((EquationPart(equation[0].equation[-lenght:])
                                                      , EquationPart(equation[1].equation[-lenght:])))
                            lenght = 0
                        else:
                            lenght -= 1
                            if lenght == 0:
                                new_system.system.append(equation)
        new_system.system.pop(0)
    return new_system


def solv(system, vars, consts):
    for equation in system.system:
        result = simplification(equation[0], equation[1], consts)
        if result is not None:
            system.system.append(result)
            system.system.pop()
    system = splitting_by_length(system, vars, consts)
    return system
