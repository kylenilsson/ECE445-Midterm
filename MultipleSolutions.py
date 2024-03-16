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
                    changed = True
                    print(f"Unit propagation: {literal} = {value}")
                    break

    def back_track(self):
        if not self.decision_tree:
            return False
        # Backtrack: undo decisions until one can be flipped
        while self.decision_tree:
            literal, value = self.decision_tree.pop()
            self.assignment[literal] = None  # Undo decision
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
#clauses = [
 #   ['~x1', '~x2', '~x3'],
  #  ['~x1', '~x2', 'x3'],
   # ['~x1', 'x2', '~x3'],
   # ['~x1', 'x2', 'x3'],
    #['x1', '~x2', '~x3'],
    #['x1', '~x2', 'x3'],
    #['x1', 'x2', '~x3'],
    #['x1', 'x2', 'x3'],
#]

def distribute_pos_to_sop(expression):
  # Split the PoS expression into individual clauses
  clauses = expression.split(" . ")

  # Initialize an empty list to store the distributed terms without parentheses
  socterms = []

  # Loop through each clause
  for i in range(len(clauses)):
    current_clause_literals = clauses[i].strip("()").split(" + ")  # Remove parentheses and split

    # Loop through the remaining clauses for distribution
    for j in range(i + 1, len(clauses)):
      remaining_clause_literals = clauses[j].strip("()").split(" + ")  # Remove parentheses and split

      # Combine literals from each clause and add to socterms
      for cl in current_clause_literals:
        for rl in remaining_clause_literals:
          socterms.append(cl + "." + rl)

  # Join the distributed terms (without parentheses) into a single SoP expression
  sop_expression = " + ".join(socterms)

  # Print the SoP expression
  print("SoP expression:", sop_expression)

  return sop_expression

# Example usage
#expression = "(x1 + x2) . (x3 + x4)"
#sop_expression = distribute_pos_to_sop(expression)
#print("SoP expression:", sop_expression)

def sop_to_pos(sop_expression):
    CNF_terms = []
    # Split the SoP expression into terms
    sop_terms = sop_expression.split(' + ')

    pos_terms = []

    for sop_term in sop_terms:
        # Split each term into its seperated literals
        literals = sop_term.split('.')
        pos_term = []

        # For each literal in the SoP term take its compliment
        for literal in literals:
            # Handle negated literals
            if literal.startswith('~'):
                pos_term.append(literal[1:])
            else:
                pos_term.append('~' + literal)

        # Convert the list of literals to a PoS term
        CNF_terms.append(pos_term)
        pos_terms.append(' + '.join(pos_term))

    # Combine the PoS terms to form the final PoS expression
    pos_expression = '('
    pos_expression += ') . ('.join(pos_terms)
    pos_expression += ')'

    print("First step PoS equation", pos_expression)

    return pos_expression

# Example usage:

#sop_expression = expression = "x1.x3 + x1.x4 + x1.x5 + x2.x3 + x2.x4 + x2.x5"
#pos_expression = sop_to_pos(sop_expression)
#print("PoS expression:", pos_expression)
#print("Clause List:", CNF_terms)

def sop_to_pos_clause_list(sop_expression):
    CNF_terms = []
    # Split the SoP expression into terms
    sop_terms = sop_expression.split(' + ')
    CNF_terms = []
    pos_terms = []

    for sop_term in sop_terms:
        # Split each term into its seperated literals
        literals = sop_term.split('.')
        pos_term = []

        # For each literal in the SoP term take its compliment
        for literal in literals:
            # Handle negated literals
            if literal.startswith('~'):
                pos_term.append(literal[1:])
            else:
                pos_term.append('~' + literal)

        # Convert the list of literals to a PoS term
        CNF_terms.append(pos_term)
        pos_terms.append(' + '.join(pos_term))

    # Combine the PoS terms to form the final PoS expression
    pos_expression = '('
    pos_expression += ') . ('.join(pos_terms)
    pos_expression += ')'

    print("CNF expression", pos_expression)
    print("CNF list" , CNF_terms)
    return CNF_terms


def sop_to_CNF(expression):
   pos_expression=sop_to_pos(expression)
   distributed_expression=distribute_pos_to_sop(pos_expression)
   CNF_equation=sop_to_pos_clause_list(distributed_expression)
   return CNF_equation

#def isSAT(clause1, clause2):
#    F= clause1 ^ clause2
#    if(F == 1):
#        SAT = True
#    if(F == 0):
#        print("UNSAT")
#        quit()

#expression = "x1.x2 + x3.x4"
#sop_to_CNF(expression)

# Example usage:
#sop_expression = "~x1.x2.~x3 + x1.~x2.~x3 + ~x1.x2.x3"
#pos_expression = sop_to_pos(sop_expression)
#print("PoS expression:", pos_expression)
#print("Clause List:", CNF_terms)

# Example test
#clauses = [['x1', '~x2', 'x3'], ['~x1', 'x2', 'x3'], ['x1', '~x2', '~x3'], ['~x1', 'x2', '~x3']]
#clauses = [['~x1', '~x2'], ['x1', 'x2'], ['x1', '~x2'], ['~x1', 'x2']]


print("Type in your equation: ")
input = input()
clauses = sop_to_CNF(input)
#SAT = True

#Uncomment if we want to have the XOR part, it is not working correctly.
#clauses2 = []
#("/nAnother Equation? Yes or No")
#if(input() == "Yes"):
#    print("Type in your equation: ")
#    clauses2 = sop_to_CNF(input())

#    isSAT(clauses,clauses2)



solver = SATSolver(clauses)
#solver.print_literals()
#solver.print_clauses()
solution = solver.solve()
print("Solution:", solution)

solver = SATSolver(clauses)

solutions = solver.find_all_solutions()
if not solutions:
    print("UNSAT")
else:
    print("SAT, ", len(solutions), "solutions found.")
    print("All solutions:", solutions)