import copy

from constatn import *
from variable import *
from equationPart import *
from system import *
from graph import *
from transition import *


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
                    variable = Variable(char, -1)
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
        if not any(isinstance(x, Variable) for x in left.equation) and \
                not any(isinstance(x, Variable) for x in right.equation):
            if left.equation == right.equation:
                return left, right
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
    splited = False
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
                splited = True
            else:
                lenght -= 1
                if lenght == 0:
                    lenght = min(len(equation[0].equation), len(equation[1].equation)) - 1
                    while lenght > 0:
                        state = True
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
                            splited = True
                        else:
                            lenght -= 1
                            if lenght == 0:
                                new_system.system.append(equation)
        if min(len(equation[0].equation), len(equation[1].equation)) - 1 != 0:
            new_system.system.pop(0)
    if splited:
        return splitting_by_length(new_system, vars, consts)
    else:
        return new_system


def check(graph):  # 0 - требует разбор, 1 - найдено решение, 2 - найдено противоречие, 3 - превышен лимит погружения
    if graph.number == 5:
        graph.ended = 3
        # print("\n Превышен лимит погружения на ветке")
        return
    founded_var = False
    for equation in graph.node.system:
        if not any(isinstance(x, Variable) for x in equation[0].equation) and \
                not any(isinstance(x, Variable) for x in equation[1].equation):
            if equation[0].equation != equation[1].equation:
                graph.ended = 2
                # print("\n Найдено противоречие на ветке")
                return
            elif not founded_var:
                graph.ended = 1
        else:
            founded_var = True
            graph.ended = 0
    if graph.ended == 1:
        print("\n Найдено решение на ветке")
        return


def levi(graph):
    vars = list(set([elem for elem in [equation[0].equation + equation[1].equation for equation in graph.node.system][0]
                     if isinstance(elem, Variable)]))
    consts = list(
        set([elem for elem in [equation[0].equation + equation[1].equation for equation in graph.node.system][0]
             if isinstance(elem, Constant)]))
    for var in vars:
        new_transition = Transition(var, '', None)
        new_system = System([])
        for equation in graph.node.system:
            new_equation = copy.deepcopy(equation)
            new_equation[0].equation = [elem for elem in equation[0].equation if elem != var]
            new_equation[1].equation = [elem for elem in equation[1].equation if elem != var]
            new_system.system.append(new_equation)
        for equation in new_system.system:
            result = simplification(equation[0], equation[1], consts)
            if result is not None:
                new_system.system.append(result)
                new_system.system.pop()
        new_system = splitting_by_length(new_system, vars, consts)
        new_child = Graph(graph.number + 1, new_system, new_transition, graph, [], 0)
        check(new_child)
        graph.children.append(new_child)
        if new_child.ended == 0:
            levi(new_child)

        for const in consts:
            new_transition = Transition(var, const, 'left')
            new_system = System([])
            for equation in graph.node.system:
                new_equation = copy.deepcopy(equation)
                index = 0
                for i in range(len(equation[0].equation)):
                    if equation[0].equation[i] == var:
                        new_equation[0].equation.insert(i + index, const)
                        index += 1
                index = 0
                for i in range(len(equation[1].equation)):
                    if equation[1].equation[i] == var:
                        new_equation[1].equation.insert(i + index, const)
                        index += 1
                new_system.system.append(new_equation)
            for equation in new_system.system:
                result = simplification(equation[0], equation[1], consts)
                if result is not None:
                    new_system.system.append(result)
                    new_system.system.pop()
            new_system = splitting_by_length(new_system, vars, consts)
            new_child = Graph(graph.number + 1, new_system, new_transition, graph, [], 0)
            check(new_child)
            graph.children.append(new_child)
            if new_child.ended == 0:
                levi(new_child)

            new_transition = Transition(var, const, 'right')
            new_system = System([])
            for equation in graph.node.system:
                new_equation = copy.deepcopy(equation)
                index = 0
                for i in range(len(equation[0].equation)):
                    if equation[0].equation[i] == var:
                        new_equation[0].equation.insert(i + index + 1, const)
                        index += 1
                index = 0
                for i in range(len(equation[1].equation)):
                    if equation[1].equation[i] == var:
                        new_equation[1].equation.insert(i + index + 1, const)
                        index += 1
                new_system.system.append(new_equation)
            for equation in new_system.system:
                result = simplification(equation[0], equation[1], consts)
                if result is not None:
                    new_system.system.append(result)
                    new_system.system.pop()
            new_system = splitting_by_length(new_system, vars, consts)
            new_child = Graph(graph.number + 1, new_system, new_transition, graph, [], 0)
            check(new_child)
            graph.children.append(new_child)
            if new_child.ended == 0:
                levi(new_child)

        for new_var in vars:
            if new_var != var:
                new_transition = Transition(var, new_var, 'left')
                new_system = System([])
                for equation in graph.node.system:
                    new_equation = copy.deepcopy(equation)
                    index = 0
                    for i in range(len(equation[0].equation)):
                        if equation[0].equation[i] == var:
                            new_equation[0].equation.insert(i + index, new_var)
                            index += 1
                    index = 0
                    for i in range(len(equation[1].equation)):
                        if equation[1].equation[i] == var:
                            new_equation[1].equation.insert(i + index, new_var)
                            index += 1
                    new_system.system.append(new_equation)
                for equation in new_system.system:
                    result = simplification(equation[0], equation[1], consts)
                    if result is not None:
                        new_system.system.append(result)
                        new_system.system.pop()
                new_system = splitting_by_length(new_system, vars, consts)
                new_child = Graph(graph.number + 1, new_system, new_transition, graph, [], 0)
                check(new_child)
                graph.children.append(new_child)
                if new_child.ended == 0:
                    levi(new_child)

                new_transition = Transition(var, new_var, 'right')
                new_system = System([])
                for equation in graph.node.system:
                    new_equation = copy.deepcopy(equation)
                    index = 0
                    for i in range(len(equation[0].equation)):
                        if equation[0].equation[i] == var:
                            new_equation[0].equation.insert(i + index + 1, new_var)
                            index += 1
                    index = 0
                    for i in range(len(equation[1].equation)):
                        if equation[1].equation[i] == var:
                            new_equation[1].equation.insert(i + index + 1, new_var)
                            index += 1
                    new_system.system.append(new_equation)
                for equation in new_system.system:
                    result = simplification(equation[0], equation[1], consts)
                    if result is not None:
                        new_system.system.append(result)
                        new_system.system.pop()
                new_system = splitting_by_length(new_system, vars, consts)
                new_child = Graph(graph.number + 1, new_system, new_transition, graph, [], 0)
                check(new_child)
                graph.children.append(new_child)
                if new_child.ended == 0:
                    levi(new_child)


def solv(start_system, vars, consts):
    for equation in start_system.system:
        result = simplification(equation[0], equation[1], consts)
        if result is not None:
            start_system.system.append(result)
            start_system.system.pop()
    start_system = splitting_by_length(start_system, vars, consts)
    graph = Graph(0, start_system, None, None, [], -1)
    levi(graph)

    return start_system
