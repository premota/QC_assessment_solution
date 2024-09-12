import pandas as pd

from utils.helper import read_yaml
from utils.exception import CustomException
from utils.logger import logging

import sys
from pathlib import Path
from typing import Any, Dict


class DataCleaningComponent:
    def __init__(self, data: pd.DataFrame, config_file: Path):
        self.data = data
        self.config = read_yaml(config_file)



    def get_cleaning_config(self)->Dict[str, Any]:
        try:
            logging.info("reading data cleaning config")
            data_cleaning_config = self.config.data_cleaning
            logging.info("data cleaning config has been read")
            return data_cleaning_config
        except Exception as e:
            raise CustomException(e,sys)
        

    def remove_outliers(self, data_cleaning_config: Dict[str, Any])->pd.DataFrame:
        try:
            outlier_config = data_cleaning_config.outlier_columns
            logging.info("outlier removal initated")
            df = self.data
            for column_name in outlier_config:
                # Calculate Q1 (25th percentile) and Q3 (75th percentile)
                Q1 = df[column_name].quantile(0.25)
                Q3 = df[column_name].quantile(0.75)
                
                # Calculate the IQR
                IQR = Q3 - Q1
                
                # Define bounds for outliers
                upper_bound = Q3 + 1.5 * IQR
                
                # Cap values above the upper bound at the upper bound
                df[column_name] = df[column_name].apply(lambda x: min(x, upper_bound))
            logging.info(f"all outliers have been removed, size of data: {df.shape}")
            return df
        
        except Exception as e:
            raise CustomException(e,sys)
