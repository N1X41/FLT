from Secondary_functions import *

if __name__ == "__main__":
    lines = read()
    grammar = parser(lines)
    grammar_lr = parser(lines)

    # Чистим грамматику от одинарных и пустых переходов
    grammar.clean()
    grammar_lr.clean()

    print('\nИсходная грамматика : ')
    grammar.print()

    # Сперва приведем грамматику к форме Грейбах по средствам устраниния левой рекурсии
    print('\nГрамматика, полученная путем устранения левосторонней рекусии :')
    grammar_lr.make_queue()
    for nont in grammar_lr.nonterms:
        if nont.queue != -1:
            grammar_lr.correct_nonterms_lr(nont.name)
    grammar_lr.nonterms.sort(key=lambda x: x.queue)
    for nont in grammar_lr.nonterms:
        if nont.queue > 0:
            grammar_lr.remove_highest_nonterm(nont.name)
    grammar_lr.update_queue()
    grammar_lr.nonterms.sort(key=lambda x: x.queue)
    for nont in grammar_lr.nonterms:
        grammar_lr.remove_highest_nonterm(nont.name)
        grammar_lr.correct_nonterms_lr(nont.name)
    grammar_lr.remove_terms()
    grammar_lr.remove_lr()
    grammar_lr.print()



    # Рекурсивно собираем один автомат, условно поделенный на блоки, после чего собираем массив отдельных автоматов
    automaton = make_automaton(grammar, grammar.nonterms[0].name, grammar.nonterms[0].name, True, [],
                               need_to_be_made(grammar))
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
                            new_rule += '[N_' + peace[1:]
                        else:
                            new_rule += peace
                    new_nont.rules.append(new_rule)
                else:
                    new_nont.rules.append(rule)
            new_grammar.nonterms.append(new_nont)
    new_grammar.clean()
    new_grammar.remove_terms()
    new_grammar.remove_lr()
    print('\nНовая грамматика, полученная методом Блюма-Коха :')
    new_grammar.print()
