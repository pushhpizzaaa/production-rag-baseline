# The Estimator and Transformer API Design

**Doc ID:** `sklearn_estimator_and_transformer_api`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Scikit-learn's unified object-oriented API revolves around Estimators (fit, predict) and Transformers (fit, transform).

---

## The Core Object Interface
Scikit-learn standardizes machine learning algorithms into three fundamental interfaces:
1. **Estimator**: Learns from data via `.fit(X, y=None)`.
2. **Transformer**: Transforms input features via `.transform(X)` or `.fit_transform(X)`.
3. **Predictor**: Produces predictions via `.predict(X)` and probabilities via `.predict_proba(X)`.

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.array([[1.0, -1.0], [2.0, 0.0], [0.0, 1.0]])

# Transformer workflow
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

print("Learned Means:", scaler.mean_)
print("Learned Variances:", scaler.var_)
```

### Key Principles
- **Consistency**: All objects share a clean, uniform interface.
- **Inspection**: All learned model parameters are stored as public attributes ending with a trailing underscore (e.g. `mean_`, `coef_`).
- **Non-proliferation of classes**: Datasets are expressed as NumPy arrays or SciPy sparse matrices, not proprietary container classes.

