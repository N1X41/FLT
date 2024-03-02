class Graph:
    def __init__(self, number, node, transition, parent, children, ended):
        self.number = number  # порядковый номер
        self.node = node  # system
        self.transition = transition  # переход
        self.parent = parent
        self.children = children
        self.ended = ended
