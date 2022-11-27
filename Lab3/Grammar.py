import Secondary_functions as sf


class Nonterm(object):
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules
        self.queue = -1

    def make_queue(self, queue):
        self.queue = queue


class Grammar(object):
    def __init__(self, nonterms):
        self.nonterms = nonterms

    def return_nonterms(self):
        answer = []
        for nont in self.nonterms:
            answer.append(nont.name)
        return answer

    def return_empty(self):
        answer = []
        for nont in self.nonterms:
            if len(nont.rules) == 0:
                answer.append(nont.name)
        return answer

    def print(self):
        for nont in self.nonterms:
            line = nont.name + ' ->'
            for rule in nont.rules:
                line += ' ' + rule + ' |'
            print(line[:len(line) - 2])

    def clean(self):
        for nont in self.nonterms:
            to_del = []
            for rule in nont.rules:
                if len(sf.return_listed_rule(rule)) == 1:
                    if sf.return_listed_rule(rule)[0] == nont.name:
                        to_del.append(rule)
                    elif sf.return_listed_rule(rule)[0] in self.return_nonterms():
                        for nt in self.nonterms:
                            for rl in nt.rules:
                                if nont.name in sf.return_listed_rule(rl):
                                    new_rule = ''
                                    for item in sf.return_listed_rule(rl):
                                        if item != nont.name:
                                            new_rule += item
                                        else:
                                            new_rule += sf.return_listed_rule(rule)[0]
                                    nt.rules.append(new_rule)
                        to_del.append(rule)
                    elif sf.return_listed_rule(rule)[0] == '!':
                        for nt in self.nonterms:
                            for rl in nt.rules:
                                if nont.name in sf.return_listed_rule(rl):
                                    new_rule = ''
                                    for item in sf.return_listed_rule(rl):
                                        if item != nont.name:
                                            new_rule += item
                                    nt.rules.append(new_rule)
                        to_del.append(rule)
            for dell in to_del:
                nont.rules.remove(dell)
        for nont in self.nonterms:
            to_del_from_nont = []
            for rule in nont.rules:
                for item in sf.return_listed_rule(rule):
                    if item in self.return_empty() or (item not in self.return_nonterms() and item[0] == '['):
                        if rule not in to_del_from_nont:
                            to_del_from_nont.append(rule)
            for rule in to_del_from_nont:
                new_rule = ''
                for item in sf.return_listed_rule(rule):
                    if item not in self.return_empty() and not (item not in self.return_nonterms() and item[0] == '['):
                        new_rule += item
                if new_rule != '':
                    nont.rules.append(new_rule)
                nont.rules.remove(rule)
        to_del = []
        for nont in self.nonterms:
            if len(nont.rules) == 0:
                to_del.append(nont)
        for dell in to_del:
            self.nonterms.remove(dell)
        for nont in self.nonterms:
            nont.rules = list(set(nont.rules))

    def remove_lr(self):
        for nont in self.nonterms:
            to_del = []
            for rule in nont.rules:
                if sf.return_listed_rule(rule)[0] in self.return_nonterms():
                    for nt in self.nonterms:
                        if nt.name == sf.return_listed_rule(rule)[0]:
                            for rl in nt.rules:
                                if not nt.name[1].isupper():
                                    new_rule = nt.name[1]
                                else:
                                    if sf.return_listed_rule(rl)[0] in self.return_nonterms():
                                        new_rule = sf.return_listed_rule(rl)[0][1] + rl[3:]
                                    else:
                                        new_rule = rl
                                for item in sf.return_listed_rule(rule)[1:]:
                                    new_rule += item
                                nont.rules.append(new_rule)
                    to_del.append(rule)
            for rule in to_del:
                nont.rules.remove(rule)

    def remove_terms(self):
        new_nonterms = []
        for nont in self.nonterms:
            for rule in nont.rules:
                for item in sf.return_listed_rule(rule):
                    if item not in self.return_nonterms() and item not in new_nonterms:
                        new_nonterms.append(item)
        for nt in new_nonterms:
            new_nt = Nonterm('[' + nt + ']', [nt])
            self.nonterms.append(new_nt)
        for nont in self.nonterms:
            if nont.name[1].isupper():
                new_rules = []
                for rule in nont.rules:
                    new_rule = ''
                    for item in sf.return_listed_rule(rule):
                        if item not in self.return_nonterms():
                            new_rule += '[' + item + ']'
                        else:
                            new_rule += item
                    new_rules.append(new_rule)
                nont.rules += new_rules
        for nont in self.nonterms:
            nont.rules = nont.rules[int(len(nont.rules) / 2):]

    # Функции для устранения левой рекурсии
    def make_queue(self):
        max = 1
        for nont in self.nonterms:
            if nont.queue == -1:
                nont.queue = max
                max += 1
            for rule in nont.rules:
                for item in sf.return_nont_from_rule(rule):
                    for nt in self.nonterms:
                        if nt.name == item and nt.queue == -1:
                            nt.queue = max
                            max += 1

    def update_queue(self):
        for nont in self.nonterms:
            nont.queue *= -1

    def remove_highest_nonterm(self, nonterm):
        to_check = []
        for nont in self.nonterms:
            if nont.name == nonterm:
                checked = []
                to_del = []
                new_rules = []
                for rule in nont.rules:
                    if sf.return_listed_rule(rule)[0] in self.return_nonterms():
                        for nt in self.nonterms:
                            if nt.name == sf.return_listed_rule(rule)[0]:
                                if nt.queue < nont.queue:
                                    to_del.append(rule)
                                    if nt.name not in checked:
                                        new_rules += nt.rules
                                        checked.append(nt.name)
                for rule in to_del:
                    nont.rules.remove(rule)
                for rule in new_rules:
                    for rl in to_del:
                        new_rule = rule
                        for item in sf.return_listed_rule(rl)[1:]:
                            new_rule += item
                        nont.rules.append(new_rule)
                        if sf.return_listed_rule(new_rule)[0] in self.return_nonterms() and sf.return_listed_rule(new_rule) not in to_check:
                            to_check.append(sf.return_listed_rule(new_rule)[0])
                for check in to_check:
                    for nt in self.nonterms:
                        if nt.name == check and nt.queue < nont.queue:
                            self.remove_highest_nonterm(nonterm)
                            break



    def correct_nonterms_lr(self, nonterm):
        already_added = False
        for nont in self.nonterms:
            if nont.name == '[N_' + nonterm[1:]:
                already_added = True
        to_del = []
        for nont in self.nonterms:
            if nont.name == nonterm:
                for rule in nont.rules:
                    if sf.return_listed_rule(rule)[0] == nonterm:
                        to_del.append(rule)
                if not already_added:
                    new_nonterm = Nonterm('[N_' + nonterm[1:], [])
                else:
                    rules = []
                for rule in to_del:
                    nont.rules.remove(rule)
                    new_rule = ''
                    for item in sf.return_listed_rule(rule)[1:]:
                        new_rule += item
                    if not already_added:
                        new_nonterm.rules.append(new_rule)
                        new_nonterm.rules.append(new_rule + new_nonterm.name)
                    else:
                        rules.append(new_rule)
                        rules.append(new_rule + '[N_' + nonterm[1:])
                new_rules = []
                if to_del != []:
                    for rule in nont.rules:
                        new_rules.append(rule + '[N_' + nonterm[1:])
                    nont.rules += new_rules
                    if not already_added and new_nonterm.rules != []:
                        self.nonterms.append(new_nonterm)
                    else:
                        for nont in self.nonterms:
                            if nont.name == '[N_' + nonterm[1:]:
                                nont.rules += rules
