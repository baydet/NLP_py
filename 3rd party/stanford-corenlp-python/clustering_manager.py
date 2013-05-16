from entities import *
import copy
import client

#self.p -- {verb : {'Li|Ri' : count_of_usages_with_verb }}
#self.l|r = {Li|Ri : total_count_of_usages}


class SynsetRetreiver:
    def __init__(self):
        self.l = {}
        self.r = {}
        self.pl = {}
        self.pr = {}
        self.statements = []
        return

    def find_synsets(self, statements):
        self.statements = statements
        self.build_sets()
        return

    def build_sets(self):
        for s in self.statements:
            #parse left and right parts of statement
            if self.l . has_key(s.left.body):
                self.l[s.left.body] += 1
            else:
                self.l[s.left.body] = 0
            #right
            if self.r . has_key(s.right.body):
                self.r[s.right.body] += 1
            else:
                self.r[s.right.body] = 1
            #building first part of pl and pr
            if not self.pl.has_key(s.v):
                self.pl[s.v] = {}
            self.pl[s.v][s.left.body] = 0
            if not self.pr.has_key(s.v):
                self.pr[s.v] = {}
            self.pr[s.v][s.right.body] = 0

            # building v-vectors
        ccl = copy.deepcopy(self.pl)
        ccr = copy.deepcopy(self.pr)
        for s in self.statements:
            for v in ccl.keys():
                if ccl[v] . has_key(s.left.body):
                    if s.v == v:
                        self.pl[v][s.left.body] += 1
                else:
                    self.pl[v][s.left.body] = 0

            for v in ccr.keys():
                if ccr[v] . has_key(s.right.body):
                    if s.v == v:
                        self.pr[v][s.right.body] += 1
                else:
                    self.pr[v][s.right.body] = 0
        self.build_rel_set()
        # print self.r
        # print self.pr
        # print self.l
        # print self.r
        return

    def get_vector(self, set, ws):
        v = []
        for k in set.keys():
            v.append((set[k]*1.0)/ws[k])
        return v

    def scalar(self, v1, v2):
        res = 0.0
        for i in range(0, len(v1)):
            res += v1[i]*v2[i]
        return res

    def conn_level(self, vli, vlj, vri, vrj):
        a =self.scalar(vli, vlj)
        b = self.scalar(vri, vrj)
        ret = 0.0
        if not (a == b == 0.0):
            ret = 2 * a * b / (a + b)
        # if ret != 0:
            # print ret
        # if ret > 0:
        #     return True
        # else:
        #     return False
        return ret




    def build_rel_set(self):
        sem_map = []
        for i in range(0, len(self.pl)):
            sem_map.append([])
            for j in range(0, len(self.pl)):
                if i == j:
                    sem_map[i].append(1)
                else:
                    sem_map[i].append(0)
        ee = []
        for i in range(0, len(self.pl)):
            for j in range(i+1, len(self.pl)):
                if sem_map[i][j] == 0:
                    vli = self.get_vector(self.pl.values()[i], self.l)
                    vlj = self.get_vector(self.pl.values()[j], self.l)
                    vri = self.get_vector(self.pr.values()[i], self.r)
                    vrj = self.get_vector(self.pr.values()[j], self.r)
                    level = self.conn_level(vli, vlj, vri, vrj)

                    if level > 0:
                        ee.append(level)
                        print self.pl.keys()[i] + ' ' + self.pl.keys()[j] + ' - %f' % level
        print sum(ee)/len(ee)


        return