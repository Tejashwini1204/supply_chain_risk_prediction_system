import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
#from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("SCMS_Delivery_History_Dataset.csv")

# ----------------------------
# DATE PROCESSING
# ----------------------------
df['Scheduled Delivery Date'] = pd.to_datetime(df['Scheduled Delivery Date'], errors='coerce')
df['Delivered to Client Date'] = pd.to_datetime(df['Delivered to Client Date'], errors='coerce')

# ----------------------------
# CREATE TARGET (DELAY)
# ----------------------------
df['delay'] = (df['Delivered to Client Date'] > df['Scheduled Delivery Date']).astype(int)

# ----------------------------
# FEATURE ENGINEERING (ADD HERE)
# ----------------------------
df['day_of_week'] = df['Scheduled Delivery Date'].dt.dayofweek
df['month'] = df['Scheduled Delivery Date'].dt.month
df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# ----------------------------
# CLEAN DATA
# ----------------------------
df = df.dropna()

# Convert Freight Cost to numeric
df['Freight Cost (USD)'] = pd.to_numeric(df['Freight Cost (USD)'], errors='coerce')

# ----------------------------
# SELECT FEATURES
# ----------------------------
df = df[['Vendor', 'Shipment Mode', 'Line Item Quantity',
         'Freight Cost (USD)', 'Unit Price',
         'day_of_week', 'month', 'is_weekend',
         'delay']]

df = df.dropna()

# ----------------------------
# ONE-HOT ENCODING
# ----------------------------
df = pd.get_dummies(df, columns=['Vendor', 'Shipment Mode'], drop_first=True)

# ----------------------------
# ENCODING
# ----------------------------
#le_vendor = LabelEncoder()
#le_mode = LabelEncoder()

#df['Vendor'] = le_vendor.fit_transform(df['Vendor'])
#df['Shipment Mode'] = le_mode.fit_transform(df['Shipment Mode'])

# ----------------------------
# CHECK CLASS DISTRIBUTION
# ----------------------------
print("Before balancing:\n", df['delay'].value_counts())

# ----------------------------
# BALANCE DATASET (VERY IMPORTANT)
# ----------------------------
df_delay = df[df['delay'] == 1]
df_ontime = df[df['delay'] == 0].sample(len(df_delay), random_state=42)

df = pd.concat([df_delay, df_ontime])

print("After balancing:\n", df['delay'].value_counts())

# ----------------------------
# SPLIT DATA
# ----------------------------
X = df.drop('delay', axis=1)
y = df['delay']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ----------------------------
# SCALING (ADD HERE)
# ----------------------------
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

num_cols = ['Line Item Quantity', 'Freight Cost (USD)', 'Unit Price']

X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

# ----------------------------
# MODEL (UPGRADED)
# ----------------------------
model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=3
)

model.fit(X_train, y_train)

scores = cross_val_score(model, X, y, cv=5)
print("Cross Validation Accuracy:", scores.mean())
print("Cross Validation Scores:", scores)
print("Mean Accuracy:", scores.mean())
# ----------------------------
# EVALUATION
# ----------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ----------------------------
# SAVE METRICS (NEW ADDITION)
# ----------------------------
import joblib
from sklearn.metrics import precision_score, recall_score

metrics = {
    "accuracy": accuracy,
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "y_test": y_test,
    "y_pred": y_pred,
    "y_prob": model.predict_proba(X_test)[:,1]
}

joblib.dump(metrics, "metrics.pkl")

print("✅ Metrics saved successfully!")

# ----------------------------
# SAVE MODEL + ENCODERS
# ----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(X.columns, "columns.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n✅ Model and encoders saved successfully!")