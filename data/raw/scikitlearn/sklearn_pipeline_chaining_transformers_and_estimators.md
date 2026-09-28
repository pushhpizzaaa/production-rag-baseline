# Pipeline: Chaining Transformers and Estimators

**Doc ID:** `sklearn_pipeline_chaining_transformers_and_estimators`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Prevent data leakage and encapsulate end-to-end modeling workflows using sklearn.pipeline.Pipeline.

---

## Why Pipelines Are Essential
A `Pipeline` sequentially applies a list of transformers followed by a final estimator:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])

# Fits scaler on train, transforms train, then fits classifier
pipeline.fit(X_train, y_train)

# Transforms test using train parameters, then predicts
accuracy = pipeline.score(X_test, y_test)
print(f"Test Accuracy: {accuracy:.4f}")
```

### Leakage Prevention
Pipelines guarantee that preprocessing parameters (e.g. mean, std dev, IDF frequencies) are computed exclusively on training folds during cross-validation, preventing catastrophic optimistic evaluation bias.

