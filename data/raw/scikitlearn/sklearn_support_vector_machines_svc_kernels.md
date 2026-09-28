# Support Vector Machines: Maximum Margin and Kernel Trick

**Doc ID:** `sklearn_support_vector_machines_svc_kernels`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Find optimal separating hyperplanes that maximize the geometric margin using linear and RBF kernels.

---

## SVM and the Kernel Trick
SVM finds the decision boundary maximizing margin $\frac{2}{\|w\|}$:
Non-linear separation uses kernel functions $K(x, x') = \exp(-\gamma \|x - x'\|^2)$ (Radial Basis Function).

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

X, y = load_iris(return_X_y=True)

# SVM strictly requires feature scaling
svm_clf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma="scale"))
svm_clf.fit(X, y)
print("Support Vectors Count:", svm_clf.named_steps["svc"].n_support_)
```

