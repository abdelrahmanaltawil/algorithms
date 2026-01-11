# Numerical Integration

Numerical integration (quadrature) approximates the definite integral of a function when an analytical solution is difficult or impossible to obtain.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [01_left_point_rule.ipynb](./01_left_point_rule.ipynb) | Left Riemann sum implementation |
| [02_right_point_rule.ipynb](./02_right_point_rule.ipynb) | Right Riemann sum implementation |
| [03_midpoint_rule.ipynb](./03_midpoint_rule.ipynb) | Midpoint rule implementation |

## 🔑 Key Formulas

### Left Point Rule
$$\int_a^b f(x)\,dx \approx \sum_{i=0}^{n-1} f(x_i) \cdot \Delta x$$

### Right Point Rule
$$\int_a^b f(x)\,dx \approx \sum_{i=1}^{n} f(x_i) \cdot \Delta x$$

### Midpoint Rule
$$\int_a^b f(x)\,dx \approx \sum_{i=0}^{n-1} f\left(\frac{x_i + x_{i+1}}{2}\right) \cdot \Delta x$$

## 📊 Method Comparison

| Method | Sample Point | Order of Error |
|--------|-------------|----------------|
| Left Point Rule | Left endpoint | O(h) |
| Right Point Rule | Right endpoint | O(h) |
| Midpoint Rule | Center of interval | O(h²) |

The **Midpoint Rule** generally provides better accuracy for the same number of subintervals.
