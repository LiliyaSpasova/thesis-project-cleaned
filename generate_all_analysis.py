from itertools import combinations, product,permutations

import pandas as pd

def sample_params_all(grouped_params, marginal_outcomes):
    """
    Generates all valid combinations where two parameters come from different distributions,
    and the marginal outcome comes from a third, distinct distribution.

    Parameters:
        grouped_params (defaultdict): A dictionary mapping parameter names to their distributions.
        marginal_outcomes (list): A list of available marginal outcomes.

    Returns:
        list: A list of tuples (target, [parameter_1, parameter_2])
    """
    
    if len(grouped_params) < 3:
        raise ValueError("Not enough different distributions to ensure a third distinct selection.")

    results = []

    # Generate all pairs of different parameters from different keys (distributions)
    for param1_name, param2_name in permutations(grouped_params.keys(), 2):
        for sample1, sample2 in product(grouped_params[param1_name], grouped_params[param2_name]):
            # Get the distributions
            dist1 = list(sample1[1]['probability'].keys())[0]
            dist2 = list(sample2[1]['probability'].keys())[0]

            if dist1 == dist2:
                continue  # Skip if distributions are not distinct

            # Find marginal outcomes from a third distinct distribution
            for outcome_param, target in marginal_outcomes:
                dist3 = list(target['probability'].keys())[0]
                if dist3 in {dist1, dist2}:
                    continue  # Skip if not a third distribution

                # Format the entries
                def format_param(sample):
                    prob_key = list(sample['probability'].keys())[0]
                    prob_value = list(sample['probability'].values())[0]
                    given_dict = sample.get('given', {})
                    given_list = list(given_dict.items()) if given_dict else []
                    return {'probability': (prob_key, prob_value), 'given': given_list}

                param_1_dict = format_param(sample1[1])
                param_2_dict = format_param(sample2[1])
                target_formatted = format_param(target)

                results.append((target_formatted, [param_1_dict, param_2_dict]))

    return results

def filter_all_parameter_pairs(results):
    """
    Filters out parameter triples where any node in the target's given (evidence)
    overlaps with the target node or the two parameter nodes.

    Args:
        results (list): List of tuples like (target, [param1, param2]).

    Returns:
        list: Filtered list of valid parameter tuples.
    """
    filtered = []

    for i, (target, params) in enumerate(results):
        target_node = target['probability'][0]
        param1_node = params[0]['probability'][0]
        param2_node = params[1]['probability'][0]

        involved_nodes = {target_node, param1_node, param2_node}

        # Extract evidence from target['given']
        evidence_nodes = {name for name, _ in target.get('given', [])}

        # Check for intersection
        conflicting_nodes = involved_nodes.intersection(evidence_nodes)

        if conflicting_nodes:
            continue

        filtered.append((target, params))

    return filtered
def filter_all_parameter_pairs_by_sensitivity_values(results):
    """
    Filters parameter triples by checking CSV heatmap sensitivity values and
    splits them into three categories: low, mid, and high.
    Each category is saved to a separate text file.
    """
    import os
    param1_labels = set()
    param2_node_labels = set()

    # Prepare file handles
    os.makedirs("filtered_results", exist_ok=True)
    low_file = open("filtered_results/low.txt", "w")
    mid_file = open("filtered_results/mid.txt", "w")
    high_file = open("filtered_results/high.txt", "w")

    for i, (target, params) in enumerate(results):
        param1_label = format_probability(params[0])
        param2_label = format_probability(params[1])
        param2_node = param2_label.split('|')

        if param2_node[0].endswith(' '):
            param2_node_label = param2_node[0][:-1]
        else:
            param2_node_label = param2_node[0]

        target_label = format_probability(target)
        evidence = target['given']
        target_csv_name = 'Brain_tumor'

        if len(evidence):
            evidence_string = target_label.split('|')[1]
            param2_node_label += ' |' + evidence_string
            target_csv_name += '_' + evidence_string[1:]

        target_csv_name += '.csv'
        param1_labels.add(param1_label)
        param2_node_labels.add(param2_node_label)

        try:
            df = pd.read_csv(f"heatmaps/{target_csv_name}", index_col=0)
        except FileNotFoundError:
            print(f"⚠️ CSV file not found: {target_csv_name}")
            continue

        try:
            value = df.loc[param2_node_label, param1_label]
        except KeyError:
            print(f"❌ Label not found in DataFrame: [{param2_node_label}][{param1_label}]")
            continue

        # Format output for writing
        target_str = f"Target: {target['probability'][0]} = {target['probability'][1]}"
        if evidence:
            evidence_str = ', '.join([f"{var} = {val}" for var, val in evidence])
            target_str += f" | Given: {evidence_str}"

        param_strs = []
        for p in params:
            prob = p['probability']
            given = ', '.join([f"{k} = {v}" for k, v in p.get('given', [])])
            entry = f"P({prob[0]} = {prob[1]})"
            if given:
                entry += f" | {given}"
            param_strs.append(entry)

        line = f"{target_str}\nParam1: {param_strs[0]}\nParam2: {param_strs[1]}\nValue: {value:.4f}\n---\n"

        # Save to appropriate file
        if 0 < value < 0.1:
            low_file.write(line)
        elif 0.1 <= value <= 0.5:
            mid_file.write(line)
        elif value > 0.5:
            high_file.write(line)


    # Close all files
    low_file.close()
    mid_file.close()
    high_file.close()




def format_probability(prob_dict):
    """
    Converts a dictionary representation of a probability into a formatted string.
    
    Example:
    {'probability': {'B': 'False'}, 'given': {'MC': 'False', 'X': 'True'}}
    → "P(B=0 | MC=0, X=1)"
    """
    # Convert probability part (assumes single key-value pair)
    prob_var, prob_value = prob_dict['probability']
    prob_value = "0" if prob_value.lower() in ["false", "no", "absent", "off"] else "1"

    # Convert given conditions (if any)
    given_conditions = []
    if 'given' in prob_dict and prob_dict['given']:
        for (var, value) in prob_dict['given']:
            given_conditions.append(f"{var} = {'0' if value.lower() in ['false', 'no', 'absent', 'off'] else '1'}")

    # Construct the final probability string
    if given_conditions:
        return f"{prob_var} = {prob_value} | {', '.join(given_conditions)}"
    else:
        return f"{prob_var} = {prob_value}"