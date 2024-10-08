from pathlib import Path
from typing import Dict

from utils.helper import read_yaml
from utils.exception import CustomException
from utils.logger import logging

import pandas as pd
import sys




class DataIngestionComponent:
    """
    Handles the ingestion of data from specified sources.
    """
    def __init__(self, config_file: Path):
        self.config = read_yaml(config_file)


    def get_data_ingestion_config(self)->Dict[str, str]:
        """
        Extracts the data ingestion configuration from the config file.

        Returns:
        -------
        dict:
            Configuration settings for data ingestion such as source directory.
        """
        try:
            logging.info("getting data ingestion config")
            config = self.config.data_ingestion
            logging.info("data ingestion config has been read")
            return config
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def ingest_data(self, config: Dict[str, str])->pd.DataFrame:
        """
        Reads data from the source directory defined in the configuration 
        and loads it into a pandas DataFrame.

        Parameters:
        ----------
        config : dict
            Data ingestion configuration, including the source directory.

        Returns:
        -------
        pd.DataFrame:
            A DataFrame containing the ingested data.
        """
        try:
            logging.info("reading data")
            data = pd.read_csv(config.source_dir)
            data_size = data.shape
            logging.info(f"data has been read successfully. size of data is {data_size}")
            return data
        
        except Exception as e:
            raise CustomException(e,sys)


