import random

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

    def decide(self, literal, value):
        """Make a decision and add it to the decision tree."""
        self.assignment[literal] = value
        self.decision_tree.append((literal, value))
        #print(self.decision_tree)

    def is_solved(self):
        """Checks if all clauses are satisfied with at least one literal being true in each."""
        for clause in self.clauses:
            if not any(self.assignment.get(literal.strip('~'), False) != (literal[0] == '~') for literal in clause):
                return False  # At least one clause is not satisfied
        return True  # All clauses are satisfied

    def has_contradiction(self):
        """Checks if there's a contradiction with the current assignments."""
        for clause in self.clauses:
            if all(self.assignment.get(literal.strip('~'), False) == (literal[0] == '~') for literal in clause):
                #print("Contradiction:", clause)
                return True
        return False

    def is_clause_satisfied(self, clause):
        """Checks if a clause is satisfied based on the current assignments."""
        for literal in clause:
            literal_value = literal.strip('~')
            is_negated = literal.startswith('~')
            assigned_value = self.assignment.get(literal_value)

            # If the literal is assigned True and not negated, or assigned False and negated, the clause is SAT.
            if assigned_value is not None and ((assigned_value and not is_negated) or (not assigned_value and is_negated)):
                return True
        return False

    def unit_propagation(self):
        changed = True
        while changed:
            changed = False
            for clause_index, clause in enumerate(self.clauses):
                if self.is_clause_satisfied(clause):
                    continue  # Skip satisfied clauses
                
                unassigned_literals = [literal for literal in clause if self.assignment[literal.strip('~')] is None]
                if len(unassigned_literals) == 1:
                    literal = unassigned_literals[0]
                    value = literal[0] != '~'
                    self.decide(literal.strip('~'), value)
                    print(f"Unit propagation: {literal} = {value}")
                    changed = True
                    #print(f"Unit propagation: {literal} = {value}")
                    break

    def back_track(self):
        if not self.decision_tree:
            return False
        # Backtrack: undo decisions until one can be flipped
        while self.decision_tree:
            literal, value = self.decision_tree.pop()
            self.assignment[literal] = None  # Undo decision
            print(f"Backtrack: {literal} = {value}")
            if value is False:  # Flip decision if possible
                self.decide(literal, True)
                return True
        return False

    def solve(self):
        while True:
            # Run unit propagation at the start of each iteration
            self.unit_propagation()
            
            if self.has_contradiction():
                # Attempt to backtrack; if not possible, the problem is unsolvable
                if not self.back_track():
                    return None
            else:
                # Try to make a new decision
                made_decision = False
                for literal in self.literals:
                    if self.assignment[literal] is None:
                        self.decide(literal, False)
                        made_decision = True
                        break
                    
                # If no new decision was made, check if all clauses are satisfied
                if not made_decision:
                    if self.is_solved():
                        print("Solved!")
                        return self.assignment
                    else:
                        # If not all clauses are satisfied, attempt to backtrack
                        if not self.back_track():
                            return None


    def find_all_solutions(self):
        all_solutions = []
        original_clauses = self.clauses[:]
        negated_clauses = []

        while True:
            # Create a new SATSolver instance with the original clauses plus any negated clauses
            solver = SATSolver(original_clauses + negated_clauses)
            solution = solver.solve()
            #print("Solution:", solution)
            
            if solution is None:
                break  # No more solutions found
            # Convert the solution to a unique string representation and add it to the list of all solutions
            solution_str = ''.join(f"{lit}:{'T' if val else 'F'}" for lit, val in sorted(solution.items()))
            all_solutions.append(solution_str)

            # Generate a new clause that negates the current solution
            new_negated_clause = [f"~{lit}" if val else lit for lit, val in solution.items()]
            negated_clauses.append(new_negated_clause)

        return all_solutions
        
# Example usage:
clauses = [
    ['~x1', '~x2', '~x3'],
    ['~x1', '~x2', 'x3'],
    ['~x1', 'x2', '~x3'],
    ['~x1', 'x2', 'x3'],
    #['x1', '~x2', '~x3'],
    #['x1', '~x2', 'x3'],
    #['x1', 'x2', '~x3'],
    #['x1', 'x2', 'x3'],
]

solver = SATSolver(clauses)

solutions = solver.find_all_solutions()
if not solutions:
    print("UNSAT")
else:
    print("SAT, ", len(solutions), "solutions found.")
    print("All solutions:", solutions)
