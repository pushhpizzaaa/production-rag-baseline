# Gradient Boosting: Sequential Residual Learning

**Doc ID:** `sklearn_gradient_boosting_machine_gbm`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Train additive decision trees sequentially, with each new tree correcting the pseudo-residuals of predecessors.

---

## Gradient Boosting Formulation
Iteratively fits shallow trees to the negative gradient of the loss function:
$$F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)$$

```python
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)
gbm = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.8,
    random_state=42
)
gbm.fit(X, y)
print("Train Score:", gbm.score(X, y))
```
`learning_rate` shrinks the contribution of each tree, trading speed for generalization.

