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
        if lenght == 0:
            new_system.system.append(equation)
            new_system.system.pop(0)
        else:
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
            if min(len(equation[0].equation), len(equation[1].equation)) - 1 > 0:
                new_system.system.pop(0)
    if splited:
        return splitting_by_length(new_system, vars, consts)
    else:
        new_system.system = list(set(new_system.system))
        return new_system


def check_previous_up(graph, system, count):
    if graph.number == 0:
        return False
    else:
        for gr in graph.children:
            result = check_previous_down(gr, system, count)
            if result:
                count += 1
                if count > 1:
                    return True
        if graph.node.make_string_system() != system.make_string_system():
            return check_previous_up(graph.parent, system, count)
        else:
            return False


def check_previous_down(graph, system, count):
    if graph.node.make_string_system() == system.make_string_system():
        return False
    else:
        for gr in graph.children:
            result = check_previous_down(gr, system, count)
            if result:
                count += 1
                if count > 1:
                    return True
        return False


def check(
        graph: Graph):  # 0 - требует разбор, 1 - найдено решение, 2 - найдено противоречие, 3 - превышен лимит погружения
    if graph.number == 10:
        graph.ended = 3
        # print("\n Превышен лимит погружения на ветке")
        return
    if check_previous_up(graph.parent, graph.node, 0):
        graph.ended = 4
        print("\n Система свернулась")
        return
    founded_var = False
    for equation in graph.node.system:
        if not any(isinstance(x, Variable) for x in equation[0].equation) and \
                not any(isinstance(x, Variable) for x in equation[1].equation):
            if equation[0].equation != equation[1].equation:
                graph.ended = 2
                # print("\n Найдено противоречие на ветке")
                # print(graph.thread(graph))
                return
            elif not founded_var:
                graph.ended = 1
        else:
            founded_var = True
            graph.ended = 0
    if graph.ended == 1:
        print("\n Найдено решение на ветке")
        print(graph.thread(graph))
        return


def find_optimal_not_null_transition(graph: Graph):
    transition = Transition(None, None, None)

    if graph.number == 0:
        for eq in graph.node.system:
            if eq[0].count() != eq[1].count():
                if isinstance(eq[1].equation[0], Variable) and isinstance(eq[0].equation[0], Constant):
                    transition = Transition(eq[1].equation[0], eq[0].equation[0], "left")
                elif isinstance(eq[0].equation[0], Variable) and isinstance(eq[1].equation[0], Constant):
                    transition = Transition(eq[0].equation[0], eq[1].equation[0], "right")
                else:
                    transition = Transition(eq[0].equation[0], eq[1].equation[0], "left")
        if transition.var is None:
            if isinstance(graph.node.system[0][1].equation[0], Variable) and \
                    isinstance(graph.node.system[0][0].equation[0], Constant):
                transition = Transition(graph.node.system[0][1].equation[0],
                                        graph.node.system[0][0].equation[0], "left")
            elif isinstance(graph.node.system[0][0].equation[0], Variable) and \
                    isinstance(graph.node.system[0][1].equation[0], Constant):
                transition = Transition(graph.node.system[0][0].equation[0],
                                        graph.node.system[0][1].equation[0], "right")
            else:
                transition = Transition(graph.node.system[0][0].equation[0],
                                        graph.node.system[0][1].equation[0], "left")
    else:
        for eq in graph.node.system:
            if len(eq[0].equation) != 0 and len(eq[1].equation) != 0:
                left_transition = Transition(eq[1].equation[0], eq[0].equation[0], "left")
                right_transition = Transition(eq[0].equation[len(eq[0].equation) - 1],
                                              eq[1].equation[len(eq[1].equation) - 1],
                                              "right")
                if graph.transition.side == "left" and \
                        isinstance(left_transition.var, Variable) and isinstance(left_transition.transition, Constant):
                    transition = left_transition
                    break
                elif graph.transition.side == "right" and \
                        isinstance(right_transition.var, Variable) and isinstance(right_transition.transition, Constant):
                    transition = right_transition
                    break
                elif graph.transition.side == "left" and isinstance(left_transition.var, Variable):
                    transition = left_transition
                elif graph.transition.side == "right" and isinstance(right_transition.var, Variable):
                    transition = right_transition
                elif isinstance(left_transition.var, Variable):
                    transition = left_transition
                elif isinstance(right_transition.var, Variable):
                    transition = right_transition

    return transition


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

    new_transition = find_optimal_not_null_transition(graph)

    if new_transition.var is not None:
        if isinstance(new_transition.transition, Constant):
            if new_transition.side == "left":
                new_system = System([])
                for equation in graph.node.system:
                    new_equation = copy.deepcopy(equation)
                    index = 0
                    for i in range(len(equation[0].equation)):
                        if equation[0].equation[i] == new_transition.var:
                            new_equation[0].equation.insert(i + index, new_transition.transition)
                            index += 1
                    index = 0
                    for i in range(len(equation[1].equation)):
                        if equation[1].equation[i] == new_transition.var:
                            new_equation[1].equation.insert(i + index, new_transition.transition)
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

            else:
                new_system = System([])
                for equation in graph.node.system:
                    new_equation = copy.deepcopy(equation)
                    index = 0
                    for i in range(len(equation[0].equation)):
                        if equation[0].equation[i] == new_transition.var:
                            new_equation[0].equation.insert(i + index + 1, new_transition.transition)
                            index += 1
                    index = 0
                    for i in range(len(equation[1].equation)):
                        if equation[1].equation[i] == new_transition.var:
                            new_equation[1].equation.insert(i + index + 1, new_transition.transition)
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
        else:
            if new_transition.side == "left":
                new_system = System([])
                for equation in graph.node.system:
                    new_equation = copy.deepcopy(equation)
                    index = 0
                    for i in range(len(equation[0].equation)):
                        if equation[0].equation[i] == new_transition.var:
                            new_equation[0].equation.insert(i + index, new_transition.transition)
                            index += 1
                    index = 0
                    for i in range(len(equation[1].equation)):
                        if equation[1].equation[i] == new_transition.var:
                            new_equation[1].equation.insert(i + index, new_transition.transition)
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
            else:
                new_system = System([])
                for equation in graph.node.system:
                    new_equation = copy.deepcopy(equation)
                    index = 0
                    for i in range(len(equation[0].equation)):
                        if equation[0].equation[i] == new_transition.var:
                            new_equation[0].equation.insert(i + index + 1, new_transition.transition)
                            index += 1
                    index = 0
                    for i in range(len(equation[1].equation)):
                        if equation[1].equation[i] == new_transition.var:
                            new_equation[1].equation.insert(i + index + 1, new_transition.transition)
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
    print(start_system.print_system())
    graph = Graph(0, start_system, None, None, [], -1)
    levi(graph)

    return start_system
