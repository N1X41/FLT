import Secondary_functions as sf


class State(object):
    def __init__(self, start, end, rules):
        self.start = start
        self.end = end
        self.rules = rules


class Automaton(object):
    def __init__(self, states):
        self.states = states

    def return_start_states(self):
        answer = []
        for state in self.states:
            if state.start not in answer:
                answer.append(state.start)
        return answer

    def return_end_states(self):
        answer = []
        for state in self.states:
            if state.end not in answer:
                answer.append(state.end)
        return answer

    def return_pairs(self):
        answer = []
        for state in self.states:
            answer.append([state.start, state.end])
        return answer

    def print(self):
        for state in self.states:
            print(state.start + ' ' + state.end)
            print(state.rules)

    def swap(self, nonterm):
        new_lines = []
        for state in self.states:
            for rule in state.rules:
                if state.start != sf.make_new(nonterm, nonterm, task=1):
                    new_lines.append(state.end + ' -> ' + rule + state.start)
                else:
                    new_lines.append(state.end + ' -> ' + rule + state.start)
                    new_lines.append(state.end + ' -> ' + rule)
        new_grammar = sf.parser(new_lines)
        return new_grammar
