from tkinter import Y
from datatypes import *


sections = (Section('sport', 55), Section('dport', 65))
rules = (Rule(sections, 'TCP'),Rule((Section('ip', 'bla'),), 'IP'))
chains = (Chain(rules, 'alert'),Chain(rules, 'kill'))
head = Head(chains, ())

x = Rule(sections, 'TCP')
y = Section('dport', 65)
# print(y)
# print(x)
print(head)