# Stochastic Processes

Simulations and analyses of random processes in continuous and discrete time.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [brownian_motion.ipynb](./brownian_motion.ipynb) | Brownian motion (Wiener process) simulation |
| [markov_chains.ipynb](./markov_chains.ipynb) | Discrete-time Markov chain analysis |
| [random_walk.ipynb](./random_walk.ipynb) | Random walk simulations in various dimensions |

## 🔑 Key Concepts

### Brownian Motion
A continuous-time stochastic process with:
- $W(0) = 0$
- Independent increments
- $W(t) - W(s) \sim \mathcal{N}(0, t-s)$

### Markov Chains
A memoryless stochastic process where future states depend only on the current state:
$$P(X_{n+1} = j | X_n = i, X_{n-1}, \ldots) = P(X_{n+1} = j | X_n = i)$$

### Random Walk
A discrete stochastic process defined as:
$$S_n = \sum_{i=1}^{n} X_i$$

## 📖 Further Reading

- [Wikipedia: Brownian motion](https://en.wikipedia.org/wiki/Brownian_motion)
- [Wikipedia: Markov chain](https://en.wikipedia.org/wiki/Markov_chain)
