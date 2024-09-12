from pathlib import Path
import sys

from utils.exception import CustomException
from model_trainer.Components.data_ingestion import DataIngestionComponent
from model_trainer.Components.data_cleaning import DataCleaningComponent 
from model_trainer.Components.data_transformation import DataTransformationComponent   
from model_trainer.Components.model_training import ModelTrainingComponent   


class TrainModel():
    """
    A pipeline class that orchestrates the entire process of data ingestion, cleaning, transformation,
    and model training using the specified configuration file.
    """
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

        # model training
        model_train_obj = ModelTrainingComponent(data=transformed_df,config_file=config_path)
        training_config = model_train_obj.get_model_config()
        model_train_obj.train_model(model_config=training_config)
    except Exception as e:
        raise CustomException(e,sys)












