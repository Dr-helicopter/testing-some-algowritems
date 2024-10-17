import numpy as np



def calculate_eigenvalues(matrix):
    """
    This function takes a square 2D list (matrix), calculates its eigenvalues,
    and returns the real part of the rounded eigenvalues as a Python list.

    Parameters:
    matrix (list of lists): A square 2D list representing the matrix.

    Returns:
    list: A list containing the real part of the rounded eigenvalues.
    """
    # Convert the 2D list into a NumPy array
    matrix_np = np.array(matrix)

    # Check if the matrix is square
    rows, cols = matrix_np.shape
    if rows != cols:
        raise ValueError("The input matrix must be square (n x n).")

    # Calculate eigenvalues using NumPy's linalg.eigvals function
    eigenvalues = np.linalg.eigvals(matrix_np)

    # Extract the real part of the eigenvalues, round them, and convert to a Python list
    real_eigenvalues = np.real(eigenvalues)
    rounded_eigenvalues = np.round(real_eigenvalues, 2).tolist()

    return rounded_eigenvalues