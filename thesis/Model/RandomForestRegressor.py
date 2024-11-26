import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
dataset = pd.read_csv("C:\\Users\\PC\\Desktop\\CompleteData.csv")

# Ensure 'Program' is treated as a string
dataset['Program'] = dataset['Program'].astype(str)

# Prepare features and target variable
X = dataset[['S2_22-23', 'S2_20-21', 'S2_23-24']]
y = dataset['S2_21-22']

# Encode categorical columns in X
for column in X.columns:
    if X[column].dtype == 'object':  # If the column is categorical
        label_encoder = LabelEncoder()
        X[column] = label_encoder.fit_transform(X[column])

# Encode y if it contains categorical values
if isinstance(y.iloc[0], str):  # Check if y contains strings
    y_label_encoder = LabelEncoder()
    y = y_label_encoder.fit_transform(y)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Instantiate and fit the RandomForestRegressor
regressor = RandomForestRegressor()
regressor.fit(x_train, y_train)

# Save the model to a file
with open('model/RandomForestRegressor.pkl', 'wb') as model_file:
    pickle.dump(regressor, model_file)
