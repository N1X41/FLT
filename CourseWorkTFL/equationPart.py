from variable import *

class EquationPart:
    def __init__(self, equation):
        self.equation = equation

    def __eq__(self, other):
        return self.make_string() == other.make_string()

    def __hash__(self):
        return hash(''.join(self.make_string()))

    def count(self):
        result = 0
        for part in self.equation:
            if isinstance(part, Variable):
                result += 1
        return result

    def make_string(self):
        return [part.name for part in self.equation]
