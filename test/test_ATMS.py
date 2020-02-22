import unittest

from ATMS import ATMS
from HornClause import HornClause, NoGood, Negation

class TestSum(unittest.TestCase):

    def test_1(self):
        rules = [
            HornClause( {'A', 'B'} , 'r'),
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['r'].label, { frozenset({'A', 'B'}) })

    def test_2(self):
        rules = [
            HornClause( {'D'} , 'l'),
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['l'].label, { frozenset({'D'}) })

    def test_3(self):
        rules = [
            HornClause( {'A'} , 'r'),
            HornClause( {'B'} , 'r'),
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['r'].label, { frozenset({'A'}), frozenset({'B'}) })

    def test_4(self):
        rules = [
            HornClause( {'A'} , 'r'),
            HornClause( {'B'} , 'r'),
            HornClause( {'r'} , 'g'),

        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['g'].label, { frozenset({'A'}), frozenset({'B'}) })

    def test_5(self):
        rules = [
            HornClause( {'D'} , 'l'),
            HornClause( {'E'} , 'k'),
            HornClause( {'D'} , 'k'),
            HornClause( {'l', 'k'} , 'i')
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['i'].label, { frozenset({'D'}) })

    def test_6(self):
        rules = [
            HornClause( {'A'} , 'r'),
            HornClause( {'B'} , 'r'),
            HornClause( {'r'} , 'g'),
            HornClause( {'D'} , 'l'),
            HornClause( {'E'} , 'k'),
            HornClause( {'D'} , 'k'),
            HornClause( {'l'} , 'i'),
            HornClause( {'g', 'i'} , 'h')
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['h'].label, { frozenset({'A','D'}), frozenset({'B','D'}) })

    def test_7(self):
        rules = [
            HornClause( {'A'} , 'r'),
            HornClause( {'B'} , 'r'),
            HornClause( {'r'} , 'g'),
            HornClause( {'D'} , 'l'),
            HornClause( {'E'} , 'k'),
            HornClause( {'D'} , 'k'),
            HornClause( {'l'} , 'i'),
            HornClause( {'g', 'i'} , 'h'),
            HornClause( {'r', 'l'}, NoGood),
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['h'].label, set())
        self.assertEqual(test.nodes[NoGood].label, {frozenset({'A','D'}), frozenset({'B','D'})})

    def test_8(self):
        rules = [
            HornClause({'A'}, 'a'),
            HornClause({'E'}, 'b'),
            HornClause({'B','b'}, 'e'),
            HornClause({'C','a'}, 'f'),
            HornClause({'a','e'}, NoGood),
            HornClause({'D'}, 'e'),
            HornClause({'E'}, 'e'),
            HornClause({'C','e'}, 'g'),
            HornClause({'g','f'}, NoGood),
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['b'].label, {frozenset('E')})
        self.assertEqual(test.nodes[NoGood].label, {frozenset({'A','D'}), frozenset({'E','A'}), frozenset({'E','A','C'}), frozenset({'C','A','D'}) })

    def test_9(self):
        rules = [
            HornClause({'B','b'}, 'e'),
            HornClause({'C','a'}, 'f'),
            HornClause({'a','e'}, NoGood),
            HornClause({'D'}, 'e'),
            HornClause({'A'}, 'a'),
            HornClause({'E'}, 'e'),
            HornClause({'C','e'}, 'g'),
            HornClause({'g','f'}, NoGood),
            HornClause({'E'}, 'b'),
        ]

        test = ATMS(rules)
        test.processRules()

        self.assertEqual(test.nodes['b'].label, {frozenset('E')})
        self.assertEqual(test.nodes[NoGood].label, {frozenset({'A','D'}), frozenset({'E','A'}), frozenset({'E','A','C'}), frozenset({'C','A','D'}) })
   
if __name__ == '__main__':
    unittest.main()