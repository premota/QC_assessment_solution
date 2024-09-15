from pathlib import Path
import sys
import pandas as pd
import streamlit as st

from utils.exception import CustomException
from model_prediction.prediction_pipeline import PredictionPipeline

st.title("Quick-check classification project")
st.write("""
This model predicts a binary label (1: bad, 0:good)
""")
st.write("---")

# numerical features (including ordinal categorical features)
numerical_features = ['Duration of Credit (month)',
       'Payment Status of Previous Credit','Credit Amount',
        'Length of current employment', 'Instalment per cent',
       'Guarantors', 'Duration in Current address',
       'Most valuable available asset', 'Age', 'Concurrent Credits',
       'No of Credits at this Bank', 
       'No of dependents']

# nominal categorical feautes
categorical_features = {"Account type":[1, 2, 4, 3], "Purpose":[2,0,9,3,1,10,5,4,6,8],
                "Savings type":[1,2,3,5,4], "Type of apartment":[1,2,3],"Marital Status":[2,3,4,1],
                "Occupation":[3,2,1,4],"Foreign Worker":[1,2]}

entered_values = {}
st.title('Numerical Inputs')

# Loop through each numerical feature and create a numerical input bar
for col_name in numerical_features:
    value = st.number_input(col_name, value=0.0)
    entered_values[col_name] = value

# Loop through each categorical feature and create drop down menu
for feature, options in categorical_features.items():
    value = st.selectbox(feature, options= options)
    entered_values[feature] = value


if st.button("Make Prediction"):
    try:
        config_path = Path("model_prediction/prediction_config.yaml")
        data_frame = pd.DataFrame(entered_values, index = [0])
        prediction_obj = PredictionPipeline(input_data=data_frame,
                                            config_path=config_path)
        prediction_config = prediction_obj.get_prediction_config()
        prediction = prediction_obj.make_prediction(prediction_config)

        st.header("Label Prediction")
        if prediction == 1:
            prediction = "BAD (1)"
        if prediction == 0:
            prediction = "Good (0)"
            
        st.write(prediction)
    except Exception as e:
        raise CustomException(e,sys)