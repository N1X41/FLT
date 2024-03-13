class Transition:
    def __init__(self, var, transition, side):
        self.var = var
        self.transition = transition
        self.side = side

    def make_string_transition(self):
        if self.side == "left":
            return self.var.name + "->" + self.transition.name + self.var.name
        elif self.side == "right":
            return self.var.name + "->" + self.var.name + self.transition.name
        else:
            return self.var.name + "-> _"
