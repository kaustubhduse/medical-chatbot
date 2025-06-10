# diabetes_model_train.py
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Generate synthetic dataset for diabetes risk
X, y = make_classification(
    n_samples=1000, n_features=5, n_informative=3, n_redundant=0, random_state=42
)

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'diabetes_model.pkl')
print("Saved diabetes_model.pkl")
