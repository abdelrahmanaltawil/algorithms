# Approximation

**Approximation Theory** is a branch of mathematics concerned with how functions can best be approximated with simpler functions, and with quantitatively characterizing the errors introduced thereby. In the context of this repository, it covers methods for fitting models to data (regression), representing complex signals with simpler basis functions (Fourier, Wavelets), and interpolating between known data points.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [linear_least_squares.ipynb](./linear_least_squares.ipynb) | Linear least squares curve fitting |
| [nonlinear_least_squares.ipynb](./nonlinear_least_squares.ipynb) | Gauss-Newton and Levenberg-Marquardt methods |
| [polynomial_approximation.ipynb](./polynomial_approximation.ipynb) | Chebyshev polynomial approximation |
| [spline_approximation.ipynb](./spline_approximation.ipynb) | Natural cubic and smoothing splines |
| [regularized_regression.ipynb](./regularized_regression.ipynb) | Ridge and Lasso regression |
| [fourier_series.ipynb](./fourier_series.ipynb) | Fourier series representation of periodic functions |
| [taylor_series.ipynb](./taylor_series.ipynb) | Taylor and Maclaurin series approximation |

## 🔑 Key Concepts
### Least Squares
Minimizes the sum of squared residuals to find the best fit:
$$ \min_\beta \| y - X\beta \|_2^2 $$
The solution is given by the **Normal Equations**: $\beta = (X^T X)^{-1} X^T y$. Geometrically, this projects the data vector $y$ onto the column space of $X$.

### Polynomial vs. Spline Approximation
- **Polynomials**: Good for local approximation or smooth global functions, but high-degree polynomials can oscillate wildly (**Runge's phenomenon**).
- **Chebyshev Polynomials**: Roots of these polynomials are used as interpolation nodes to minimize the maximum error (minimax interpolation).
- **Splines**: Piecewise polynomials (usually cubic) connected at "knots". They avoid oscillation and ensuring smoothness (continuous derivatives) across knots.

### Regularization
Adds a penalty term to the loss function to prevent overfitting, effectively constraining the magnitude of coefficients:
- **Ridge (L2)**: $\text{Loss} + \lambda\|\beta\|_2^2$. Shrinks coefficients independently; good for handling multicollinearity.
- **Lasso (L1)**: $\text{Loss} + \lambda\|\beta\|_1$. Promotes *sparsity* (sets some coefficients to exactly zero), performing feature selection.

### Fourier Series
Represents periodic functions as a sum of orthogonal sine and cosine basis functions.
$$ f(t) \approx \frac{a_0}{2} + \sum_{n=1}^{N} \left[ a_n \cos(n\omega t) + b_n \sin(n\omega t) \right] $$
Because basis functions are orthogonal, coefficients can be computed independently via integration.

### Taylor Series
Approximates a differentiable function using a polynomial constructed from its derivatives at a single point (local approximation).
$$f(x) \approx P_n(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!} (x - a)^k$$

## 📖 Further Reading

- [Wikipedia: Least Squares](https://en.wikipedia.org/wiki/Least_squares)
- [Wikipedia: Chebyshev Polynomials](https://en.wikipedia.org/wiki/Chebyshev_polynomials)
- [Wikipedia: Regularization](https://en.wikipedia.org/wiki/Regularization_(mathematics))
- [Wikipedia: Taylor Series](https://en.wikipedia.org/wiki/Taylor_series)
