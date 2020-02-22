from HornClause import HornClause, NoGood, isAssumption
from Node import Node

# ATTENTION: In the ATMS implementation the Hyperresolution rule no has been
# inserted but is implemented in a separated function; make it sure to use it to
# get the expected result

class ATMS:

    def __init__(self, rules = [], environment = None, verbose = False):
        self.nodes = dict()
        self.verbose = verbose

        # TODO: (code) check if is a list of HornClause
        self.rules = rules
        # TODO: (code) check if is a set of Fact (HornClause)
        if environment is None:
            self.environment = set(frozenset())
        else:
            self.environment = environment

    def processRules(self, rules = None, environment = None):
        if rules: # TODO: (code) check if is a list of HornClause
            self.rules = rules
        if environment: # TODO: (code) check if is a set of Fact (HornClause)
            self.environment = environment

        _rules = self.rules
        self.rules = []
        for r in _rules:
            self.addRule(r, self.environment)
    
    def addRule(self, rule, environment = None):
        if self.verbose: print("\nNew Rule:", rule)

        self.rules.append(rule)
        if self.nodes.get(rule.consequent, None) == None:
            self.nodes[rule.consequent] = Node(rule)
        else:
            self.nodes.get(rule.consequent).addJustification(rule)

        self.PROPAGATE(rule, {frozenset()}, {frozenset()})
        
    # funzioni sicure
    def PROPAGATE(self, rule, a, I):
        if self.verbose: console_log("PROPAGATE", rule = rule, a = a, I = I)
        L = self.WEAVE(a, I, rule.antecedents)
        if L == set(): return
        self.UPDATE(L, rule.consequent)

    def WEAVE(self, a, I, X):
        if self.verbose: console_log("WEAVE", a = a, I = I, X = X)
        #1. Terminiation Condition
        if X == set():
            return I

        #2. Iterate over the antecedent nodes
        R = X.copy()    # tail of X
        h = R.pop()     # head of X

        #3. Avoid computing the full label
        if h == a:
            return self.WEAVE(set(), I, R)

        #4. Incrementally construct the increniental label
        # union of an environment of I and an environment of h’s label
        node = self.nodes.get(h)
        if not node:
            node = Node(HornClause(h))
            self.nodes[h] = node

        _I = set()
        for env_1 in I:
            for env_2 in node.label:
                _I.add(frozenset(env_1.union(env_2)))
        I = _I

        #5. Ensure that I’ is minimal and contains no known inconsistency
        toRemove = set()
        # remove nogoods
        NoGoodNode = self.nodes.get(NoGood, None)
        if NoGoodNode:
            for env in I:
                if env in NoGoodNode.label:
                    toRemove.add(env)
        I -= toRemove
        # remove any environment subsumed by any other
        for i in I:
            for j in I:
                if i == j: continue
                # if i.issubset(j):
                if i.issuperset(j):
                    toRemove.add(i)
        I -= toRemove

        # 6.
        return self.WEAVE(a, I, R)

    def UPDATE(self, L, n):
        if self.verbose: console_log("UPDATE", L = L, n = n)
        #1. Detect nogoods.
        if n == NoGood:
            for E in L: self.NOGOOD(E)
            return

        #2. Update n’s label ensuring minirnality
        node = self.nodes[n]
        #a: Delete every environment from L which is a superset of some label
        #   environment of n.
        toRemove = set()
        for env_l in L:
            for env_n in node.label:
                if env_l.issuperset(env_n):
                    toRemove.add(env_l)
        L -= toRemove
        #b: Delete every environment from the label of n which is a superset of
        #   some element of L.
        toRemove = set()
        for env_n in node.label:
            for env_l in L:
                if env_n.issuperset(env_l):
                    toRemove.add(env_n)
        node.label -= toRemove
        #c: Add every remaining environment of L to the label of n.
        node.label = node.label.union(L)
        if self.verbose: console_log("LABEL", node_updated = node)

        #3. For every justification j in which n as mentioned as an antecedent
        for j in self.rules:
            if n in j.antecedents:

                #c: Early termination
                if L == set(): return

                #a: Propagate the incremental change to a’s label to its
                #   consequences
                self.PROPAGATE(j, n, L)

                #b: Remove subsumed and inconsistent environments from L
                L = {env for env in self.nodes.get(n).label if env in L}
                
    def NOGOOD(self, E):
        if self.verbose: console_log("NOGOOD", E = E)
       
        #2. Remove E and any superset from every node label
        for n in self.nodes.values():
            toRemove = set()
            for env in n.label:
                if env.issuperset(E):
                    toRemove.add(env)
                    if self.verbose: console_log("TO REMOVE", E = E, from_node = n)
            n.label -= toRemove
            if self.verbose and toRemove != set(): console_log("REMOVED", node_now = n)

        #1: Mark E as nogood.
        self.nodes[NoGood].label.add(E)

    def hyperresolution(self, choose):
        _nogood = set()
        for env_nogood in self.nodes[NoGood].label:
            _nogood = _nogood.union(env_nogood)
        for prop in choose:
            _nogood.remove(prop)
        self.nodes[NoGood].label = _nogood
    
    def __str__(self):
        res = "\n\n"
        for k,n in self.nodes.items():
            if not isAssumption(k):
                res += repr(n) +"\n"
        res += "\n\nAssumption\n"
        for k,n in self.nodes.items():
            if isAssumption(k):
                res += repr(n) + "\n"
        return res
    

def console_log(title, **kargs):
    print(title+":")
    for k, v in kargs.items():
        print("\t", k, ":", v)