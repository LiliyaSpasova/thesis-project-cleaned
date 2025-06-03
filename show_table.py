import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def format_sensitivity_table_list(dataset):
    #dataset=[dataset]
    """
    Takes a list of sensitivity triplets (each with 3 elements: [sens1, sens2, two-way]) and
    returns a pandas DataFrame with each row containing:
    Param1, Param2, Target, Sens Function 1, Sens Function 2, Two-way Sens Function.
    """
    
    def format_single(coeffs):
        coeffs = np.round(coeffs, 2)
        if len(coeffs) == 4:
            a, b, c, d = coeffs
            return f"({a}·x + {b})/({c}·x + {d})"
        elif len(coeffs) == 2:
            a, b = coeffs
            return f"{a}·x + {b}"
        else:
            return "Invalid format"

    def format_two_way(coeffs):
        coeffs = np.round(coeffs, 2)
        
        if len(coeffs) == 8:
            num = coeffs[:4]
            den = coeffs[4:]
            num_str = f"({num[0]}·xy + {num[1]}·x + {num[2]}.y + {num[3]})"
            den_str = f"({den[0]}·xy + {den[1]}·x + {den[2]}·y + {den[3]})"
            return f"{num_str} / {den_str}"
        
        elif len(coeffs) == 4:
            num = coeffs
            num_str = f"({num[0]}·xy + {num[1]}·x + {num[2]}·y + {num[3]})"
            return f"{num_str}"
        
        else:
            return "Invalid format"

    
    rows = []

    for entry in dataset:
        sens_val=entry[0]
        entry=entry[1]
        if entry is None or len(entry) != 3:
            continue  # Skip invalid entries

        sens1, sens2, twoway = entry

        param1 = sens1[1][0]
        param2 = sens2[1][0]
        target = sens1[1][1]

        sens_func1 = format_single(sens1[0][0])
        sens_func2 = format_single(sens2[0][0])
        two_way_func = format_two_way(twoway[0][0])

        rows.append({
            "Param1": param1,
            "Param2": param2,
            "Sensitivity value":sens_val,
            "Target": target,
            "Sens Function 1": sens_func1,
            "Sens Function 2": sens_func2,
            "Two-way Sens Function": two_way_func
        })

    return pd.DataFrame(rows)

def save_table_as_image(df, output_path="sensitivity_table.png"):
    fig, ax = plt.subplots(figsize=(20, 2 + len(df)*0.8))
    ax.axis('off')
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.scale(1.2, 1.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()