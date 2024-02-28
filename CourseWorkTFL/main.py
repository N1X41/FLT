from solving import *


if __name__ == '__main__':
    # system = System(["AABxyyxBB=AAyBxxAyB"])
    system = System(["Axxyyx=xxyxAAA", "ABxyyx=AyBxxy", "Axxyyx=xxyyxA"])

    variables, constants, system = process_equation(system)

    print("\nУникальные переменные:")
    for var in variables:
        print(var.name)

    print("\nУникальные константы:")
    for const in constants:
        print(const.name)

    for equation in system.system:
        print("\nЛевая часть уравнения: " + (''.join([var.name for var in equation[0].equation])).replace(' ', ''))
        print("Правая часть уравнения: " + (''.join([var.name for var in equation[1].equation])).replace(' ', ''))

    system = solv(system, variables, constants)

    for equation in system.system:
        print("\nУпрощенная левая часть уравнения: " +
              (''.join([var.name for var in equation[0].equation])).replace(' ', ''))
        print("Упрощенная правая часть уравнения: " +
              (''.join([var.name for var in equation[1].equation])).replace(' ', ''))
