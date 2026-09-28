# K-Means Clustering and k-means++ Initialization

**Doc ID:** `sklearn_k_means_clustering_and_k_means_plus_plus`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Partition data into k clusters by minimizing within-cluster sum-of-squares (inertia).

---

## K-Means Objective
Minimizes inertia:
$$\sum_{i=0}^{n} \min_{\mu_j \in C} (\|x_i - \mu_j\|^2)$$

```python
from sklearn.cluster import KMeans
import numpy as np

X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

# init='k-means++' seeds initial centroids far apart, avoiding poor local minima
kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10, random_state=0)
kmeans.fit(X)

print("Cluster Labels:", kmeans.labels_)
print("Centroids:\n", kmeans.cluster_centers_)
print("Inertia:", kmeans.inertia_)
```

