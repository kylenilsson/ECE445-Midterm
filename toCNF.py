def sop_to_pos(sop_expression):
    # Split the SoP expression into terms
    sop_terms = sop_expression.split(' + ')

    pos_terms = []
    for sop_term in sop_terms:
        # Split each term into its constituent literals
        literals = sop_term.split('.')
        pos_term = []

        # For each literal in the SoP term, create its complement
        for literal in literals:
            # Handle negated literals
            if literal.startswith('~'):
                pos_term.append(literal[1:])
            else:
                pos_term.append('~' + literal)

        # Convert the list of literals to a PoS term
        pos_terms.append(' + '.join(pos_term))

    # Combine the PoS terms to form the final PoS expression
    pos_expression = ' . '.join(pos_terms)
    return pos_expression

# Example usage:
sop_expression = "~x1 . x2 . ~x3 + x1 . ~x2 . ~x3 + ~x1 . x2 . x3"
pos_expression = sop_to_pos(sop_expression)
print("PoS expression:", pos_expression)
