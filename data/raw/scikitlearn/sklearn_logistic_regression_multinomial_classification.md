# Logistic Regression for Binary and Multinomial Classification

**Doc ID:** `sklearn_logistic_regression_multinomial_classification`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Model event probabilities using the sigmoid link function and cross-entropy loss.

---

## Logistic Regression
Logistic regression models odds via the logistic function:
$$P(Y=1|X) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X)}}$$

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = LogisticRegression(max_iter=1000, C=1.0, solver="lbfgs")
clf.fit(X_train, y_train)

probs = clf.predict_proba(X_test[:3])
print("Predicted probabilities:\n", probs)
```
Parameter `C` is the inverse of regularization strength ($C = \frac{1}{\alpha}$). Smaller `C` specifies stronger regularization.

