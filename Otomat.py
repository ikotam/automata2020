import collections
import copy

class Otomat:
    def __init__(self, states, Sigmoid, start, finish):
        self.__init__(states, start, finish)
        self.Sigmoid = Sigmoid
    
    def __init__(self, states, start, finish):
        self.states = states
        self.Start = start
        self.Finish = finish
    def __init__(self):
        self.arcDict = {} # danh sách cung trong otomat
        self.count_in_State = {} # đếm số trạng thái trỏ vào trạng thái đang xét 
        self.states = [] # danh sách các trạng thái
        self.Finish = [] # tập các trạng thái kết 
        self.Start = None # đỉnh vào
        self.Sigmoid = [] # bảng chữ  cái

    def set_Sigmoid(self, Sigmoid):
        self.Sigmoid = Sigmoid
    
    def set_Start(self, Start):
        self.Start = Start

    def set_Finish(self, Finish):
        self.Finish = Finish

    def add_Finish(self, state):
        self.Finish.append(state)

    def add_arc(self, p, q, a): # thêm cung mới vào otomat, delta(p, a) = q   
        if (p not in self.states):
            self.states.append(p)
            self.arcDict[p] = {}
            self.count_in_State[p] = 0

        if (q not in self.states):
            self.states.append(q)
            self.arcDict[q] = {}
            self.count_in_State[q] = 0

        if (a not in self.Sigmoid):
            self.Sigmoid.append(a)

        self.arcDict[p][a] = q
        self.count_in_State[q] += 1

    def get_arcDict(self):
        return self.arcDict
    
    def check_unreachable_state(self):
        for state in self.states:
            if (self.count_in_State[state] == 0) and state != self.Start:
                return False

        return True

    def Remove_state(self, state):
        for alpha in self.arcDict[state]:
            self.count_in_State[self.arcDict[state][alpha]] -= 1

        self.arcDict.pop(state)
        self.states.remove(state)

        for st in self.arcDict:
            for alpha in self.arcDict[st]:
                if self.arcDict[st][alpha] == state:
                    self.arcDict[st].pop(alpha)


    def remove_unreachable_state(self):
        for state in self.states:
            if (self.count_in_State[state] == 0) and state != self.Start:
                self.Remove_state(state)
                self.count_in_State[state] == 0

        if (self.check_unreachable_state() == False): self.remove_unreachable_state()

    def checkP(self, state1, state2):
        if state1 == state2: return True
        if (state1 in (self.Finish)) and (state2 not in (self.Finish)): return False
        if (state1 not in (self.Finish)) and (state2 in (self.Finish)): return False
        return True

    def equal(self, Dict1, Dict2):
        if (Dict1 == Dict2): return True
        return False

    def DFA(self):
        self.fill_otomat()
        self.remove_unreachable_state()
        mark = {}
        newmark = {}

        for state1 in self.states:
            newmark[state1] = {}
            for state2 in self.states:
                if state2 > state1:
                    newmark[state1][state2] = True
                    if (self.checkP(state1, state2) == False):
                        newmark[state1][state2] = False

        
        while (self.equal(mark, newmark) == False):            
            mark = copy.deepcopy(newmark)
            
            for state1 in self.states:
                for state2 in self.states:
                    if state2 > state1 and (mark[state1][state2] == True):
                    # if (mark[state1][state2] == True):
                        for alpha in self.Sigmoid:
                            # print(state1, state2, alpha)
                            st3 = self.arcDict[state1][alpha]
                            st4 = self.arcDict[state2][alpha]
                            if (st3 == st4): continue
                            if (st3 > st4): st3, st4 = st4, st3
                            
                            if (mark[st3][st4] == False): 
                                newmark[state1][state2] = False
                                break

        return newmark 

    def Minimize_Otomat(self):
        mark = self.DFA()
        Gmin = Otomat()
        Gmin.set_Sigmoid(self.Sigmoid)

        new_states = []
        flag = {st: -1 for st in self.states}
        cnt = 0
        for st1 in self.states:
            if flag[st1] != -1: continue
            tmp = [st1]
            flag[st1] = cnt          
            for st2 in self.states:
                if st2 > st1 and (mark[st1][st2] == True):
                # if (mark[st1][st2] == True):
                    tmp.append(st2)
                    flag[st2] = flag[st1]
            new_states.append(tmp)
            cnt += 1
            

        new_arc = {}

        for i in range(len(new_states)):
            sts = new_states[i]
            new_arc[i] = {}
            for st in sts:
                for alpha in self.arcDict[st]:
                    stt = flag[self.arcDict[st][alpha]]
                    new_arc[i][alpha] = new_states[stt]
                    
        for st in new_arc:
            print(new_states[st], ': ', end= ' ')
            print((new_arc[st]))


    def fill_otomat(self):
        for st in self.states:
            for alpha in self.Sigmoid:
                if alpha not in self.arcDict[st]:
                    self.add_arc(st,'epsilon', alpha)



