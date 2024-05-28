import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump, load

# Load the dataset
data = pd.read_csv("summary_lettuce.csv")

# Step 1: Data Preprocessing
X = data[['Growth Day','Temperature_mean','Humidity_mean','pH Level_mean','TDS Value_mean']]
y = data['Condition']

# Step 2: Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 4: Model Training
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 5: Model Evaluation
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Step 6: Model Tuning (Optional)

# Step 7: Prediction
# Now you can use this model to predict the condition of lettuce plants for new data points.
new_data = pd.DataFrame({
    'Growth Day': [20, 21, 22],
    'Temperature_mean': [25.8, 26.5, 25.0],
    'Humidity_mean': [62, 67, 60],
    'pH Level_mean': [6.6, 6.9, 7.1],
    'TDS Value_mean': [410, 430, 390],

})


predictions = rf_model.predict(new_data)


print("\nPredicted conditions for new data points:")
for i, prediction in enumerate(predictions):
    print(f"Data point {i+1}: {prediction}")
    

dump(rf_model, 'random_forest_model.joblib')
