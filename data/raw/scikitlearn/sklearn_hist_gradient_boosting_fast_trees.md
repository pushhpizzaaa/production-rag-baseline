# HistGradientBoosting: High-Performance Binned Boosting

**Doc ID:** `sklearn_hist_gradient_boosting_fast_trees`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Train gradient boosted trees on millions of rows using LightGBM-inspired integer histogram binning.

---

## Why HistGradientBoosting Is 10x-50x Faster
`HistGradientBoostingClassifier` bins continuous features into 256 discrete integer bins (uint8):
- Memory footprint drops drastically.
- Split finding reduces from $O(N \log N)$ to $O(K)$ where $K=256$.
- Native support for missing values (`np.nan`) without imputation.

```python
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
# Introduce NaNs
X[0, 0] = np.nan

hgb = HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=20)
hgb.fit(X, y)
print("Trained model on data containing NaNs successfully:", hgb.score(X, y))
```

