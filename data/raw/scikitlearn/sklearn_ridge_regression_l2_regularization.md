# Ridge Regression: L2 Regularization and Multicollinearity

**Doc ID:** `sklearn_ridge_regression_l2_regularization`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Mitigate multicollinearity and model overfitting by adding an L2 penalty on coefficient magnitudes.

---

## Ridge Formulation
Ridge adds a squared L2 norm penalty to the loss function:
$$\min_w \|Xw - y\|^2_2 + \alpha \|w\|^2_2$$

```python
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.datasets import make_regression

X, y = make_regression(n_samples=100, n_features=10, noise=0.1, random_state=42)

# Automatically tune alpha via generalized cross-validation
ridge = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0]).fit(X, y)
print("Optimal Alpha:", ridge.alpha_)
print("Model Score R2:", ridge.score(X, y))
```
L2 regularization shrinks coefficients toward zero but never forces them to exact zero.

