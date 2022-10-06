from Parcer import *

'''
<Q0, {Q0}>
<Q0, a> -> Q1
<Q0,b>->Q0  
<Q1, a> ->Q0
<Q1,b> -> Q1

<Q0, {Q2,Q1}>
<Q0, a> -> Q1
<Q0,c> -> Q3
<Q3,a> -> Q3
<Q0, b> -> Q0	
<Q1, a> -> Q1
<Q1, b> -> Q2
<Q1,c> -> Q1
<Q2,c> -> Q2
<Q2,a>-> Q1
<Q2,b> -> Q2
<Q4, a>-> Q5>
<Q5, a>-> Q4>

<Q0, {Q0,Q1}>
<Q0, b> -> Q1
<Q0,c> -> Q4
<Q0,a> -> Q3
<Q1, a> -> Q2	
<Q2, c> -> Q2
<Q2, b> -> Q1
<Q3,a> -> Q4
<Q4,a> -> Q5
<Q5,a>-> Q3
'''


if __name__ == "__main__":
    lines = read()
    dfa, monoid = parser(lines)
    monoid.make_equals(dfa)
    monoid.make_transformation_monoid(dfa)
    print("Правила переписывания : ")
    for rule in monoid.rules[1:len(monoid.rules)]:
        print(rule)
    print("\nКлассы эквивалентности")
    for equal in monoid.equals:
        print(equal)
