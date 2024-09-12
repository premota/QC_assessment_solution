from pathlib import Path
from typing import Dict

from utils.helper import read_yaml
from utils.exception import CustomException
from utils.logger import logging

import pandas as pd
import sys




class DataIngestionComponent:
    def __init__(self, config_file: Path):
        self.config = read_yaml(config_file)

    def get_data_ingestion_config(self)->Dict[str, str]:
        try:
            logging.info("getting data ingestion config")
            config = self.config.data_ingestion
            logging.info("data ingestion config has been read")
            return config
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def ingest_data(self, config: Dict[str, str])->pd.DataFrame:
        try:
            logging.info("reading data")
            data = pd.read_csv(config.source_dir)
            data_size = data.shape
            logging.info(f"data has been read successfully. size of data is {data_size}")
            return data
        
        except Exception as e:
            raise CustomException(e,sys)


from model_trainer.Components.data_cleaning import DataCleaningComponent 
from model_trainer.Components.data_transformation import DataTransformationComponent      
if __name__ == "__main__":
    
    try:
        config_path = Path("model_trainer/training_config.yaml")

        # data ingestion
        injest_obj = DataIngestionComponent(config_path)
        inject_config = injest_obj.get_data_ingestion_config()
        data = injest_obj.ingest_data(inject_config)
        
        # data cleaning
        cleaning_obj = DataCleaningComponent(data=data, config_file=config_path)
        outlier_config = cleaning_obj.get_cleaning_config()
        clean_df = cleaning_obj.remove_outliers(outlier_config)

        # data transformation
        transform_obj = DataTransformationComponent(data=clean_df, config_file=config_path)
        transform_config = transform_obj.get_transformation_config()
        transformed_df = transform_obj.convert_data_type(transform_config)
        transformed_df = transform_obj.transform_data(transformed_df,transform_config)
    except Exception as e:
        raise CustomException(e,sys)












