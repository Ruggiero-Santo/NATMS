from HornClause import NoGood, negation, Negation, HornClause
from ATMS import ATMS, console_log
from Node import Node

class NATMS(ATMS):

    def NOGOOD(self, E):
        super().NOGOOD(E)
    
        #3. Handle negated assumptions. For every A in E for which notA appears
        # in some justification call UPDATE({E-{A}, -A).
        for A in E:
            for j in self.nodes[NoGood].clause:
                
                # If assumption A has appeared in nogoods before -A is used in
                # some antecedent must be created with the initial label NOGOOD
                notA = negation(A)
                node = self.nodes.get(notA)
                if not node:
                    node = Node(HornClause(notA))
                    # node.label = {frozenset(NoGood)}
                    self.nodes[notA] = node

                if A in j.antecedents:
                    _e = set(E.copy())
                    _e.discard(A)
                    self.UPDATE({frozenset(_e)}, notA)
                    break