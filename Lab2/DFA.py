class DFA(object):
    def __init__(self, start, states, final_states, transform, alphabet):
        self.start = start
        self.states = states
        self.final_states = final_states
        self.transform = transform
        self.alphabet = alphabet
        self.correct_states = []
        self.without_not_possible = []
        self.without_traps = []
        self.delete_not_possible([self.start])
        self.delete_traps(self.final_states)
        self.intersection_list()
        self.correct_dfa()

    def print(self):
        print(self.start)
        print(self.states)
        print(self.final_states)
        print(self.alphabet)
        print(self.transform)
        print(self.correct_states)

    def transformation(self, start, letter):
        for transition in self.transform:
            if transition[0] == start and transition[1] == letter:
                return transition[2]
        return False

    def word_in_machine(self, word):
        last_state = self.start
        for letter in word:
            if not self.transformation(last_state, letter):
                return False
            else:
                last_state = self.transformation(last_state, letter)
        if last_state in self.final_states:
            return last_state
        else:
            return False

    def trans_directions(self, start, with_loops):
        result = []
        for transition in self.transform:
            if transition[0] == start:
                if not with_loops:
                    if transition[2] != start:
                        result.append(transition[1])
                else:
                    result.append(transition[1])
        result.sort()
        return result

    def delete_not_possible(self, states):
        new_states = []
        for rule in self.transform:
            for state in states:
                if state == rule[0] and rule[0] != rule[2] and rule[2] not in self.without_not_possible:
                    self.without_not_possible.append(rule[2])
                    new_states.append(rule[2])
        if len(new_states) != 0:
            self.delete_not_possible(new_states)

    def delete_traps(self, states):
        new_states = []
        for rule in self.transform:
            for state in states:
                if state == rule[2] and rule[0] != rule[2] and rule[0] not in self.without_traps:
                    self.without_traps.append(rule[0])
                    new_states.append(rule[0])
        if len(new_states) != 0:
            self.delete_traps(new_states)

    def intersection_list(self):
        self.correct_states = [value for value in self.without_not_possible if value in self.without_traps]
        self.correct_states.append(self.start)


    def correct_dfa(self):
        rules_to_remove = []
        states_to_remove = []
        for rule in self.transform:
            if rule[0] not in self.correct_states or rule[2] not in self.correct_states:
                rules_to_remove.append(rule)
        for state in self.states:
            if state not in self.correct_states:
                states_to_remove.append(state)
        for rule in rules_to_remove:
            self.transform.remove(rule)
        for state in states_to_remove:
            self.states.remove(state)
