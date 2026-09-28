# GridSearchCV: Exhaustive Hyperparameter Optimization

**Doc ID:** `sklearn_grid_search_cv_hyperparameter_tuning`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Tune combinations of hyperparameters across cross-validation folds systematically.

---

## Exhaustive Grid Search
```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

param_grid = {
    "n_estimators": [50, 100],
    "max_depth": [3, 5, None],
    "min_samples_split": [2, 5]
}

grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring="accuracy")
grid.fit(X, y)

print("Best Parameters:", grid.best_params_)
print("Best CV Score:", grid.best_score_)
```

