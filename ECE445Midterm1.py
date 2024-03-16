import random

class SATSolver:
    def __init__(self, clauses):
        self.clauses = clauses
        self.assignment = {}
        self.decision_tree = []
        self.literals = set()
        self.literal_clause_map = {}  # Mapping literals to clauses
        self.solutions = []

        # Initialize and extract literals from clauses
        for clause_index, clause in enumerate(self.clauses):
            for literal in clause:
                normalized_literal = literal.strip('~')
                self.literals.add(normalized_literal)
                self.assignment[normalized_literal] = None
                self.literal_clause_map.setdefault(normalized_literal, []).append(clause_index) #clause_map looks like {x1: [0,1,2,3,4,5], x2: ...}. Keeps track of the clauses with that literal.

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
        print(f"Decision: {literal} = {value}")

    def backtrack(self):
        """Undo decisions and implications until reaching a decision that can be inverted."""
        print("Backtracking...")
        if not self.decision_tree:
            return False
        
        while self.decision_tree:
            literal, value = self.decision_tree.pop()
            print(f"Undo decision: {literal} = {value}")
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
       #I believe not all literals have to be assigned as we are asked for the smallest SAT combo.
        return all(value is not None for value in self.assignment.values())

    def has_contradiction(self):
        """Checks if there's a contradiction with the current assignments."""
        for clause in self.clauses:
            if all(self.assignment.get(literal.strip('~'), False) == (literal[0] == '~') for literal in clause):
                print("Contradiction:", clause)
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
        """Checks for a unity clause and assigns the correct value to the one literal to satisfy clause"""
        changed = True #Flag to determine if we found a unity clause an update the value
        while changed:
            changed = False 
            for clause_index, clause in enumerate(self.clauses):
                if self.is_clause_satisfied(clause):
                    continue  # Skip satisfied clauses
                
                unassigned_literals = [literal for literal in clause if self.assignment[literal.strip('~')] is None]
                if len(unassigned_literals) == 1:
                    # Existing unit propagation logic...
                    literal = unassigned_literals[0]
                    print("Unity Clause:", clause, "Unassigned Literal:", literal.strip('~'))
                    value = literal[0] != '~'  #Returns the correct value to make it SAT with that clause
                    self.decide(literal.strip('~'), value)
                    changed = True
                    break

    def solve(self):
        self.unit_propagation() #Assings the value to literal if it detects a unity clause
        if self.is_solved():
            return self.assignment
        if self.has_contradiction():
            if not self.backtrack():
                print("No solution found.")
                return None
        else:
            for literal in self.literals:
                if self.assignment[literal] is None:
                    self.decide(literal, random.choice([True,False]))  # Make a decision
                    result = self.solve()
                    if result:
                        return result
                    self.backtrack()
            print("No solution found after trying all options.")
            return None
        
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

input = input()
clauses = sop_to_CNF(input)

solver = SATSolver(clauses)
#solver.print_literals()
#solver.print_clauses()
solution = solver.solve()
print("Solution:", solution)