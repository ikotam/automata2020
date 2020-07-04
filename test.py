from Otomat import Otomat
import collections


G = Otomat()

with open('input1.txt', 'r') as f:
    lines = f.readlines()
    for line in lines[:-2]:
        tmp = line.replace('\n', '').split(' ')
        G.add_arc(tmp[0], tmp[1], tmp[2])
    G.set_Start(lines[-2].replace('\n', ''))
    G.set_Finish(lines[-1].replace('\n', '').split(' '))

# print(G.arcDict)
# print(G.DFA())
G.Minimize_Otomat()
