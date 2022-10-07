import itertools
from Secondary_functions import *


class Monoid(object):
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.rules = [0]
        self.equals = []

    def make_equals(self, dfa):
        for letter in self.alphabet:
            self.equals.append([letter])
        for rule in dfa.transform:
            for equal in self.equals:
                if rule[1] == equal[0]:
                    helper = [rule[0], rule[2]]
                    equal.append(helper)

    def make_sintax_by_number(self, count):
        alphabet = ''
        for letter in self.alphabet:
            alphabet += letter
        return [*map(''.join, itertools.product(alphabet, repeat=count))]


    def make_transformation_monoid(self, dfa):
        ended = False
        count = 2
        while not ended:
            ended = True
            for word in self.make_sintax_by_number(count):
                if word == rewrite(word, self.rules):
                    rules = []
                    for state in dfa.states:
                        rule = [state, state]
                        for letter in word:
                            if rule and dfa.transformation(rule[1], letter):
                                rule[1] = dfa.transformation(rule[1], letter)
                            else:
                                rule = False
                        if rule:
                            rules.append(rule)
                    rules.sort()
                    added = False
                    for equal in self.equals:
                        helper = equal[1:len(equal)]
                        helper.sort()
                        if rules == helper:
                            self.rules[0] = count
                            self.rules.append([word, equal[0]])
                            added = True
                    if not added:
                        helper = [word]
                        for rule in rules:
                            helper.append(rule)
                        self.equals.append(helper)
                        ended = False
            count += 1
