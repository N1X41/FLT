from solving import *


if __name__ == '__main__':
    equation = "AABxyyxBB=AAyBxxyAB"
    variables, constants, leftPart, rightPart = process_equation(equation)

    print("Левая часть уравнения: " + (''.join([var.name for var in leftPart.equation])).replace(' ', ''))

    print("\nПравая часть уравнения: " + (''.join([var.name for var in rightPart.equation])).replace(' ', ''))

    print("\nУникальные переменные:")
    for var in variables:
        print(var.name)

    print("\nУникальные константы:")
    for const in constants:
        print(const.name)

    leftPart, rightPart = solv(leftPart, rightPart, variables, constants)

    print("\nУпрощенная левая часть уравнения: " + (''.join([var.name for var in leftPart.equation])).replace(' ', ''))

    print("\nУпрощенная правая часть уравнения: " +
          (''.join([var.name for var in rightPart.equation])).replace(' ', ''))
