# Classification Metrics: Precision, Recall, and F1-Score

**Doc ID:** `sklearn_classification_metrics_precision_recall_f1`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Measure classification performance beyond accuracy on balanced and imbalanced targets.

---

## Precision, Recall, and F1
- $\text{Precision} = \frac{TP}{TP + FP}$: Purity of positive predictions.
- $\text{Recall} = \frac{TP}{TP + FN}$: Coverage of actual ground-truth positives.
- $F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$: Harmonic mean.

```python
from sklearn.metrics import precision_recall_fscore_support, classification_report
import numpy as np

y_true = np.array([0, 1, 1, 0, 1, 0])
y_pred = np.array([0, 1, 0, 0, 1, 1])

p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary")
print(f"Precision: {p:.2f}, Recall: {r:.2f}, F1: {f1:.2f}")
print("\n", classification_report(y_true, y_pred))
```

