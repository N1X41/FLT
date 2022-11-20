from Secondary_functions import *

# Формат ввода :
# [S] -> [P][I]a
# [P] -> [P]b
# [P] -> z
# [I] -> [I]z
# [I] -> [B]b
# [I] -> c
# [I] -> [I][P]b
# [B] -> [B]b
# [B] -> c
# [B] -> [I][P]d

if __name__ == "__main__":
    lines = read()
    grammar = parser(lines)

    print('\nИсходная грамматика : ')
    grammar.print()

    # Рекурсивно собираем один автомат, условно поделенный на блоки, после чего собираем массив отдельных автоматов
    automaton = make_automaton(grammar, grammar.nonterms[0].name, True, [], need_to_be_made(grammar))
    automatons = make_updated_grammar(automaton)

    for auto in automatons:
        print('\nНачальный автомат для - ' + auto[0])
        auto[1].print()

    # На основе имеющихся автоматов собираем новые грамматики для каждого нетерминала
    for auto in automatons:
        print('\nНовая грамматика для - ' + auto[0])
        auto[1] = auto[1].swap(auto[0])
        auto[1].print()

    # Изменяем нетерминалы внутри правил на новые и собираем общую грамматику
    new_grammar = Grammar([])
    for auto in automatons:
        for nont in auto[1].nonterms:
            new_nont = Nonterm(nont.name, [])
            for rule in nont.rules:
                if len(list(set(grammar.return_nonterms()) & set(return_nont_from_rule(rule)))) > 0:
                    new_rule = ''
                    for peace in return_listed_rule(rule):
                        if peace in grammar.return_nonterms():
                            new_rule += '[0' + peace[1:]
                        else:
                            new_rule += peace
                    new_nont.rules.append(new_rule)
                else:
                    new_nont.rules.append(rule)
            new_grammar.nonterms.append(new_nont)
    print('\nНовая грамматика :')
    new_grammar.print()
