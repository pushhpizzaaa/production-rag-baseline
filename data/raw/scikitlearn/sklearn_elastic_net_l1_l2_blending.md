# ElasticNet: Blending L1 and L2 Regularization

**Doc ID:** `sklearn_elastic_net_l1_l2_blending`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Combine the feature selection of Lasso with the grouping effect of Ridge using ElasticNet.

---

## ElasticNet Formulation
ElasticNet minimizes:
$$\min_w \frac{1}{2 n} \|Xw - y\|^2_2 + \alpha \cdot \rho \|w\|_1 + \frac{\alpha (1 - \rho)}{2} \|w\|^2_2$$
Where $\rho$ is `l1_ratio` ($0 \le \rho \le 1$).

```python
from sklearn.linear_model import ElasticNet
import numpy as np

X = np.random.randn(100, 8)
y = np.random.randn(100)

enet = ElasticNet(alpha=0.1, l1_ratio=0.7).fit(X, y)
print("ElasticNet coefficients:", enet.coef_)
```
Overcomes Lasso's limitation when dealing with highly correlated feature clusters by selecting groups together.

