# ROC-AUC Score and Receiver Operating Characteristic Curves

**Doc ID:** `sklearn_roc_auc_score_and_roc_curve`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Evaluate ranking quality across discrimination thresholds using Area Under the ROC Curve.

---

## ROC-AUC Metrics
ROC plots True Positive Rate vs False Positive Rate across all probability decision thresholds:

```python
from sklearn.metrics import roc_auc_score, roc_curve
import numpy as np

y_true = np.array([0, 0, 1, 1])
y_scores = np.array([0.1, 0.4, 0.35, 0.8])

auc = roc_auc_score(y_true, y_scores)
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
print(f"Area Under ROC Curve: {auc:.4f}")
```
An AUC of 0.5 represents a random guess, while 1.0 indicates perfect class separation.

