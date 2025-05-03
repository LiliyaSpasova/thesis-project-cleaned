from collections import defaultdict
import pysmile
import pysmile_license
import coefficient_calculator
import numpy as np
from plots import *
from linear_system_solver import *
from get_distribution import *
import itertools
import random
import pgmpy
import yodo
import pandas as pd
import seaborn as sns
from derive_senstivity_function import *

#probability={'CVP': 'HIGH'}, given={'HISTORY': 'TRUE'}

def format_probability(prob_dict):
    """
    Converts a dictionary representation of a probability into a formatted string.
    
    Example:
    {'probability': {'B': 'False'}, 'given': {'MC': 'False', 'X': 'True'}}
    → "P(B=0 | MC=0, X=1)"
    """
    # Convert probability part (assumes single key-value pair)
    prob_var, prob_value = list(prob_dict['probability'].items())[0]
    prob_value = "0" if prob_value == "False" else "1"

    # Convert given conditions (if any)
    given_conditions = []
    if 'given' in prob_dict and prob_dict['given']:
        for var, value in prob_dict['given'].items():
            given_conditions.append(f"{var}={'0' if value == 'False' else '1'}")

    # Construct the final probability string
    if given_conditions:
        return f"({prob_var}={prob_value}|{', '.join(given_conditions)})"
    else:
        return f"({prob_var}={prob_value})"


def get_all_params_for_yodo(net):
    res=[]
    h = net.get_first_node()
    while (h >= 0):
        node_name=net.get_node_name(h)
        distribution=get_cpt_dict(net,node_name)
        for (conditions,value) in distribution:
            temp={}
            probability={}
            given={}
            probability[node_name]=value
            for node,val in conditions:
                given[node]=val
            temp['probability']=probability
            if (bool(given)):
                temp['given']=given
            else:
                temp['given']=None
            name=format_probability(temp)
            res.append((name,temp))
        h = net.get_next_node(h)
    return res

def get_all_marginal_outcomes(net,evidence=None):
    res=[]
    h = net.get_first_node()
    while (h >= 0):
        node_name=net.get_node_name(h)
        distribution=get_cpt_dict(net,node_name)
        for (_,value) in distribution:
            temp={}
            probability={}
            given={}
            probability[node_name]=value
            if evidence is not None:
                for  key, value in evidence:
                    given[key]=value
            temp['probability']=probability
            temp['given']=given
            name=format_probability(temp)
            res.append((name,temp))
        h = net.get_next_node(h)
    seen = {}
    for item in res:
        key = item[0]  # the string part
        if key not in seen:
            seen[key] = item

    unique_names_list = list(seen.values())
    return unique_names_list

def group_param_by_distributions(all_params):
    grouped = defaultdict(list)

    for key, value in all_params:
        prob_key = list(value['probability'].keys())[0]
        grouped[prob_key].append((key, value))

    return grouped

def sample_params(grouped_params, marginal_outcomes, num_samples=5):
    """
    Selects two different parameters from different distributions and a third, separate marginal outcome.
    Returns a formatted output where target is a tuple and parameters are dictionaries with structured data.

    Parameters:
        grouped_params (defaultdict): A dictionary mapping parameter names to their distributions.
        marginal_outcomes (list): A list of available marginal outcomes.
        num_samples (int): Number of samples to generate (default: 5).

    Returns:
        list: A list of tuples (target, [parameter_1, parameter_2])
    """
    if len(grouped_params) < 3:
        raise ValueError("Not enough different distributions to ensure a third distinct selection.")

    results = []

    for _ in range(num_samples):
        # Pick two different parameters from different distributions
        param1, param2 = random.sample(list(grouped_params.keys()), 2)
        
        # Select one random sample from each chosen parameter's distribution
        sample1 = random.choice(grouped_params[param1])
        sample2 = random.choice(grouped_params[param2])

        # Extract the distributions of param1 and param2
        dist1 = list(sample1[1]['probability'].keys())[0]
        dist2 = list(sample2[1]['probability'].keys())[0]

        # Ensure the marginal outcome comes from a third, different distribution
        available_outcomes = [outcome for outcome in marginal_outcomes if list(outcome[1]['probability'].keys())[0] not in {dist1, dist2}]
        if not available_outcomes:
            raise ValueError("Not enough distinct marginal outcomes to ensure a third distribution.")

        # Pick a random marginal outcome
        outcome_param, target = random.choice(available_outcomes)

        # Format the target as ('Node_name', 'value')

        # Convert param1 and param2 into the required format
        def format_param(sample):
            prob_key = list(sample['probability'].keys())[0]
            prob_value = list(sample['probability'].values())[0]
            given_dict = sample.get('given', {})
            given_list = list(given_dict.items()) if given_dict else []  # Convert given dict to list of tuples
            return {'probability': (prob_key, prob_value), 'given': given_list}

        param_1_dict = format_param(sample1[1])
        param_2_dict = format_param(sample2[1])
        
        # Append formatted result
        results.append((format_param(target), [param_1_dict, param_2_dict]))

    return results

def get_sensitivity_values(net, yodo_params,marignal_outcomes):
    num_params = len(yodo_params)
    
    # Initialize an empty DataFrame for storing sensitivity values
    sensitivity_matrix = pd.DataFrame(
        np.zeros(( len(marginal_outcomes),num_params)),  # Matrix of zeros
        index=[p[0] for p in marignal_outcomes],  # Row names = prob params
        columns=[p[0] for p in yodo_params]  # Column names = given params
    )

    # Compute sensitivity for each (prob, given) pair
    for name_x,prob in marignal_outcomes:
        sens_vals = yodo.get_all_sensitivity_values(net,prob)  # Returns 26 values
        
        for (name_y,_,val) in sens_vals:
            sensitivity_matrix.at[name_x, name_y] = val
    
    return sensitivity_matrix
        
def serealize(params):
    res=[]
    for par in params:
        parameters=[]
        par_1=par['param_1'][1]
        par_2=par['param_2'][1]
        par_1['probability']=tuple(par_1['probability'])
        if par_1['given'] is None:
            par_1['given']=[]
        else:
            par_1['given'] = list(par_1['given'].items())  
        par_2['probability']=tuple(par_2['probability'])
        if par_2['given'] is None:
            par_2['given']=[]
        else:
            par_2['given'] = list(par_2['given'].items())  
    
        parameters.append(par_1)
        parameters.append(par_2)
        res.append((parameters,tuple(par['target'].items())))
    return res




    
"""
analysis=yodo(net_bif,{'C':'True'})

plot(net_bif,{'C':'True'})
print(analysis)
sv = analysis[('B','MC')]['derivative']

print(sv)
"""

"""

sensitivity_matrix = get_sensitivity_values(net_bif, yodo_params,marginal_outcomes)

sensitivity_matrix.to_csv("sensitivity_matrix.csv", index=True)


# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(sensitivity_matrix, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.8)

# Labels and title
plt.title("Sensitivity Analysis Heatmap")
plt.xlabel("Given Parameter")
plt.ylabel("Prob Parameter")
plt.show()
"""
#print(marginal_outcomes)
def generate_random_analysis():
    net_xdls = pysmile.Network()
            
    net_xdls.read_file("Brain_Tumor_original.xdsl")

    all_condition_probabilties=get_all_params_for_yodo(net_xdls)

    marginal_outcomes=get_all_marginal_outcomes(net_xdls,[('C','True')])
        
    grouped_by_distributions=group_param_by_distributions(all_condition_probabilties)
    params=sample_params(grouped_by_distributions,marginal_outcomes,10)
    #{'probability': ('ISC', 'False'),'given':[('MC','False'),('SH','True')]}
    for par in params:
        get_all_funtions(net_xdls,par)

def show_heatmap():
    net_xdls = pysmile.Network()
            
    net_xdls.read_file("Brain_Tumor_original.xdsl")

    all_condition_probabilties=get_all_params_for_yodo(net_xdls)

    marginal_outcomes=get_all_marginal_outcomes(net_xdls,[('C','True')])
    net_bif=pgmpy.readwrite.BIFReader("Brain_Tumor_original.bif").get_model()
    sensitivity_matrix = get_sensitivity_values(net_bif, all_condition_probabilties,marginal_outcomes)

    sensitivity_matrix.to_csv("sensitivity_matrix.csv", index=True)


    # Plot heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(sensitivity_matrix, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.8)

    # Labels and title
    plt.title("Sensitivity Analysis Heatmap")
    plt.xlabel("Given Parameter")
    plt.ylabel("Prob Parameter")
    plt.show()
def run_analysis():
    net_xdls = pysmile.Network()
            
    net_xdls.read_file("Brain_Tumor_original.xdsl")
    parameter_1 = {'probability': ('B', 'True'), 'given': [('MC', 'True')]}
    parameter_2 = {'probability': ('ISC', 'True'), 'given': [('MC', 'True')]}
    target = {'probability': ('C', 'True'),'given':None}

    parameters = [target,[parameter_1,parameter_2]]
    get_all_funtions(net_xdls,parameters)

if __name__ == "__main__":
    #generate_random_analysis()

    #show_heatmap()
    for i in range(0,15):
        run_analysis()
        
    
