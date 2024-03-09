class SATSolver:
    def __init__(self, clauses):
        self.clauses = clauses  # A list of clauses where each clause is a list of integers representing literals
        self.assignments = {}  # Maps variable (int) to a boolean value
        self.decision_tree = []  # Stack to track decisions and implications (for backtracking)
        self.unit_clauses = []  # Track unit clauses for efficient propagation
        self.literals = [] #Contains all the literals present in CNF



        for item in self.clauses:
            for i in item:
                if(i.find('~') != 1):        #Get list of literals. If NOT in front removes it. [x1, x2, x3] and no ~x1, ~x2 in list 
                    i=i.replace('~', '')
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

    def solve(self):  # Note the removal of `clauses` argument
        """
        Solves the SAT formula using the DPLL algorithm with unit propagation.

        Returns:
            A dictionary representing the solution assignment (variable: truth value)
            or None if the formula is unsatisfiable.
        """

        assignment = {var: False for var in self.literals}  # Initialize with False

        while True:
            if not self.unit_propagation(assignment):
                return None

            # Check if all clauses are satisfied using self.clauses
            if all(any(assignment[abs(lit)] for lit in clause) for clause in self.clauses):
                return assignment

            # If no conflict or satisfaction, make a decision
            variable = self.pick_unassigned_literal()  # Implement this function for decision-making
            self.decide(variable, True)

            # If backtracking is needed, release the unsat branch
            if self.backtrack():
                self.release_unsat_branch()

            # Alternatively, explore both branches for completeness
            # else:
            #     self.decide(variable, False)
                
    def unit_propagation(self, assignment):
        """2
        Performs unit propagation on the current assignment using self.clauses.
        """

        changes = False
        for clause in self.clauses.copy():  # Iterate over a copy of self.clauses
            unassigned_literals = [lit for lit in clause if assignment[abs(lit)] is None]
            if not unassigned_literals:
                return False  # Conflict
            elif len(unassigned_literals) == 1:
                literal = unassigned_literals[0]
                assignment[abs(literal)] = True if literal > 0 else False
                changes = True
                self.clauses.remove(clause)  # Can remove satisfied clause from self.clauses
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