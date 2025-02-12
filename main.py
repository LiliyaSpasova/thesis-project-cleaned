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

from yodo import *
import pandas as pd
import seaborn as sns

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
        return f"{prob_var} = {prob_value} | {', '.join(given_conditions)})"
    else:
        return f"{prob_var} = {prob_value}"


def get_all_params_for_yodo(net):
    res=[]
    h = net.get_first_node()
    while (h >= 0):
        node_name=net.get_node_name(h)
        print(node_name)
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
    print(res, end="\n")
    print(res.__len__())
    return res

def get_all_marginal_outcomes(net,evidence=None):
    res=[]
    h = net.get_first_node()
    while (h >= 0):
        node_name=net.get_node_name(h)
        distribution=get_cpt_dict(net,node_name)
        if evidence is not None:
            for  key, value in evidence:
                net.set_evidence(key,value)
        net.update_beliefs()

        for (conditions,value) in distribution:
            temp={}
            probability={}
            given={}
            probability[node_name]=value
            for node,val in conditions:
                given[node]=val
            temp['probability']=probability
            name=format_probability(temp)
            res.append((name,()))
        h = net.get_next_node(h)
    unique_names_list = list(set(item[0] for item in res))
    res=[]
    for item in unique_names_list:
        param, value = item.split(" = ")
        prob={}
        prob[param]='True' if value=='1' else 'False'
        res.append((item,prob))

    print(res, end="\n")
    print(res.__len__())
    return res


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
        sens_vals = get_all_sensitivity_values(net,prob)  # Returns 26 values
        
        for (name_y,_,val) in sens_vals:
            sensitivity_matrix.at[name_x, name_y] = val
    
    return sensitivity_matrix
        
    
net_xdls = pysmile.Network()
        
net_xdls.read_file("Brain_Tumor_original.xdsl")

net_bif=pgmpy.readwrite.BIFReader("Brain_Tumor_original.bif").get_model()
"""
analysis=yodo(net_bif,{'C':'True'})

plot(net_bif,{'C':'True'})
print(analysis)
sv = analysis[('B','MC')]['derivative']

print(sv)
"""
yodo_params=get_all_params_for_yodo(net_xdls)

marginal_outcomes=get_all_marginal_outcomes(net_xdls,[('C','False')])

#get_sensitivity_values(net,yodo_params)


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
