# anemia_model_train.py
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Generate synthetic dataset for anemia risk (simulate features like Hemoglobin, RBC, MCV)
X, y = make_classification(
    n_samples=1000, n_features=3, n_informative=2, n_redundant=0, random_state=24
)

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24
)

# Train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=24)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'anemia_model.pkl')
print("Saved anemia_model.pkl")
