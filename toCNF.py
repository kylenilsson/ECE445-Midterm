def sop_to_pos(sop_expression):
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
        #CNF_terms.append(pos_term)
        pos_terms.append(' + '.join(pos_term))

    # Combine the PoS terms to form the final PoS expression
    pos_expression = '('
    pos_expression += ') . ('.join(pos_terms)
    pos_expression += ')'
    return pos_expression

# Example usage:
CNF_terms = []
sop_expression = "~x1.x2.~x3 + x1.~x2.~x3 + ~x1.x2.x3"
pos_expression = sop_to_pos(sop_expression)
print("PoS expression:", pos_expression)
#print("Clause List:", CNF_terms)
