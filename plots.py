import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_rational_functions(plots_params,evidence_available, x_range=(0, 1),num_points=100,points=None,labels=None, ax=None):
    x = np.linspace(x_range[0], x_range[1], num_points)
    
    # Plot each rational function
    if evidence_available:
        # Plot each rational function
        for i, (a, b, c, d) in enumerate(plots_params):
            # Calculate y-values, handling cases where denominator is zero
            y = (a * x + b) / (c * x + d)
            ax.plot(
                x,
                y,
                label=(
                    f"Resulting function {i+1}:({a:.2f}*x + {b:.2f}) /\n"
                    f"                    ({c:.2f}*x + {d:.2f})"
                )
            )
    else:
        # Plot each linear function (ax + b)
        for i, (a, b) in enumerate(plots_params):
            y = a * x + b
            ax.plot(x, y, label=f"Resulting function: {i+1}: {a}*x + {b}")

    #y_additional = (0.993 * x - 0.001)/(x+0.786)
    #plt.plot(x, y_additional, label="Original funciton, as defined in the syllabus", linestyle='--', color='red')
    


    if points:
        for (px, py) in points:
            plt.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
    
    # Set plot labels and legend
    ax.set_ylim(0, 1)  
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_title('Result plots')
    ax.legend()
    ax.grid(True)


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
    labels=['x','y','f(x,y)'],
    ax1=None,
    ax2=None
):
    # Create grid for 3D plot and contour plot
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    X, Y = np.meshgrid(x, y)


    # Plot each function on the 3D surface
    for i, params in enumerate(plots_params):
        if evidence_available:
            a, b, c, d, e, f, g, h = params
            denominator = e * X * Y + f * X + g * Y + h
            Z = (a * X * Y + b * X + c * Y + d) / denominator
            Z[np.abs(denominator) < 1e-6] = np.nan
            ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.6)

            # Add text showing the formula
            formula = (
                f"({a:.2f}*x*y + {b:.2f}*x + {c:.2f}*y + {d:.2f})\n"
                f"/ ({e:.2f}*x*y + {f:.2f}*x + {g:.2f}*y + {h:.2f})"
            )
            ax1.text2D(0.05, 0.95 - 0.05*i, formula, transform=ax1.transAxes)
        else:
            a, b, c, d = params
            Z = a * X * Y + b * X + c * Y + d
            ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.6)

            formula = f"{a:.2f}*x*y + {b:.2f}*x + {c:.2f}*y + {d:.2f}"
            ax1.text2D(0.05, 0.95 - 0.05*i, formula, transform=ax1.transAxes)    
            ax1.set_xlabel(labels[0])
    ax1.set_ylabel(labels[1])
    ax1.set_zlabel(labels[2])
    ax1.set_zlim(0, 1)  # Ensure full vertical range in 3D plot


   # ax1.set_title('3D Surface Plot of Functions')

    # Contour Plot (Second subplot)

        # Contour Plot (Second subplot) - updated for filled contours and colorbars
    for i, params in enumerate(plots_params):
        if evidence_available:
            a, b, c, d, e, f, g, h = params
            denominator = e * X * Y + f * X + g * Y + h
            Z = (a * X * Y + b * X + c * Y + d) / denominator
            Z[np.abs(denominator) < 1e-6] = np.nan
            title = (
                f"({a:.2f}xy + {b:.2f}x + {c:.2f}y + {d:.2f}) /\n"
                f"({e:.2f}xy + {f:.2f}x + {g:.2f}y + {h:.2f})"
            )
        else:
            a, b, c, d = params
            Z = a * X * Y + b * X + c * Y + d
            title = f"{a:.2f}xy + {b:.2f}x + {c:.2f}y + {d:.2f}"

    cs = ax2.contourf(X, Y, Z, levels=20, cmap='viridis')
    ax2.set_xlabel(labels[0])
    ax2.set_ylabel(labels[1])
    plt.colorbar(cs, ax=ax2)

    # If points are provided, add them to the plot
    if points:
        for (px, py) in points:
            ax2.scatter(px, py, color='green', marker='o', label=f"Point ({px}, {py})")
        ax2.legend()

