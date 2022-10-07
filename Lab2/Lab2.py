from Parcer import *
import time

'''
<A0,{A5,A3,A7}>
<A9,a>->A0
<A0,c>->Q1
<Q1,a>->Q2
<Q2,b>->Q1
<B0,b>->A9
<A9,b>->B0
<A0,a>->A1
<A0,b>->A2
<A1,a>->A3
<A1,b>->A4
<A3,a>->A3
<A3,b>->A4
<A7,a>->A8
<A7,b>->A8
<A8,a>->A7
<A4,a>->A3
<A4,b>->A4
<A2,a>->A6
<A2,b>->A5
<A6,a>->A6
<A6,b>->A5
<A5,a>->A6
<A5,b>->A5
'''


if __name__ == "__main__":
    lines = read()
    dfa, monoid = parser(lines)
    start = time.process_time()
    monoid.make_equals(dfa)
    monoid.make_transformation_monoid(dfa)
    end = time.process_time()
    print("Время выполнения : " + str(end-start))
    print("\nПравила переписывания : ")
    for rule in monoid.rules[1:len(monoid.rules)]:
        print(rule)
    print("\nКлассы эквивалентности")
    for equal in monoid.equals:
        print(equal)
