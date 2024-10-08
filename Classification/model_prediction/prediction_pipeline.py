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
        """
        Retrieves the prediction-specific configuration from the loaded config object.

        Returns:
            Any: The configuration object specific to the prediction process, the 
                 type of which depends on the structure of the loaded configuration.
        """
        try:
            prediction_config = self.config.prediction
            return prediction_config
        except Exception as e:
            raise CustomException(e,sys)
    

    def make_prediction(self, config: Dict[str, Any])-> int:
        """
        Executes the prediction process on the loaded data using specified configuration
        details for the transformer and model paths, as well as handling of nominal columns.

        Args:
            config (Dict[str, Any]): A dictionary containing the configuration settings,
                                    which include:
                                    - transformer_pickle_dir: Path to the pickle file
                                    of the pre-trained transformer.
                                    - model_artifact_dir: Path to the pickle file of the
                                    pre-trained machine learning model.
                                    - nominal_columns: A list of column names in the data
                                    that should be treated as categorical (nominal).

        Returns:
            int: The predicted result generated by the machine learning model. Assumes
                the model's `predict` method returns an integer.
        """

        try:
            # extract all config
            transformer_path = config.transformer_pickle_dir
            model_path = config.model_artifact_dir
            nominal_columns = config.nominal_columns

            # load transformer and model pickle file
            transformer = load_pickle(transformer_path)
            model = load_pickle(model_path)

            # convert nominal feature to obj string
            for feature in nominal_columns:
                self.data[feature] = self.data[feature].astype(object)

            # transform input data
            transformed_data = transformer.transform(self.data)
            # make prediction
            prediction = model.predict(transformed_data)
            return prediction
        
        except Exception as e:
            raise CustomException(e,sys)