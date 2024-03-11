class SATSolver:
    def __init__(self, clauses):
        self.clauses = clauses
        self.assignment = {}
        self.decision_tree = []
        self.literals = set()
        self.literal_clause_map = {}  # Mapping literals to clauses

        # Initialize and extract literals from clauses
        for clause_index, clause in enumerate(self.clauses):
            for literal in clause:
                normalized_literal = literal.strip('~')
                self.literals.add(normalized_literal)
                self.assignment[normalized_literal] = None
                self.literal_clause_map.setdefault(normalized_literal, []).append(clause_index)

    def print_literals(self):
        """Prints out the list of literals and their dictionaries."""
        print("Literals and their dictionaries:")
        for literal, value in self.assignment.items():
            print(f"{literal}: {value}")

    def print_clauses(self):
        """Prints out the list of clauses."""
        print("Clauses:")
        for clause in self.clauses:
            print(clause)

    def decide(self, literal, value):
        """Make a decision and add it to the decision tree."""
        self.assignment[literal] = value
        self.decision_tree.append((literal, value))

    def backtrack(self):
        """Undo decisions and implications until reaching a decision that can be inverted."""
        if not self.decision_tree:
            return False
        
        while self.decision_tree:
            literal, value = self.decision_tree.pop()
            self.assignment[literal] = None  # Undo the decision
            if value is False:  # Try the opposite value if the last decision was False
                self.decide(literal, True)
                return True
        return False

    def is_solved(self):
        """Checks if all clauses are satisfied and all variables are assigned."""
        for clause in self.clauses:
            if not any(self.assignment.get(literal.strip('~'), False) != (literal[0] == '~') for literal in clause):
                return False
        return all(value is not None for value in self.assignment.values())

    def has_contradiction(self):
        """Checks if there's a contradiction with the current assignments."""
        for clause in self.clauses:
            if all(self.assignment.get(literal.strip('~'), False) == (literal[0] == '~') for literal in clause):
                return True
        return False

    def unit_propagation(self):
        changed = True
        while changed:
            changed = False
            for clause_index, clause in enumerate(self.clauses):
                unassigned_literals = [literal for literal in clause if self.assignment[literal.strip('~')] is None]
                if len(unassigned_literals) == 1:
                    literal = unassigned_literals[0]
                    value = literal[0] != '~'
                    self.decide(literal.strip('~'), value)
                    changed = True
                    break

    def solve(self):
        self.unit_propagation()
        if self.is_solved():
            return self.assignment
        if self.has_contradiction():
            if not self.backtrack():
                print("No solution found.")
                return None
        else:
            for literal in self.literals:
                if self.assignment[literal] is None:
                    self.decide(literal, True)  # Make a decision
                    result = self.solve()
                    if result:
                        return result
                    self.backtrack()
            print("No solution found after trying all options.")
            return None

# Example test
clauses = [['x1', '~x2', 'x3'], ['~x1', 'x2', 'x3'], ['x1', '~x2', '~x3']]
solver = SATSolver(clauses)
solution = solver.solve()
print("Solution:", solution)
 