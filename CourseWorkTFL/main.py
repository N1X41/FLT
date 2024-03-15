from solving import *


if __name__ == '__main__':
    # start_system = System(["ABxyyx=AyBxxy"])
    # start_system = System(["Axxyyx=xxyxAAA", "AABy=yBAA"])
    start_system = System(["z=By", "xA=Bx", "xAy=yxA"])

    variables, constants, start_system = process_equation(start_system)

    print("\nУникальные переменные:")
    for var in variables:
        print(var.name)

    print("\nУникальные константы:")
    for const in constants:
        print(const.name)

    for equation in start_system.system:
        print("\nЛевая часть уравнения: " + (''.join([var.name for var in equation[0].equation])).replace(' ', ''))
        print("Правая часть уравнения: " + (''.join([var.name for var in equation[1].equation])).replace(' ', ''))

    graph = solv(start_system, variables, constants)

    # for equation in system.system:
    #     print("\nУпрощенная левая часть уравнения: " +
    #           (''.join([var.name for var in equation[0].equation])).replace(' ', ''))
    #     print("Упрощенная правая часть уравнения: " +
    #           (''.join([var.name for var in equation[1].equation])).replace(' ', ''))
