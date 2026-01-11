# Approximation

Approximation methods for fitting functions to data, representing signals, and regression.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [01_linear_least_squares.ipynb](./01_linear_least_squares.ipynb) | Linear least squares curve fitting |
| [02_nonlinear_least_squares.ipynb](./02_nonlinear_least_squares.ipynb) | Gauss-Newton and Levenberg-Marquardt methods |
| [03_polynomial_approximation.ipynb](./03_polynomial_approximation.ipynb) | Chebyshev polynomial approximation |
| [04_spline_approximation.ipynb](./04_spline_approximation.ipynb) | Natural cubic and smoothing splines |
| [05_regularized_regression.ipynb](./05_regularized_regression.ipynb) | Ridge and Lasso regression |
| [fourier_series.ipynb](./fourier_series.ipynb) | Fourier series representation of periodic functions |

## 🔑 Key Concepts

**Least Squares** minimizes the sum of squared residuals:
$$\min_\beta \sum_{i=1}^n (y_i - \hat{f}(x_i, \beta))^2$$

**Chebyshev Polynomials** provide near-optimal polynomial approximation.

**Regularization** adds a penalty term to prevent overfitting:
- **Ridge** (L2): $\lambda\|\beta\|_2^2$
- **Lasso** (L1): $\lambda\|\beta\|_1$

## 📖 Further Reading

- [Wikipedia: Least Squares](https://en.wikipedia.org/wiki/Least_squares)
- [Wikipedia: Chebyshev Polynomials](https://en.wikipedia.org/wiki/Chebyshev_polynomials)
- [Wikipedia: Regularization](https://en.wikipedia.org/wiki/Regularization_(mathematics))
