# RobustScaler: Outlier-Resistant Feature Scaling

**Doc ID:** `sklearn_robust_scaler_outlier_handling`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Scale features using median and Interquartile Range (IQR) to withstand extreme outliers.

---

## Robust Scaling with Median and IQR
When features contain heavy outliers, standard deviation is heavily skewed:
$$\text{RobustScale}(x) = \frac{x - \text{median}}{\text{IQR}} = \frac{x - Q_2}{Q_3 - Q_1}$$

```python
from sklearn.preprocessing import RobustScaler
import numpy as np

# Dataset with massive outlier (9999.0)
data = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [9999.0]])

scaler = RobustScaler()
scaled_data = scaler.fit_transform(data)
print("Robust Scaled Values:\n", scaled_data[:5])
```
The outlier does not influence the center (median) or spread (IQR) of the normal distribution.

