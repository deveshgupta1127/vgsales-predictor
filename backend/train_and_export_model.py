import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

# Load dataset
print("Loading dataset...")
df = pd.read_csv('vgsales.csv')
print(f"Original shape: {df.shape}")
df.dropna(inplace=True)
print(f"Shape after dropping NA: {df.shape}")

# Explore dataset
print("Top 5 records:")
print(df.head())
print("Data types:")
print(df.dtypes)
print("Descriptive statistics:")
print(df.describe())

# Encode categorical features
label_encoders = {}
for col in ['Platform', 'Genre', 'Publisher']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Save encoders
with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

# Define features and target
features = ['Platform', 'Genre', 'Publisher', 'Critic_Score', 'User_Score']
X = df[features]
y = df['Global_Sales']

# Normalize scores
scaler = StandardScaler()
X[['Critic_Score', 'User_Score']] = scaler.fit_transform(X[['Critic_Score', 'User_Score']])

# Save scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split completed.")

# Train model
print("Training XGBoost model...")
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# Evaluate model
print("Evaluating model...")
y_pred = model.predict(X_test)
print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")

# Plot predictions
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
plt.xlabel('Actual Global Sales')
plt.ylabel('Predicted Global Sales')
plt.title('Actual vs Predicted Global Sales')
plt.grid(True)
plt.savefig("prediction_plot.png")
plt.close()
print("Saved prediction plot.")

# Save model
print("Saving model to model.pkl...")
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved successfully.")
