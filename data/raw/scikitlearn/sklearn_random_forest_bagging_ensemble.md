# Random Forest: Bagging and Feature Subsampling

**Doc ID:** `sklearn_random_forest_bagging_ensemble`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Ensemble hundreds of de-correlated decision trees trained on bootstrap samples with random feature subsets.

---

## Random Forest Mechanics
Combines Bootstrap Aggregation (bagging) with random feature subspaces:
1. Sample $N$ items with replacement (bootstrap).
2. At each node split, consider only a random subset of features (typically $\sqrt{p}$).
3. Grow trees to full depth without pruning.
4. Aggregate predictions by majority vote or mean averaging.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
rf = RandomForestClassifier(n_estimators=100, max_features="sqrt", random_state=42, n_jobs=-1)
rf.fit(X, y)

print("Top 3 Feature Importances:", sorted(zip(rf.feature_importances_, range(X.shape[1])), reverse=True)[:3])
```

