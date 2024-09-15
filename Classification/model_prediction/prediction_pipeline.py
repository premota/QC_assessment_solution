from pathlib import Path
import sys
from typing import Any, Dict

import pandas as pd

from utils.exception import CustomException
from utils.helper import read_yaml, load_pickle



class PredictionPipeline:
    """
    A class to encapsulate the prediction pipeline for a machine learning model, 
    handling configurations and prediction operations.

    Attributes:
        data (pd.DataFrame): The input data on which predictions are to be made.
        config (dict): Configuration settings loaded from a YAML file, containing
                       details needed for transforming data and making predictions.

    Args:
        input_data (pd.DataFrame): The data to be used for predictions.
        config_path (Path): The path to the configuration YAML file.
    """

    def __init__(self, input_data: pd.DataFrame,
                  config_path: Path) -> None:
        self.data = input_data
        self.config = read_yaml(config_path)

    def get_prediction_config(self):
        try:
            prediction_config = self.config.prediction
            return prediction_config
        except Exception as e:
            raise CustomException(e,sys)
    

    def make_prediction(self, config: Dict[str, Any])-> int:
        try:
            transformer_path = config.transformer_pickle_dir
            model_path = config.model_artifact_dir
            nominal_columns = config.nominal_columns

            transformer = load_pickle(transformer_path)
            model = load_pickle(model_path)

            for feature in nominal_columns:
                self.data[feature] = self.data[feature].astype(object)
        
            transformed_data = transformer.transform(self.data)
            prediction = model.predict(transformed_data)
            return prediction
        
        except Exception as e:
            raise CustomException(e,sys)