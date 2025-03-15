import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get feature names from the model
feature_names = model.best_estimator_.feature_names_in_

st.title('Insurance Cross-Sell Prediction')
st.write("""
Predict customer likelihood to purchase vehicle insurance
""")

# Create input widgets
inputs = {}
st.header('Customer Information')

# Personal Information
col1, col2 = st.columns(2)
with col1:
    inputs['Gender'] = st.selectbox('Gender', ['Male', 'Female'])
    inputs['Age'] = st.slider('Age', 20, 85, 30)
    inputs['Region_Code'] = st.selectbox('Region Code', sorted([
        28, 3, 11, 41, 33, 6, 35, 50, 15, 45, 8, 36, 30, 26, 16, 47, 48, 19,
        39, 23, 37, 5, 17, 2, 7, 29, 46, 27, 25, 13, 18, 20, 49, 22, 44, 0,
        9, 31, 12, 34, 21, 10, 14, 38, 24, 40, 43, 32, 4, 51, 42, 1, 52
    ]))

with col2:
    inputs['Driving_License'] = 1 if st.selectbox('Driving License', ['Yes', 'No']) == 'Yes' else 0
    inputs['Previously_Insured'] = 1 if st.selectbox('Previously Insured', ['Yes', 'No']) == 'Yes' else 0
    inputs['Vehicle_Age'] = st.slider('Vehicle Age (Years)', 0, 10, 1)
    inputs['Vehicle_Damage'] = 1 if st.selectbox('Vehicle Damage', ['Yes', 'No']) == 'Yes' else 0

# Insurance Details
st.subheader('Insurance Policy Details')
inputs['Annual_Premium'] = st.slider('Annual Premium ($)', 2000, 600000, 30000)
inputs['Policy_Sales_Channel'] = st.selectbox('Policy Sales Channel', [
    26, 152, 160, 124, 14, 13, 30, 156, 163, 157, 122, 19, 22, 15, 154, 16,
    52, 155, 11, 151, 125, 25, 61, 1, 86, 31, 150, 23, 60, 21, 121, 3, 139,
    12, 29, 55, 7, 47, 127, 153, 78, 158, 89, 32, 8, 10, 120, 65, 4, 42, 83,
    136, 24, 18, 56, 48, 106, 54, 93, 116, 91, 45, 9, 145, 147, 44, 109, 37,
    140, 107, 128, 131, 114, 118, 159, 119, 105, 135, 62, 138, 129, 88, 92,
    111, 113, 73, 36, 28, 35, 59, 53, 148, 133, 108, 64, 39, 94, 132, 46, 81,
    103, 90, 51, 27, 146, 63, 96, 40, 66, 100, 95, 123, 98, 75, 69, 130, 134,
    49, 97, 38, 17, 110, 80, 71, 117, 58, 20, 76, 104, 87, 84, 137, 126, 68,
    67, 101, 115, 57, 82, 79, 112, 99, 70, 2, 34, 33, 74, 102, 149, 43, 6, 50,
    144, 143, 41
])

inputs['Vintage'] = st.slider('Vintage (Days)', 10.0, 299.0, 150.0)

# Convert categoricals to numerical
input_df = pd.DataFrame([inputs])
input_df = pd.get_dummies(input_df, columns=['Gender'])

# Ensure all required columns are present
missing_cols = set(feature_names) - set(input_df.columns)
for col in missing_cols:
    input_df[col] = 0  # Add missing columns with 0 values

# Reorder columns to match training data
input_df = input_df[feature_names]

# Make prediction
if st.button('Predict Insurance Purchase Likelihood'):
    prediction = model.best_estimator_.predict(input_df)
    probability = model.best_estimator_.predict_proba(input_df)[0][1]
    
    st.subheader('Prediction')
    st.write(f'Will purchase insurance: **{"Yes" if prediction[0] == 1 else "No"}**')
    st.write(f'Probability: {probability:.2%}')
    
    st.subheader('Model Info')
    st.write(f'Best parameters: {model.best_params_}')
    st.write(f'Validation accuracy: {model.best_score_:.2%}')

st.write("""
**Note:** 
- All monetary values are in Indian Rupees ($)
- Vehicle Age should be reported in whole years
- Vintage represents number of days since policy inception
""")