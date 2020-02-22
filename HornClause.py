NoGood = '⊥'
Negation = '¬'


def isAssumption(value):  
    check = 0
    # Lines 8 and 9 should be commented because the paper says negative assumptions are not assumptions
    if value[check] is Negation:
        check+=1
    return value[check].isupper()

def negation(variable):
    """Denies the variable. It adds the negation symbol.
    """    
    if variable[0] == Negation:
        return variable[1:]
    return Negation + variable

class HornClause:
    """Class that represent a HornClause. Is a classical definition see 
    https://en.wikipedia.org/wiki/Horn_clause
    """    

    def __init__(self, antecedents, consequent = None):
        self.antecedents = antecedents
        self.consequent = consequent
        if isinstance(antecedents, str) and consequent is None:
            self.consequent = antecedents
            self.antecedents = set()
            if not HornClause._isFact(self.antecedents, self.consequent):
                self.antecedents = None

    def __repr__(self):
        if self.isFact(): return "Fact"
        type = "Goal" if self.consequent == NoGood else "Definite"
        return type + " clause: " + str(self.antecedents) + " -> " + self.consequent


    def __eq__(self, other):
        if not isinstance(other, HornClause):
            return False
        if self.consequent == other.consequent:
            if self.antecedents == other.antecedents:
                return True
        return False

    def __hash__(self):
        return hash(str(self))
    
    def isFact(self):
        return HornClause._isFact(self.antecedents, self.consequent)

    @staticmethod
    def _isFact(antecedents, consequent):
        return antecedents == set() and isAssumption(consequent)