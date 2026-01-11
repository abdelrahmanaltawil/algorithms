# Differential Equations

Numerical methods for solving ordinary differential equations (ODEs) and optimal control problems.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [euler_method.ipynb](./euler_method.ipynb) | Euler's method for first-order ODEs |
| [runge_kutta_method.ipynb](./runge_kutta_method.ipynb) | Fourth-order Runge-Kutta method |
| [forward_backward_sweep.ipynb](./forward_backward_sweep.ipynb) | Optimal control using forward-backward sweep |

## 🔑 Key Methods

### Euler's Method
$$y_{n+1} = y_n + h \cdot f(t_n, y_n)$$

### Runge-Kutta (4th Order)
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

## 📊 Accuracy Comparison

| Method | Order of Error |
|--------|----------------|
| Euler | O(h) |
| Runge-Kutta 4 | O(h⁴) |

## 📖 Further Reading

- [Wikipedia: Euler method](https://en.wikipedia.org/wiki/Euler_method)
- [Wikipedia: Runge-Kutta methods](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)
