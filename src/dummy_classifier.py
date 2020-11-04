import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
class MajorityClassifier(BaseEstimator, ClassifierMixin):
    """Predicts the majority class of its training data."""
    def __init__(self):
        pass
    def fit(self, X, y):
        self.X = X
        return self
    def predict(self, X):
        return np.fromiter([x[0] for x in X],int, len(X))

class RuleClassifier(BaseEstimator, ClassifierMixin):
    """Predicts the majority class of its training data."""
    def __init__(self, vectorizer):
        self.v = vectorizer
        pass
    def fit(self, X, y):
        return self
    def predict_(self, x):
        dict = self.v.inverse_transform(x)
        if dict[0].has_key('ALARM_ANOMALOUS_HOST'):
            return 1
        return 0
    def predict(self, X):
        return np.fromiter([self.predict_(x) for x in X],int, len(X))

    
class CountClassifier(BaseEstimator, ClassifierMixin):
    """Predicts the majority class of its training data."""
    def __init__(self, vectorizer):
        self.v = vectorizer
        pass
    def fit(self, X, y):
        return self
    def predict_(self, x):
        dict = self.v.inverse_transform(x)
        if len(dict[0]) > 2:
            return 1
        return 0
    def predict(self, X):
        return np.fromiter([self.predict_(x) for x in X],int, len(X))
