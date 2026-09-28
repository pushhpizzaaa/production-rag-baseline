# Decision Trees: Classification and Regression Trees (CART)

**Doc ID:** `sklearn_decision_tree_classifier_and_regressor`  
**Category:** `Scikit-Learn`  
**Domain:** `Machine Learning & Feature Engineering`  
**Summary:** Construct recursive partitioning decision trees using Gini impurity, Entropy, and Mean Squared Error.

---

## CART Algorithm
Decision trees split feature spaces recursively to maximize purity:
- **Gini Impurity**: $I_G(p) = 1 - \sum_{i=1}^J p_i^2$
- **Entropy**: $H(p) = -\sum_{i=1}^J p_i \log_2(p_i)$

```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris

iris = load_iris()
dt = DecisionTreeClassifier(max_depth=3, min_samples_split=5, criterion="gini")
dt.fit(iris.data, iris.target)

tree_rules = export_text(dt, feature_names=iris.feature_names)
print(tree_rules)
```

### Hyperparameters to Prevent Overfitting
- `max_depth`: Limits tree depth.
- `min_samples_split`: Minimum sample count required to split an internal node.
- `min_samples_leaf`: Minimum samples in a leaf.

