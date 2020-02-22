from HornClause import HornClause

class Node:
    def __init__(self, clause):
        if isinstance(clause, HornClause):
            self.clause = {clause}
            self.label =  set(frozenset())
            if clause.isFact():
                self.label = {frozenset({clause.consequent})}
    
    def addJustification(self, clause):
        self.clause.add(clause)

    def __repr__(self):
        return "Node: {}\n\tJustifications: {}\n\tLabel: {}".format(self.clause.copy().pop().consequent,  self.clause, self.label)
