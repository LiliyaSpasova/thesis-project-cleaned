import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_rational_functions(plots_params,evidence_available, x_range=(0, 1),num_points=100,points=None):
    x = np.linspace(x_range[0], x_range[1], num_points)
    
    plt.figure(figsize=(8, 6))
    
    # Plot each rational function
    if evidence_available:
        # Plot each rational function
        for i, (a, b, c, d) in enumerate(plots_params):
            # Calculate y-values, handling cases where denominator is zero
            y = (a * x + b) / (c * x + d)
            plt.plot(x, y, label=f"Resulting function: {i+1}: ({a}*x + {b}) / ({c}*x + {d})")
    else:
        # Plot each linear function (ax + b)
        for i, (a, b) in enumerate(plots_params):
            y = a * x + b
            plt.plot(x, y, label=f"Resulting function: {i+1}: {a}*x + {b}")

    #y_additional = (0.993 * x - 0.001)/(x+0.786)
    #plt.plot(x, y_additional, label="Original funciton, as defined in the syllabus", linestyle='--', color='red')
    


    if points:
        for (px, py) in points:
            plt.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
    
    # Set plot labels and legend
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Result plots')
    plt.legend()
    plt.grid(True)
    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

def plot_3d_rational_functions(
    plots_params, 
    evidence_available=True,
    x_range=(0, 1), 
    y_range=(0, 1), 
    num_points=100, 
    points=None,
    labels=['x','y','f(x,y)']
):
    # Create grid for 3D plot and contour plot
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)

    # Set up figure and axes
    fig = plt.figure(figsize=(14, 6))

    # 3D Plot (First subplot)
    ax1 = fig.add_subplot(121, projection='3d')

    # Plot each function on the 3D surface
    for i, params in enumerate(plots_params):
        if evidence_available:
            # For rational functions, expect 8 parameters
            a, b, c, d, e, f, g, h = params
            denominator = e * X * Y + f * X + g * Y + h
            Z = (a * X * Y + b * X + c * Y + d) / denominator
            Z[np.abs(denominator) < 1e-6] = np.nan  # Handle singularities
        else:
            # For linear functions, expect 4 parameters
            a, b, c, d = params
            Z = a * X * Y + b * X + c * Y + d

        ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.6)

    ax1.set_xlabel(labels[0])
    ax1.set_ylabel(labels[1])
    ax1.set_zlabel(labels[2])
   # ax1.set_title('3D Surface Plot of Functions')

    # Contour Plot (Second subplot)
    ax2 = fig.add_subplot(122)

    for i, params in enumerate(plots_params):
        if evidence_available:
            # For rational functions, expect 8 parameters
            a, b, c, d, e, f, g, h = params
            denominator = e * X * Y + f * X + g * Y + h
            Z = (a * X * Y + b * X + c * Y + d) / denominator
            Z[np.abs(denominator) < 1e-6] = np.nan  # Handle singularities
        else:
            # For linear functions, expect 4 parameters
            a, b, c, d = params
            Z = a * X * Y + b * X + c * Y + d

        # Create a contour plot using your working approach
        contour = ax2.contour(X, Y, Z, cmap='viridis')

    ax2.set_xlabel(labels[0])
    ax2.set_ylabel(labels[1])
    fig.colorbar(contour, ax=ax2)

    # If points are provided, add them to the plot
    if points:
        for (px, py) in points:
            ax2.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
        ax2.legend()

    # Display plots
    plt.tight_layout()
    plt.show()
