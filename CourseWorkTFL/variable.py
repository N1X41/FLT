class Variable:
    def __init__(self, name, leght):
        self.name = name
        self.lenght = leght

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name, self.lenght))
