# K-Nearest Neighbors (KNN): Instance-Based Learning

**Doc ID:** `sklearn_k_nearest_neighbors_knn_classifier`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Classify samples based on majority voting among the k-closest instances in Euclidean feature space.

---

## KNN Mechanics
KNN is a non-parametric, lazy learner: no explicit training phase occurs during `fit()`; query points are compared against stored instances during `predict()`:

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
knn = KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2)
knn.fit(X, y)

pred = knn.predict([X[0]])
print("Predicted label:", pred)
```
Suffers from the curse of dimensionality when feature counts grow beyond 20-30 dimensions.

