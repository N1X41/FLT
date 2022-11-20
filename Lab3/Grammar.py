class Nonterm(object):
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules


class Grammar(object):
    def __init__(self, nonterms):
        self.nonterms = nonterms

    def return_nonterms(self):
        answer = []
        for nont in self.nonterms:
            answer.append(nont.name)
        return answer

    def print(self):
        for nont in self.nonterms:
            line = nont.name + ' ->'
            for rule in nont.rules:
                line += ' ' + rule + ' |'
            print(line[:len(line) - 2])
