import os
import numpy as np
from scipy.fftpack import ifft2


def lagrange(x, y, x_int):
    """Interpolates a value using the 'Lagrange polynomial'.
    Args:
        x: an array containing x values.
        y: an array containing y values.
        x_int: value to interpolate.
    Returns:
        y_int: interpolated value.
    """
    n = x.size
    y_int = 0

    for i in range(0, n):
        p = y[i]
        for j in range(0, n):
            if i != j:
                p = p * (x_int - x[j]) / (x[i] - x[j])
        y_int = y_int + p

    return [y_int]


def neville(x, y, x_int):
    """Interpolates a value using the 'Neville polynomial'.
    Args:
        x: an array containing x values.
        y: an array containing y values.
        x_int: value to interpolate.
    Returns:
        y_int: interpolated value.
        q: coefficients matrix.
    """
    n = x.size
    q = np.zeros((n, n - 1))

    # Insert 'y' in the first column of the matrix 'q'
    q = np.concatenate((y[:, None], q), axis=1)

    for i in range(1, n):
        for j in range(1, i + 1):
            q[i, j] = ((x_int - x[i - j]) * q[i, j - 1] -
                       (x_int - x[i]) * q[i - 1, j - 1]) / (x[i] - x[i - j])

    y_int = q[n - 1, n - 1]
    return [y_int, q]


def interpolation(X, Y, value):
    vandermonde = lambda x, y: [1, x, y, x**2, y**2]
    vandermonde_matrix = np.array([vandermonde(x, y) for x,y in zip(X,Y)])

    coefficients = np.linalg.solve(vandermonde_matrix, value)
    a_0, a_1, a_2, a_3, a_4 = coefficients
    interpulant = lambda x,y : a_0 + a_1*x + a_2*y + a_3*x**2 + a_4*y**2

    # interpulant extrema
    extrema_x, extrema_y = np.linalg.solve(np.array([[2*a_3, 0], [0, 2*a_4]]),
                              np.array([-a_1, -a_2]))
    extrema = (extrema_x, extrema_y, interpulant(extrema_x, extrema_y))

    return interpulant, extrema


if __name__ == "__main__":
    input_folder = r"./Post_Processing/Data/ratio_1"
    file_name = "w_k_0001000.npz"

    file_path = os.path.join(input_folder, file_name)
    compressed_file = np.load(file_path) 
    w_k, time = compressed_file["arr_0"], compressed_file["arr_1"]

    w = np.real(ifft2(w_k))