class Graph:
    def __init__(self, number, node, transition, parent, children, ended):
        self.number = number  # порядковый номер
        self.node = node  # system
        self.transition = transition  # переход
        self.parent = parent
        self.children = children
        self.ended = ended

    def thread(self, graph):
        if graph.number == 0:
            return graph.node.print_system()
        else:
            return graph.thread(graph.parent) + "\n" + graph.transition.make_string_transition() +\
                "\n" + graph.node.print_system()
