from DFA import *
from Monoid import *


def parser(lines):
    start = ""
    states = []
    final_states = []
    transform = []
    alphabet = []
    for line in lines:
        new_line = ""
        if line != "":
            for letter in line:
                if line == lines[0]:
                    if letter == ',':
                        new_line += ' '
                    else:
                        if letter != '<' and letter != '>' and letter != '{' \
                                and letter != '}' and letter != ' ':
                            new_line += letter
                else:
                    if letter == ',' or letter == '-':
                        new_line += ' '
                    else:
                        if letter != '<' and letter != '>' and letter != ' ' and letter != '\t':
                            new_line += letter
        if line != lines[0]:
            if new_line != "":
                helper = new_line.split(' ')
                transform.append(helper)
                if helper[1] not in alphabet:
                    alphabet.append(helper[1])
                if helper[0] not in states:
                    states.append(helper[0])
                if helper[2] not in states:
                    states.append(helper[2])
        else:
            result = new_line.split(' ')
            start = result[0]
            final_states = result[1:len(result)]
    alphabet.sort()
    states.sort()
    final_states.sort()
    dfa = DFA(start, states, final_states, transform, alphabet)
    monoid = Monoid(alphabet)
    return dfa, monoid
