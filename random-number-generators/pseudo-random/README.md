# Pseudo-Random Number Generation

Pseudo-random number generators (PRNGs) are deterministic algorithms that produce sequences of numbers that approximate the properties of random numbers.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [linear_congruential_generator.ipynb](./linear_congruential_generator.ipynb) | Classic LCG implementation and analysis |

## 🔑 Linear Congruential Generator (LCG)

$$X_{n+1} = (aX_n + c) \mod m$$

Where:
- **a**: Multiplier
- **c**: Increment
- **m**: Modulus
- **X₀**: Seed value

### Properties

| Aspect | Description |
|--------|-------------|
| Period | At most m |
| Speed | Very fast |
| Quality | Depends on parameter choice |
| Use case | Simple simulations, games |

## ⚠️ Limitations

- Not suitable for cryptographic applications
- Sequential correlation in higher dimensions
