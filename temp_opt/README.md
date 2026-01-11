# Estimation

**Estimation Theory** is a branch of statistics that deals with estimating the values of parameters based on measured empirical data that has a random component. The parameters describe an underlying physical setting in such a way that their value affects the distribution of the measured data. The goal is to arrive at an estimator $\hat{\theta}$ that approximates the true parameter $\theta$ as closely as possible.

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [maximum_likelihood_estimation.ipynb](./maximum_likelihood_estimation.ipynb) | Maximum Likelihood Estimation (MLE) with examples |

## 🔑 Key Concepts

### Maximum Likelihood Estimation (MLE)
MLE estimates parameters $\theta$ by finding the values that maximize the probability of observing the given data $X$.
$$\hat{\theta}_{MLE} = \arg\max_{\theta} L(\theta|X)$$
where $L(\theta|X) = \prod_{i=1}^{n} f(x_i|\theta)$.
In practice, we often maximize the **Log-Likelihood** $\ell(\theta) = \sum \log f(x_i|\theta)$ because sums are easier to differentiate than products, and the logarithm is a monotonically increasing function.

### Properties of Estimators
Good estimators often share these properties:
- **Unbiasedness**: $E[\hat{\theta}] = \theta$. On average, the estimator hits the true parameter value.
- **Consistency**: $\hat{\theta} \xrightarrow{P} \theta$ as sample size $n \to \infty$. With enough data, the estimate converges to the truth.
- **Efficiency**: Among unbiased estimators, the one with the lowest variance is most efficient (see Cramér-Rao bound).

## 📖 Further Reading

- [Wikipedia: Maximum Likelihood Estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)
- [Wikipedia: Statistical Inference](https://en.wikipedia.org/wiki/Statistical_inference)
