import numpy as np


# Calculate the SVD of the coefficient matrix


def solve_system(coefficients):
    U, S, Vh = np.linalg.svd(coefficients)

# Find the null space of the matrix (solutions to Ax = 0)
    null_space = Vh[np.where(S < 0.05)].T  # Adjust the tolerance as needed

    # Generate a non-trivial solution by scaling a vector from the null space
    solution = null_space[:, 0]   # Scale the first vector, adjust the scale as needed

    return solution



# Define the coefficients matrix
coefficients = np.array([
    [0.75, 1, -0.36, -0.48],
    [0.7, 1, -0.329, -0.47],
    [0.65, 1, -0.293, -0.45],
    [0.6, 1, -0.258, -0.43]
])

import numpy as np

# Calculate the SVD of the coefficient matrix and solve Ax = b
def solve_system_without_evidence(coefficients, b):
    # Perform SVD on the coefficient matrix
    U, S, Vh = np.linalg.svd(coefficients)

    # Invert the singular values (regularization to avoid division by zero)
    tolerance = 1e-5  # Adjust tolerance as needed for numerical stability
    S_inv = np.zeros_like(S)
    
    # Invert the singular values, replacing very small values with zeros (for numerical stability)
    S_inv[S > tolerance] = 1 / S[S > tolerance]
    
    # Solve the system using the pseudoinverse formula: x = V * S_inv * U.T * b
    solution = Vh.T @ np.diag(S_inv) @ U.T @ b
    
    return solution



coefficients=np.array([
[0.7,1],
[0.4,1]
])
# Define the right-hand side vector b (for example, a non-zero vector)
b = np.array([0.335,0.326])


