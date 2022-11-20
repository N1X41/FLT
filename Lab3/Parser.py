from Grammar import *
from Secondary_functions import *


def parser(lines):
    grammar = Grammar([])
    for line in lines:
        line = make_clean_line(line)
        line = line.split(' ')
        if line[0] not in grammar.return_nonterms():
            nonterm = Nonterm(line[0], [line[1]])
            grammar.nonterms.append(nonterm)
        else:
            for nont in grammar.nonterms:
                if nont.name == line[0]:
                    nont.rules.append(line[1])
    return grammar
