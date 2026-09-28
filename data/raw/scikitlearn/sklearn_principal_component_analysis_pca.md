# Principal Component Analysis (PCA) for Dimensionality Reduction

**Doc ID:** `sklearn_principal_component_analysis_pca`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Project high-dimensional data onto orthogonal axes of maximum variance via Singular Value Decomposition.

---

## PCA Mechanics
Computes eigenvectors of the covariance matrix to capture the greatest variance in descending order:

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print("Explained Variance Ratio:", pca.explained_variance_ratio_)
print("Total variance retained:", sum(pca.explained_variance_ratio_))
```
Features must be scaled to mean 0 and variance 1 before PCA; otherwise features with large raw magnitudes dominate the principal components.

