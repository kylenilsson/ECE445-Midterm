import random

class SATSolver:
    def __init__(self, clauses):
        self.clauses = clauses
        self.assignment = {}
        self.decision_tree = []
        self.literals = []

        # Initialize assignment with all literals set to None and extract literals from clauses
        for item in self.clauses:
            for i in item:
                # Remove negation if present to ensure consistency
                if i[0] == '~':
                    literal = i[1:]
                else:
                    literal = i

                if literal not in self.literals:
                    self.literals.append(literal)
                    # Initialize assignment with all literals set to None
                    self.assignment[literal] = None

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
        print(self.assignment)

    def decide(self, literal, value):
        """Make a decision and add it to the decision tree."""
        self.assignment[literal] = value
        self.decision_tree.append((literal, value))
        print(f"Decision: {literal} = {value}")

    def solve(self):
        """Solves the SAT formula using the specified rules."""
        print("Solving SAT formula...")
        self.unit_propagation(self.literals)
        return self.assignment

    def backtrack(self):
        """Undo decisions and implications until reaching a decision that can be inverted."""
        while self.decision_tree:
            literal, value = self.decision_tree.pop()
            self.assignment[literal] = None
            print(f"Backtrack: {literal} = {value}")
  
    def evaluateClauses(self):
        """Evaluate the current assignment against the clauses."""
        for clause in self.clauses:
            clause_result = False
            for literal in clause:
                if literal[0] == '~':
                    if self.assignment[literal[1:]] == False:
                        clause_result = True
                        break
                else:
                    if self.assignment[literal] == True:
                        clause_result = True
                        break
            if clause_result == False:
                return False
        return True

    def unit_propagation(self, literals):
        #Check for unit clauses

        return self.assignment

# Initializing the solver with a list of clauses
clauses = [['x1', '~x2', 'x3'], ['~x1', 'x2', 'x3'], ['x1', '~x2', '~x3']] # Example clauses
solver = SATSolver(clauses)
solver.print_literals()  # Print literals and their dictionaries
solver.print_clauses()  # Print list of clauses
solution = solver.solve()
print(solution)