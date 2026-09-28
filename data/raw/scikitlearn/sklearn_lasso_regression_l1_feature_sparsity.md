# Lasso Regression: L1 Regularization and Feature Selection

**Doc ID:** `sklearn_lasso_regression_l1_feature_sparsity`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Drive uninformative feature coefficients strictly to zero using L1 regularization for sparse models.

---

## Lasso Formulation
Lasso adds an L1 penalty to the loss:
$$\min_w \frac{1}{2 n} \|Xw - y\|^2_2 + \alpha \|w\|_1$$

```python
from sklearn.linear_model import Lasso
import numpy as np

X = np.random.randn(50, 10)
# Only first 2 features matter
y = 2.5 * X[:, 0] - 1.8 * X[:, 1] + np.random.randn(50) * 0.1

lasso = Lasso(alpha=0.2).fit(X, y)
print("Lasso Coefs:", np.round(lasso.coef_, 2))
print("Zeroed features count:", np.sum(lasso.coef_ == 0))
```
Due to the geometry of the L1 diamond constraint, Lasso performs automated feature selection.

