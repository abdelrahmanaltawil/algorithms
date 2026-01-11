# Linear Algebra

 numerical methods for solving systems of linear equations ($Ax = b$).

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [direct-solvers.ipynb](./direct-solvers.ipynb) | Direct methods including Gaussian Elimination, LU Decomposition, and Cholesky Decomposition. |
| [iterative-solvers.ipynb](./iterative-solvers.ipynb) | Iterative methods including Stationary (Jacobi, Gauss-Seidel, SOR) and Krylov Subspace (Conjugate Gradient) solvers. |

## 🔑 Key Concepts

### Direct Solvers
Methods that compute the exact solution (within machine precision) in a finite number of steps.
- **Gaussian Elimination**: Reduces matrix to row echelon form.
- **LU Decomposition**: Factors $A$ into Lower ($L$) and Upper ($U$) triangular matrices.
- **Cholesky Decomposition**: Factors symmetric positive-definite $A$ into $LL^T$.

### Iterative Solvers
Methods that generate a sequence of approximations to the solution.
- **Stationary Methods**: Express the solution as $x^{(k+1)} = Mx^{(k)} + c$ (e.g., Jacobi, Gauss-Seidel).
- **Krylov Subspace Methods**: Minimize residual over a subspace basis (e.g., Conjugate Gradient).
