# K-Fold and StratifiedKFold Cross-Validation

**Doc ID:** `sklearn_k_fold_and_stratified_k_fold_cross_validation`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Evaluate model stability by splitting datasets into k mutually exclusive validation partitions.

---

## Stratified K-Fold CV
```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
clf = LogisticRegression(max_iter=200)

scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
print("Fold Accuracies:", scores)
print(f"Mean CV Accuracy: {scores.mean():.4f} +/- {scores.std():.4f}")
```

