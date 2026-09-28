# Building Custom Estimators with BaseEstimator and ClassifierMixin

**Doc ID:** `sklearn_custom_estimator_base_estimator_and_mixin`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Author custom scikit-learn compatible algorithms with automated get_params and set_params support.

---

## Writing Custom Estimators
Inherit from `BaseEstimator` and relevant mixins:

```python
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import numpy as np

class MeanMajorityClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)
        self.mean_feature_ = np.mean(X[:, 0])
        return self

    def predict(self, X):
        check_is_fitted(self, ["classes_", "mean_feature_"])
        X = check_array(X)
        return (X[:, 0] > self.mean_feature_).astype(int)
```

