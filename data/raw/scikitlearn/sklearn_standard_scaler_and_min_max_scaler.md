# StandardScaler and MinMaxScaler: Normalization Fundamentals

**Doc ID:** `sklearn_standard_scaler_and_min_max_scaler`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Compare z-score standardization (zero mean, unit variance) versus min-max feature bounding.

---

## Scaling Techniques
- **StandardScaler**: Computes $z = \frac{x - \mu}{\sigma}$. Centers data to mean 0, variance 1. Essential for PCA, SVM, Ridge/Lasso, and Logistic Regression.
- **MinMaxScaler**: Scales data to fixed range $[0, 1]$ via $x_{scaled} = \frac{x - x_{min}}{x_{max} - x_{min}}$. Useful for bounded neural networks or image pixels.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np

data = np.array([[10.0], [20.0], [30.0], [100.0]])

std_scaler = StandardScaler()
mm_scaler = MinMaxScaler()

print("Standard Scaled:\n", std_scaler.fit_transform(data))
print("MinMax Scaled:\n", mm_scaler.fit_transform(data))
```
Notice: Both are sensitive to extreme outliers because outliers distort mean, variance, min, and max.

