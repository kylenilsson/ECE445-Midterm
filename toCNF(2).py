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

expression = "x1.x2 + x3.x4"
sop_to_CNF(expression)