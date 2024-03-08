class SATSolver:
    def __init__(self, clauses):
        self.clauses = clauses  # A list of clauses where each clause is a list of integers representing literals
        self.assignments = {}  # Maps variable (int) to a boolean value
        self.decision_tree = []  # Stack to track decisions and implications (for backtracking)
        self.unit_clauses = []  # Track unit clauses for efficient propagation
        self.literals = [] #Contains all the literals present in CNF



        for item in self.clauses:
            for i in item:
                if i not in self.literals:
                    self.literals.append(i)

        for literal in self.literals:        #Makes dictionary of literals all with an unassigned value. {x1: None, x2: None, ...}
            self.assignments[literal]= None


 #   def add_clause(self, clause):
 #       """Add a new clause to the solver."""
 #       self.clauses.append(clause)
 #       # If clause is a unit clause, add it to unit_clauses stack for later use
 #       if len(clause) == 1:
 #           self.unit_clauses.append(clause)

    def decide(self, variable, value):
        """Make a decision and add it to the decision tree."""
        self.assignments[variable] = value
        self.decision_tree.append((variable, value))

    def backtrack(self):
        """Undo decisions and implications until reaching a decision that can be inverted."""
        while self.decision_tree:
            variable, value = self.decision_tree.pop()
            del self.assignments[variable]  # Remove the assignment
            if value == False:  # If we previously assigned False, try True as part of backtracking
                self.decide(variable, True)
                return True
        return False  # If decision_tree is empty, no further backtracking is possible

    def solve(clauses):
        """
        Solves the SAT formula using the DPLL algorithm with unit propagation.

        Args:
            clauses: A list of lists representing clauses (literals combined with OR).

        Returns:
            A dictionary representing the solution assignment (variable: truth value) 
            or None if the formula is unsatisfiable.
        """
        # Initialize assignment with all variables False
        assignment = {var for clause in clauses for var in clause if var[0] != '~'}
        assignment = {var: False for var in assignment}

        while True:
            # Unit propagation
            if not unit_propagation(clauses, assignment):
                return None

            # Check if all clauses are satisfied
            if all(all(assignment[abs(lit)] for lit in clause) for clause in clauses):
                return assignment
        

    def unit_propagation(clauses, assignment):
        """
        Performs unit propagation on the current assignment and clauses.

        Args:
            clauses: A list of lists representing clauses (literals combined with OR).
            assignment: A dictionary mapping variables to truth values (True/False/None).

        Returns:
            A boolean indicating if unit propagation resulted in a conflict (False) 
            or a modified assignment with new deductions (True).
        """
        changes = False
        for clause in clauses.copy():  # Iterate over a copy to avoid modifying original list
            unassigned_literals = [lit for lit in clause if assignment[abs(lit)] is None]
            if len(unassigned_literals) == 0:
            # Conflict detected, formula cannot be satisfied
                return False
            elif len(unassigned_literals) == 1:
                literal = unassigned_literals[0]
                assignment[abs(literal)] = True if literal > 0 else False
                changes = True
                clauses.remove(clause)  # Can remove satisfied clause
        return changes

    def release_unsat_branch(self):
        """Releases all data for the current UNSAT branch."""
        while self.decision_tree:
            variable, _ = self.decision_tree.pop()
            del self.assignments[variable]

        # Optionally, could also reset or handle unit_clauses, clauses, etc., depending on solver strategy

# Initializing the solver with a list of clauses
clauses = [['x1', '~x2', 'x3'], ['~x1', 'x2', 'x3'], ['x1', '~x2', '~x3']] # Example clauses
solver = SATSolver(clauses)
solution = solver.solve()

if solution is None:
  print("No solution found")
else:
  print("Solution:", solution)

# Here, you would add methods to implement unit propagation, the actual CDCL algorithm steps, etc.