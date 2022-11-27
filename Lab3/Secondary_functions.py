from Automaton import *
from Grammar import *


def read():
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        lines.append(line)
    return lines


def make_clean_line(line):
    answer = ''
    for letter in line:
        if letter != ' ' and letter != '-' and letter != '>':
            answer += letter
        elif letter == '>':
            answer += ' '
    return answer


def make_new(*args, task):
    if task == 1:
        return args[0][:len(args[0]) - 1] + '_' + args[1][1:]
    else:
        return '[N_' + args[0][1:]


def make_automaton(grammar, nonterm, auto_nt, first_term, made, make_automatons):
    automaton = Automaton([])
    if auto_nt == grammar.nonterms[0].name and first_term:
        state_flag = State('Автомат для ', nonterm, ['----------------'])
        automaton.states.append(state_flag)
    # if first_term:
    made.append(nonterm)
    for nont in grammar.nonterms:
        if nont.name == nonterm:
            for rule in nont.rules:
                if return_listed_rule(rule)[0] not in grammar.return_nonterms():
                    if [make_new(nont.name, auto_nt, task=1), make_new(nont.name, task=0)] not in \
                            automaton.return_pairs():
                        state = State(make_new(nont.name, auto_nt, task=1), make_new(auto_nt, task=0), [rule])
                        automaton.states.append(state)
                    else:
                        for state in automaton.states:
                            if state.end == make_new(nont.name, auto_nt, task=1) and state.start == \
                                    make_new(auto_nt, task=0):
                                state.rules.append(rule)
                else:
                    nt_end = get_end(rule)
                    if return_nont_from_rule(rule)[0] == nont.name:
                        if nont.name + '_' + nont.name not in automaton.return_end_states():
                            state = State(make_new(nont.name, auto_nt, task=1),
                                          make_new(nont.name, auto_nt, task=1), [rule[nt_end:]])
                            automaton.states.append(state)
                        else:
                            for state in automaton.states:
                                if state.end == make_new(nont.name, auto_nt, task=1) and state.start == \
                                        make_new(nont.name, auto_nt, task=1):
                                    state.rules.append(rule[nt_end:])
                    else:
                        state = State(make_new(nont.name, auto_nt, task=1),
                                      make_new(return_nont_from_rule(rule)[0], auto_nt, task=1), [rule[nt_end:]])
                        automaton.states.append(state)
                        if return_nont_from_rule(rule)[0] not in made:
                            new_states = make_automaton(grammar, rule[:nt_end], auto_nt, False, made,
                                                        make_automatons).states
                            for state in new_states:
                                if state.end[:2] == '[N':
                                    state.end = make_new(auto_nt, task=0)
                            automaton.states += new_states
    if first_term and auto_nt == grammar.nonterms[0].name:
        if auto_nt in make_automatons:
            make_automatons.remove(auto_nt)
        for nont in make_automatons:
            state_flag = State('Автомат для ', nont, ['----------------'])
            automaton.states.append(state_flag)
            automaton.states += make_automaton(grammar, nont, nont, True, [], []).states
    return automaton



def parser(lines):
    grammar = Grammar([])
    for line in lines:
        line = make_clean_line(line)
        line = line.split(' ')
        if line[0] not in grammar.return_nonterms():
            if line[1] != '':
                nonterm = Nonterm(line[0], [line[1]])
            else:
                nonterm = Nonterm(line[0], ['!'])
            grammar.nonterms.append(nonterm)
        else:
            for nont in grammar.nonterms:
                if nont.name == line[0]:
                    if line[1] != '':
                        nont.rules.append(line[1])
                    else:
                        nont.rules.append('!')
    return grammar


def make_updated_grammar(automaton):
    automatons = []
    is_writing = False
    for state in automaton.states:
        if state.start == 'Автомат для ' and is_writing:
            is_writing = False
        if state.start == 'Автомат для ' and not is_writing:
            auto = Automaton([])
            automatons.append([state.end, auto])
            is_writing = True
        if is_writing and state.start != 'Автомат для ':
            automatons[len(automatons)-1][1].states.append(state)
    return automatons


def return_nont_from_rule(rule):
    answer = []
    word = ''
    is_reading = False
    for letter in rule:
        if letter == '[':
            is_reading = True
        if is_reading:
            word += letter
        if letter == ']':
            is_reading = False
            answer.append(word)
            word = ''
    return answer


def return_listed_rule(rule):
    answer = []
    word = ''
    is_reading = False
    for letter in rule:
        if letter == '[':
            is_reading = True
        if is_reading:
            word += letter
        if letter == ']':
            is_reading = False
            answer.append(word)
            word = ''
        if not is_reading and letter != ']':
            answer.append(letter)
    return answer


def get_end(rule):
    nt_end = 1
    for letter in rule:
        if letter != ']':
            nt_end += 1
        else:
            break
    return nt_end


def need_to_be_made(grammar):
    answer = []
    for nonterm in grammar.nonterms:
        for rule in nonterm.rules:
            if rule[0] == '[':
                for nt in return_nont_from_rule(rule)[1:]:
                    if nt not in answer:
                        answer.append(nt)
            else:
                for nt in return_nont_from_rule(rule):
                    if nt not in answer:
                        answer.append(nt)
    return answer
