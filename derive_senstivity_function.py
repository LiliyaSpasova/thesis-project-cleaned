import pysmile
import pysmile_license
import coefficient_calculator
import numpy as np
from plots import *
from linear_system_solver import *
from get_distribution import *
import itertools
import random


def update_cpt_with_epsilon(net,parameters,target,num_variations):
    res=[]
    value_combinations=generate_value_combinations(parameters.__len__(),num_variations)
    target_node_name, target_node_value = target['probability']
    target_cpt_dict= get_cpt_dict(net, net.get_node(target_node_name))

    parameters_info =extract_parameters_info(net,parameters)
    for variation in value_combinations:
        coordinates=[]
        for param_index,p in enumerate(parameters_info):
            cpt = p['cpt']
            true_index=p['true_index']
            false_index=p['false_index']
            parameter_node_name=p['name']
            parameter_node_value=p['parameter_node_value']
            distribution=p['distribution']
            cpt[true_index]=variation[param_index]
            cpt[false_index]=1-variation[param_index]
            net.set_node_definition(parameter_node_name,cpt)
            coordinates.append(cpt[ distribution[parameter_node_value][1]])
        if target['given'] is not None:
            for  key, value in target['given']:
                net.set_evidence(key,value)
        net.update_beliefs()
        beliefs = net.get_node_value(target_node_name)
        falsy_values = ['false', 'off', 'no', 'absent']

        if target_node_value.lower() in falsy_values:
            coordinates.append(beliefs[1])
        else:
            coordinates.append(beliefs[0])
        res.append(tuple(coordinates))
    return res

def round_point_values(values):
    res=[]
    for val in values:
        val = val[:-1] + (round(val[-1], 4),)
        res.append(val)
    return res
def round_plot_params(values, precision=4):
    res = []
    for val_tuple in values:
        # Round each element in the tuple to the specified precision
        rounded_tuple = tuple(round(v, precision) for v in val_tuple)
        res.append(rounded_tuple)
    return res

def calculate_variations_needed(parameters,target):
    num_parameters=parameters.__len__()
    res=pow(2,num_parameters)
    if target['given'] is not None and len(target['given'])>0:
        res=res*2
    return res

def extract_parameters_info(net,parameters):
    structured_data = []
    for parameter in parameters:
        # Extract parameter details
        parameter_node_name, parameter_node_value = parameter['probability']
    
        # Generate all combinations for the current node
        cpt = net.get_node_definition(parameter_node_name)  # Placeholder function call
        distribution = get_distribution(net, parameter)    # Placeholder function call
        truthy_values = ['true', 'on', 'yes', 'present','presen']
        falsy_values = ['false', 'off', 'no', 'absent']

        # Normalize the keys in the distribution for lookup
        normalized_distribution = {key.lower(): value for key, value in distribution.items()}

        _, true_index = next((v for k, v in normalized_distribution.items() if k in truthy_values), (None, None))
        _, false_index = next((v for k, v in normalized_distribution.items() if k in falsy_values), (None, None))

        # Save structured data for each combination
        structured_data.append({
                'name': parameter_node_name,
                'true_index': true_index,
                'false_index': false_index,
                'distribution':distribution,
                'parameter_node_value':parameter_node_value,
                'cpt': cpt  # Assuming you want the entire CPT structure
            })
    
    return structured_data

def generate_value_combinations(num_parameters,num_combinations):
    probability_values=[0.1,0.4,0.7,0.9]
    #if num_parameters==1:
      #  selected_combinations = random.sample(probability_values, num_combinations)
        #return selected_combinations
    all_combinations = list(itertools.product(probability_values, repeat=num_parameters))
    
    # Check if num_combinations exceeds available combinations

    if num_combinations > len(all_combinations):
        raise ValueError(f"Requested {num_combinations} combinations, but only {len(all_combinations)} are available.")
    
    # Randomly select the desired number of combinations
    selected_combinations = random.sample(all_combinations, num_combinations)
    
    return selected_combinations
def generate_labels(parameters, target):
    labels = []
    truthy_values = ['on', 'true', 'present', 'yes']

    if isinstance(parameters, dict):
        parameters = [parameters]

    for param in parameters:
        if param['probability'][1].lower() in truthy_values:
            prob_var = param['probability'][0]
        else:
            prob_var = '-' + param['probability'][0]
        
        given_vars = param.get('given', [])
        
        if given_vars:
            given_str = '^'.join([
                gv[0] if gv[1].lower() in truthy_values else '-' + gv[0]
                for gv in given_vars
            ])
            labels.append(f'P({prob_var}|{given_str})')
        else:
            labels.append(f'P({prob_var})')

    # Handle target separately
    if target['probability'][1].lower() in truthy_values:
        target_var = target['probability'][0]
    else:
        target_var = '-' + target['probability'][0]
    
    target_vars = target.get('given', [])
    
    if target_vars:
        given_str = '^'.join([
            gv[0] if gv[1].lower() in truthy_values else '-' + gv[0]
            for gv in target_vars
        ])
        labels.append(f'P({target_var}|{given_str})')
    else:
        labels.append(f'P({target_var})')

    return labels



def plot(parameters,points,evidence_available,labels,ax1,ax2=None,plots=True):
    
    if isinstance(parameters, dict):
        parameters = [parameters]

    plots_params=[]
    coefficients=[]
    b=[]
    if parameters.__len__()==1:
        for (x,y) in points:
            coefficients.append(coefficient_calculator.get_coefficients_1_way(x,y,evidence_available))
            if not evidence_available:
                b.append(y)
        if evidence_available:
            plots_params.append(solve_system(coefficients))
        else:
            plots_params.append(solve_system_without_evidence(coefficients,b))
        if plots:
            plot_rational_functions(plots_params=round_plot_params(plots_params),evidence_available=evidence_available,labels=labels,ax=ax1)
        else:
            return (plots_params,labels)
    else:
        for (x,y,z) in points:
            coefficients.append(coefficient_calculator.get_coefficients_2_way(x,y,z,evidence_available))
            if not evidence_available:
                b.append(z)
        if evidence_available:
            plots_params.append(solve_system(coefficients))
        else:
            plots_params.append(solve_system_without_evidence(coefficients,b))
        if plots:
            plot_3d_rational_functions(plots_params=plots_params,evidence_available=evidence_available,labels=labels,ax1=ax1,ax2=ax2)
        else:
            return (plots_params,labels)

import matplotlib.pyplot as plt

def get_all_functions(net, params, plots):
    all_values = []

    target = params[0]
    parameters = params[1]

    # Determine if evidence is available
    evidence_available = 'given' in target and len(target['given'])>0

    # Single parameter case
    if len(parameters) == 1:
        if isinstance(parameters, dict):
            parameters = [parameters]

        labels = generate_labels(parameters, target)
        needed_variations = calculate_variations_needed(parameters, target)
        points = update_cpt_with_epsilon(net, parameters, target, needed_variations)
        points = round_point_values(points)

        if plots:
            fig, ax = plt.subplots(figsize=(12, 10))
            plot(parameters, points, evidence_available, labels, ax1=ax)
            plt.tight_layout()
            plt.show()
            return
        else:
            result = plot(parameters, points, evidence_available, labels, ax1=None, plots=False)
            all_values.append(result)
            return all_values

    # Multi-parameter case (2 parameters + joint plot)
    if plots:
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
        ax_3d = fig.add_subplot(2, 2, 3, projection='3d')

    for i, p in enumerate(parameters):
        if isinstance(p, dict):
            p = [p]

        labels = generate_labels(p, target)
        needed_variations = calculate_variations_needed(p, target)
        points = update_cpt_with_epsilon(net, p, target, needed_variations)
        points = round_point_values(points)

        if plots:
            plot(p, points, evidence_available, labels, ax1=axes[0, i])
        else:
            result = plot(p, points, evidence_available, labels, ax1=None, plots=False)
            all_values.append(result)

    # Joint 3D plot
    labels = generate_labels(parameters, target)
    needed_variations = calculate_variations_needed(parameters, target)
    points = update_cpt_with_epsilon(net, parameters, target, needed_variations)
    points = round_point_values(points)

    if plots:
        plot(parameters, points, evidence_available, labels, ax1=ax_3d, ax2=axes[1, 1], plots=True)
        plt.tight_layout()
        plt.show()
        return
    else:
        result = plot(parameters, points, evidence_available, labels, ax1=None, ax2=None, plots=False)
        all_values.append(result)
        return all_values
