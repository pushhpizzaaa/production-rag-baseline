# FeatureUnion: Concatenating Feature Extractors

**Doc ID:** `sklearn_feature_union_horizontal_concatenation`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Combine multiple feature extraction mechanisms into a single feature vector using FeatureUnion.

---

## Horizontal Feature Stacking
While `Pipeline` chains operations in series, `FeatureUnion` executes transformers in parallel and concatenates their outputs horizontally:

```python
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.datasets import load_digits

X, y = load_digits(return_X_y=True)

union = FeatureUnion([
    ("pca", PCA(n_components=10)),
    ("select_best", SelectKBest(k=5))
])

X_features = union.fit_transform(X, y)
print("Extracted feature dimensions:", X_features.shape[1]) # 10 + 5 = 15 features
```

