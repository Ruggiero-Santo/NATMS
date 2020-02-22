import unittest
from NATMS import NATMS
from HornClause import HornClause, NoGood, Negation

class TestSum(unittest.TestCase):

    def test_1(self):
        rules = [
            HornClause({'A', 'C'}, NoGood),
            HornClause({'B', 'C'}, NoGood),
            HornClause({ Negation+'A', Negation+'B'}, NoGood),
        ]

        test = NATMS(rules)
        test.processRules()
        
        # abbastanza sicuro
        assert frozenset('C') in test.nodes[NoGood].label

    def test_2(self):
        rules = [
            HornClause( {'A', 'B', 'C'} , NoGood)
        ]

        test = NATMS(rules)
        test.processRules()

        # non molto sicuro
        assert frozenset({'C', 'B'}) in test.nodes['¬A'].label
        assert frozenset({'A', 'C'}) in test.nodes['¬B'].label
        assert frozenset({'A', 'B'}) in test.nodes['¬C'].label

    def test_3(self):
        rules = [
            HornClause( {'A'} , 'b'),
            HornClause( {Negation + 'A'} , 'b')
        ]

        test = NATMS(rules)
        test.processRules()

        assert test.nodes['b'].label == { frozenset({Negation + 'A'}), frozenset({'A'}) }

if __name__ == '__main__':
    unittest.main()