# Model Persistence: Serializing Models with Joblib

**Doc ID:** `sklearn_model_persistence_joblib_safetensors`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Save and restore trained scikit-learn models and preprocessing pipelines using Joblib.

---

## Serializing Models
```python
import joblib
from sklearn.linear_model import Ridge
import numpy as np

model = Ridge().fit([[0, 0], [1, 1]], [0, 1])

# Save model weights and metadata
joblib.dump(model, "ridge_model.joblib")

# Load model in production
loaded_model = joblib.load("ridge_model.joblib")
print("Prediction from loaded model:", loaded_model.predict([[2, 2]]))
```
Joblib is heavily optimized for NumPy array data buffers, outperforming Python's standard `pickle`.

