def parse_probability_line(line):
    """
    Parses a line like:
    - P(MC = False)
    - P(ISC = False) | MC = False, B = True
    into a dictionary with 'probability' and 'given'
    """
    prob_part, *given_part = line.replace("P(", "").replace(")", "").split("|")
    prob_node, prob_value = [s.strip() for s in prob_part.split("=")]

    param = {
        "probability": (prob_node, prob_value),
        "given": []
    }

    if given_part:
        givens = given_part[0].split(",")
        for g in givens:
            if "=" in g:
                key, val = [x.strip() for x in g.split("=")]
                param["given"].append((key, val))
    return param


def load_params(filename):
    """
    Reads a text file of saved parameter combinations and reconstructs them into
    (target, [param1, param2], value) format.
    """
    results = []
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    i = 0
    while i < len(lines):
        # Target line
        target_line = lines[i].replace("Target: ", "")
        if "| Given:" in target_line:
            target_prob, given_part = target_line.split("| Given:")
            target_node, target_val = [s.strip() for s in target_prob.split("=")]
            given_pairs = []
            for g in given_part.split(","):
                k, v = [x.strip() for x in g.split("=")]
                given_pairs.append((k, v))
        else:
            target_node, target_val = [s.strip() for s in target_line.split("=")]
            given_pairs = []

        target = {
            "probability": (target_node, target_val),
            "given": given_pairs
        }

        # Param1 and Param2
        param1 = parse_probability_line(lines[i+1].replace("Param1: ", ""))
        param2 = parse_probability_line(lines[i+2].replace("Param2: ", ""))

        # Value
        value = float(lines[i+3].replace("Value: ", ""))

        results.append((target, [param1, param2], value))

        i += 5  # Skip to next block (includes --- separator)

    return results

