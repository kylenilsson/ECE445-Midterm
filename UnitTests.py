import unittest
from newDataStructIdea import SATSolver

class TestSATSolver(unittest.TestCase):
    def setUp(self):
        self.clauses = [['x1', '~x2', 'x3'], ['~x1', 'x2', 'x3'], ['x1', '~x2', '~x3']]
        self.solver = SATSolver(self.clauses)

    def test_init(self):
        self.assertEqual(self.solver.clauses, self.clauses)
        self.assertEqual(self.solver.assignment, {'x1': None, 'x2': None, 'x3': None})
        self.assertEqual(self.solver.decision_tree, [])
        self.assertEqual(self.solver.literals, ['x1', 'x2', 'x3'])

    def test_decide(self):
        self.solver.decide('x1', True)
        self.assertEqual(self.solver.assignment['x1'], True)
        self.assertEqual(self.solver.decision_tree, [('x1', True)])

    def test_backtrack(self):
        self.solver.decide('x1', True)
        self.solver.backtrack()
        self.assertEqual(self.solver.assignment['x1'], None)
        self.assertEqual(self.solver.decision_tree, [])

    def test_evaluateClauses(self):
        self.solver.decide('x1', True)
        self.solver.decide('x2', False)
        self.solver.decide('x3', True)
        self.assertTrue(self.solver.evaluateClauses())

    def test_unit_propagation(self):
        self.solver.unit_propagation(self.solver.literals)
        self.assertEqual(self.solver.assignment, {'x1': None, 'x2': None, 'x3': None})

if __name__ == '__main__':
    unittest.main()