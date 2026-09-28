# Linear Regression: Ordinary Least Squares (OLS)

**Doc ID:** `sklearn_linear_regression_ordinary_least_squares`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Fit linear models by minimizing the residual sum of squares between observations and linear approximations.

---

## Ordinary Least Squares (OLS)
LinearRegression solves $\min_w \|Xw - y\|^2_2$ using Singular Value Decomposition (SVD):

```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = 1 * x_0 + 2 * x_1 + 3
y = np.dot(X, np.array([1, 2])) + 3

reg = LinearRegression().fit(X, y)
print("Coefficients:", reg.coef_)
print("Intercept:", reg.intercept_)
print("Prediction on [[3, 5]]:", reg.predict([[3, 5]]))
```

### Assumptions of OLS
1. Linearity of relationship between features and target.
2. Homoscedasticity (constant variance of residuals).
3. Independence of errors (no autocorrelation).
4. No multicollinearity (features are not linearly dependent).

