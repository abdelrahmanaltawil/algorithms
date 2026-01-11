# Quasi-Random Number Generation

Quasi-random sequences (low-discrepancy sequences) fill sample space more evenly than pseudo-random sequences, making them ideal for numerical integration and optimization.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [additive_recurrence_sequence.ipynb](./additive_recurrence_sequence.ipynb) | Weyl/additive recurrence sequence implementation |

## 🔑 Additive Recurrence Sequence

$$x_n = \{n \cdot \alpha\}$$

Where:
- **{·}** denotes the fractional part
- **α** is an irrational number (often the golden ratio φ = (√5 - 1)/2)

### Properties

| Aspect | Description |
|--------|-------------|
| Discrepancy | O(log n / n) - optimal for 1D |
| Simplicity | Very easy to implement |
| Use case | Numerical integration, sampling |

## 💡 Applications

- Quasi-Monte Carlo integration
- Uniform sampling of parameter spaces
- Computer graphics (anti-aliasing)
