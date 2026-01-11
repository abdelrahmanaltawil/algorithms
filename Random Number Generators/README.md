# Random Number Generators

Random number generation is fundamental to simulations, statistical sampling, and numerical methods.

## 📁 Contents

| Folder | Description |
|--------|-------------|
| [pseudo-random](./pseudo-random/) | Deterministic sequences appearing random (e.g., LCG) |
| [quasi-random](./quasi-random/) | Low-discrepancy sequences for uniform space filling |

## 🔑 Quick Comparison

| Property | Pseudo-Random | Quasi-Random |
|----------|--------------|--------------|
| Reproducibility | ✅ (with seed) | ⚠️ (position-dependent) |
| Speed | Fast | Fast |
| Uniformity in high dimensions | Variable | Excellent |
| Pattern-free | May cluster | Structured but uniform |
| Best for | General simulation | Numerical integration |

## 🎯 Choosing the Right Generator

| Use Case | Recommended |
|----------|-------------|
| Speed and reproducibility needed | Pseudo-Random |
| Random-like properties for general simulation | Pseudo-Random |
| Even distribution in high dimensions | Quasi-Random |
| Numerical integration | Quasi-Random |
| Faster convergence requirements | Quasi-Random |
