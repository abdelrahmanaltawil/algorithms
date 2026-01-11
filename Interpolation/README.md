# Interpolation

In the mathematical field of numerical analysis, **interpolation** is a type of estimation, a method of constructing new data points within the range of a discrete set of known data points.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [lagrange_polynomial.ipynb](./lagrange_polynomial.ipynb) | Polynomial interpolation using Lagrange basis polynomials |

## 🔑 Key Concepts

### Lagrange Polynomial
The Lagrange interpolating polynomial is the unique polynomial of lowest degree that interpolates a given set of data points. For a set of points $(x_j, y_j)$, it is defined as:

$$ L(x) = \sum_{j=0}^{k} y_j \ell_j(x) $$

where $\ell_j(x)$ are the Lagrange basis polynomials:

$$ \ell_j(x) = \prod_{i=0, i \neq j}^{k} \frac{x - x_i}{x_j - x_i} $$
