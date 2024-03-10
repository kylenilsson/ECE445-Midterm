import random

class SATSolver:
    def __init__(self, clauses):
        self.clauses = clauses  # A list of clauses where each clause is a list of literals
        self.assignment = {}  # Maps literals to their truth values
        self.decision_tree = []  # Stack to track decisions and implications (for backtracking)
        self.literals = []  # Contains all the literals present in the CNF

        # Initialize assignment with all literals set to None and extract literals from clauses
        for item in self.clauses:
            for i in item:
                if(i.find('~') != 1):        #Get list of literals. If NOT in front removes it. [x1, x2, x3] and no ~x1, ~x2 in list 
                    i=i.replace('~', '')
                if i not in self.literals:
                    self.literals.append(i)

        for literal in self.literals:        #Makes dictionary of literals all with an unassigned value. {x1: None, x2: None, ...}
            self.assignment[literal]= None

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

    def unit_propagation(self, literals):
        """Performs unit propagation according to the specified rules."""
        # Check for unit clauses
        unit_clauses = [clause for clause in self.clauses if len(clause) == 1 and self.assignment[clause[0]] is None]

        # If there are unit clauses
        if unit_clauses:
            for clause in unit_clauses:
                literal = clause[0]
                if literal[0] == '~':  # Negation of literal
                    self.assignment[literal[1:]] = False
                else:
                    self.assignment[literal] = True
            return True  # Unit propagation succeeded

        # Check for satisfied clauses or clauses with literals set to True
        
        satisfiable_clauses = [clause for clause in self.clauses if any(self.assignment[lit] is True for lit in clause)]
        self.clauses = [clause for clause in self.clauses if clause not in satisfiable_clauses]

        # If no unit clauses and no satisfied clauses, randomly assign a literal
        if not unit_clauses and not satisfiable_clauses:
            literal_to_assign = random.choice([lit for lit, val in self.assignment.items() if val is None])
            self.decide(literal_to_assign, random.choice([True, False]))
            return True  # Random assignment made

        return False  # No unit clauses and no random assignment made

    def decide(self, literal, value):
        """Make a decision and add it to the decision tree."""
        self.assignment[literal] = value
        self.decision_tree.append((literal, value))

    def solve(self):
        """Solves the SAT formula using the specified rules."""
        while True:
            if not self.unit_propagation(self.literals):
                return None  # If conflict is detected or no more decisions can be made, return None

            # Check if all clauses are satisfied
            if all(any(self.assignment[lit] is True for lit in clause) for clause in self.clauses):
                return self.assignment  # Return satisfying assignment

            # If no conflict and some clauses remain, branch the decision tree
            unassigned_literals = [lit for lit, val in self.assignment.items() if val is None]
            literal_to_branch = random.choice(unassigned_literals)
            self.decide(literal_to_branch, random.choice([True, False]))


# Initializing the solver with a list of clauses
clauses = ['x1', '~x2', 'x3'] # Example clauses
solver = SATSolver(clauses)
solver.print_literals()  # Print literals and their dictionaries
solver.print_clauses()  # Print list of clauses
solution = solver.solve()