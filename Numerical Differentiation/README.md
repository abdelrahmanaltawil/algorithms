# Numerical Differentiation

Numerical differentiation approximates derivatives of functions using discrete data points. These methods are fundamental when analytical derivatives are unavailable or impractical.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [01_forward_diffrentionation.ipynb](./01_forward_diffrentionation.ipynb) | Forward difference scheme |
| [02_backward_diffrentionation.ipynb](./02_backward_diffrentionation.ipynb) | Backward difference scheme |
| [03_central_diffrentionation.ipynb](./03_central_diffrentionation.ipynb) | Central difference scheme |

## 🔑 Key Methods

### Forward Difference
$$f'(x) \approx \frac{f(x+h) - f(x)}{h}$$

### Backward Difference
$$f'(x) \approx \frac{f(x) - f(x-h)}{h}$$

### Central Difference
$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$

## 📊 Accuracy Comparison

| Method | Order of Error |
|--------|----------------|
| Forward Difference | O(h) |
| Backward Difference | O(h) |
| Central Difference | O(h²) |

The **Central Difference** method provides higher accuracy but requires function values on both sides of the point.
