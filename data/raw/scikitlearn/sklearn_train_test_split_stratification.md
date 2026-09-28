# Train-Test Split and Stratification Strategies

**Doc ID:** `sklearn_train_test_split_stratification`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Split datasets while preserving class distribution proportions in classification tasks.

---

## Stratified Splitting
Random splitting on imbalanced datasets can result in rare classes missing completely from the test set:

```python
from sklearn.model_selection import train_test_split
import numpy as np

X = np.random.randn(100, 4)
y = np.array([0] * 90 + [1] * 10) # 10% positive class

# stratify=y preserves exact 90:10 ratio across both train and test splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Test Positive Ratio: {np.mean(y_test):.2f}") # 0.10
```

