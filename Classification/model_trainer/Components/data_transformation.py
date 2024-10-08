import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from utils.exception import CustomException
from utils.logger import logging
from utils.helper import read_yaml, save_to_pickle

from typing import Any, Dict

import sys


class DataTransformationComponent:
    """
    A component responsible for performing data transformations including 
    data type conversions,separating numerical and categorical features, 
    and applying transformations.
    """
    def __init__(self, data: pd.DataFrame, 
                 config_file: Dict[str, Any]) -> None:
        
        self.data = data
        self.config_file = read_yaml(config_file)


    def get_transformation_config(self):
        """
        Retrieves the transformation configuration from the YAML file.

        Returns:
        -------
        dict:
            A dictionary containing the transformation settings, such as columns 
            and target feature.
        """
        try:
            logging.info("getting transformation config")
            transformation_config = self.config_file.data_transformation
            logging.info("data transformation config has been read")
            return transformation_config
        except Exception as e:
            raise CustomException(e,sys)


    def convert_data_type(self, data_transformation_config: Dict[str, Any]):
        """
        Converts nominal categorical columns to the appropriate data type.

        Parameters:
        ----------
        data_transformation_config : dict
            Configuration dictionary containing details about nominal columns.

        Returns:
        -------
        pd.DataFrame:
            The updated DataFrame with nominal columns converted to object type.
        """
        try:
            logging.info("converting nominal categorical columns to the right datatype")
            nominal_columns = data_transformation_config.nominal_columns
            for feature in nominal_columns:
                self.data[feature] = self.data[feature].astype(object)
            logging.info("data type conversion is complete")
            return self.data
        except Exception as e:
            raise CustomException(e,sys)
        

    def transform_data(self,dataframe, data_transformation_config: Dict[str, Any]):
        """
        Transforms the data by applying numerical and categorical transformers 
        (e.g., scaling, one_hot_encoding).

        Parameters:
        ----------
        dataframe : pd.DataFrame
            The DataFrame that contains the features to be transformed.
        data_transformation_config : dict
            The configuration for data transformation, including the target column 
            and the location to save the transformer.

        Returns:
        -------
        pd.DataFrame:
            A transformed DataFrame with numerical and categorical features processed.
        """
        try:
            # extract target feature and location to save transformer object from config
            target = data_transformation_config.target
            save_location = data_transformation_config.transformer_pickle


            df = dataframe.drop([target], axis =1)
            #seoarate numerical and categorical data
            logging.info("separating numerical and categorical data")
            numerical_features = df.select_dtypes(exclude = "object").columns.to_list()
            categorical_features = df.select_dtypes(include = "object").columns.to_list()
            
            # Transformers
            logging.info("instantiating tranformers")
            numerical_transformer = MinMaxScaler()
            categorical_transformer = OneHotEncoder(drop = 'if_binary')
            
            # define column transformer object
            pipeline = ColumnTransformer(
            [
            ( "numerical transformer", numerical_transformer, numerical_features),
                ("categorical transformer", categorical_transformer, categorical_features)
            ])
            
            # apply transformer
            logging.info("fit and transformers")
            transformed_array = pipeline.fit_transform(df)
            
            # Get the transformed column names
            transformed_numerical_columns = pipeline.transformers_[0][2]
            transformed_categorical_columns = pipeline.transformers_[1][1].get_feature_names_out(
                                                                            input_features=categorical_features)
            
            # Combine numerical and categorical transformed column names
            transformed_column_names = list(transformed_numerical_columns) + list(transformed_categorical_columns)
            
            # convert array to dataframe
            transformed_data = pd.DataFrame(transformed_array, columns=transformed_column_names)
            
            # attach target feature
            transformed_data[target] = dataframe[target]
            logging.info(f"data has been transformed, to shape {transformed_data.shape}")

            save_to_pickle(obj_path=save_location, obj=pipeline)
            logging.info("transformer object saved as pickle file")
            return transformed_data
        except Exception as e:
            raise CustomException(e,sys)

