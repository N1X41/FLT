"""
S - aSb
S - bT
T - aTb
T - bS
S - a
T - a


Q - b
S - FSSRA
T - A
R - A
R - bT
T - bR
S - bR
Q - bQ
R - FRSRA
T - FTRSA
Q - FQSSA
S - A


Q - b
S - fQSQa
S - aSa
T - a
R - a
R - bT
T - bR
S - bR
Q - bQ
R - fQTRa
R - aTa
T - fQTRa
T - aRa
Q - fQSSa
S - a
"""

lines = []
nt_list = []
equival_list = []
empty = []
term = []
result = []

def getEnd(line):
    result = ""
    for i in range(4, len(line)):
        result = result + line[i]
    return result

class Equival(object):
    def __init__(self):
        self.list = []
        self.rules = []

    def add_nt(self, NT):
        self.list.append(NT)

    def set_rules(self, rules):
        self.rules = rules

    def print(self):
        print(self.list)
        print(self.rules)

class NonTerm(object):
    def __init__(self, NT):
        self.NT = NT
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def print(self):
        for rule in self.rules:
            print(self.NT + " - " + rule)

    def make_rules(self):
        new_rules = []
        for rule in self.rules:
            new_rule = ""
            for latter in rule:
                if latter.isupper():
                    if latter not in empty:
                        new_rule = new_rule + "_"
                    else:
                        new_rule = new_rule + "*"
                else:
                    new_rule = new_rule + latter
            new_rules.append(new_rule)
            new_rules.sort()
        return new_rules

def parcer():
    global empty, term
    for line in lines:

        for latter in getEnd(line):
            if latter.isupper():
                if latter not in empty:
                    empty.append(latter)
            else:
                if latter not in term:
                    term.append(latter)

        nt_added = False
        for non_t in nt_list:
            if line[0] == non_t.NT:
                nt_added = True
                non_t.add_rule(getEnd(line))
                break
        if not nt_added:
            nt = NonTerm(line[0])
            nt.add_rule(getEnd(line))
            nt_list.append(nt)

    using = [i.NT for i in nt_list]
    empty = [i for i in empty if i not in using]

    for nt in nt_list:
        nt_added = False
        for eq in equival_list:
            if nt.NT in eq.list:
                nt_added = True
                break
            else:
                if nt.make_rules() == eq.rules:
                    eq.add_nt(nt.NT)
                    nt_added = True
                    break
        if not nt_added:
            eq = Equival()
            eq.add_nt(nt.NT)
            eq.set_rules(nt.make_rules())
            equival_list.append(eq)

def make_rule(rule):
    new_rule = ""
    for latter in rule:
        if latter.isupper():
            if latter not in empty:
                new_rule = new_rule + "_"
            else:
                new_rule = new_rule + "*"
        else:
            new_rule = new_rule + latter
    return new_rule

def get_number(rule):
    answer = ""
    for latter in rule:
        if latter in term:
            answer = answer + 't'
        if latter in empty:
            answer = answer + 'e'
        if latter not in term and latter not in empty:
            count = 1
            for eq in equival_list:
                if latter in eq.list:
                    answer = answer + str(count)
                count = count + 1
    return answer

def equival_classes():
    changes = 1
    while changes > 0:
        changes = 0
        for eq in equival_list:
            new_eq = Equival()
            to_delete = []
            if len(eq.list) > 1:
                base = []
                for nt in nt_list:
                    if nt.NT == eq.list[0]:
                        for rule in nt.rules:
                            base.append(get_number(rule))
                base.sort()
                for nt in eq.list:
                    for nonterm in nt_list:
                        if nonterm.NT == nt:
                            compare = []
                            for rule in nonterm.rules:
                                compare.append(get_number(rule))
                            compare.sort()
                            if base != compare:
                                to_delete.append(nt)
                                #eq.list.remove(nt)
                                new_eq.add_nt(nt)
                                new_eq.rules = eq.rules
                                changes = 1
            if len(to_delete) > 0:
                equival_list.append(new_eq)
                for nt in to_delete:
                    eq.list.remove(nt)

def correct_rules():
    global result
    for eq in equival_list:
        for nt in nt_list:
            if nt.NT == eq.list[0]:
                new_nt = NonTerm(nt.NT)
                for rule in nt.rules:
                    new_rule = ""
                    for latter in rule:
                        if latter in term:
                            new_rule = new_rule + latter
                        if latter in empty:
                            new_rule = new_rule + empty[0]
                        if latter not in term and latter not in empty:
                            for eq_newrule in equival_list:
                                if latter in eq_newrule.list:
                                    new_rule = new_rule + eq_newrule.list[0]
                                    break
                    new_nt.add_rule(new_rule)
                result.append(new_nt)

while True:
    try:
        line = input()
    except EOFError:
        break
    lines.append(line)

parcer()

equival_classes()

print("\n Введенные правила :")
for nt in nt_list:
    nt.print()

print("\n Классы эквивалентности и их общие правила :")
print("Пустые нетерминалы")
for eq in empty:
    print(eq)

for eq in equival_list:
    print("\n")
    eq.print()

correct_rules()

print("\n Упрощенная грамматика :")
for nt in result:
    nt.print()