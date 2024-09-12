import sys
from typing import Any, Dict

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from utils.helper import read_yaml, save_to_pickle
from utils.exception import CustomException
from utils.logger import logging

class ModelTrainingComponent:
    def __init__(self,data: pd.DataFrame, 
                 config_file: Dict[str, Any]) -> None:
        self.data = data
        self.config = read_yaml(config_file)


    def get_model_config(self):
        try:
            logging.info("getting model configuration")
            model_config = self.config.model_training
            logging.info("model config extracted")
            return model_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def train_model(self, model_config :Dict[str, Any]):
        try:
            # extract all model configs
            param = model_config.param_grid
            test_size = model_config.test_size
            target = model_config.target
            random_state = model_config.random_state
            algo_type = model_config.classifier
            data_frame = self.data
            model_dir = model_config.model_artifact_dir

            logging.info("perform train test split")
            #split data into X and y
            X_data = data_frame.drop([target],axis = 1)
            y_data = data_frame[target]

            # Assuming X and y into train and test, add stratify = y_data to make sure 
            # the imbalance nature of target is considered
            X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, 
                                                                test_size=test_size, 
                                                                random_state=random_state,
                                                                stratify=y_data)


            # Define all classifiers
            classifiers = {
                'Logistics Regression': LogisticRegression(**param),
                'Decision tree': DecisionTreeClassifier(**param),
                'Random Forest': RandomForestClassifier(**param),
                'XGBoost': XGBClassifier(**param)
            }

            # FIT models
            for classifier_name, classifier in classifiers.items():
                # select only classifier specified on config_file
                if classifier_name == algo_type:
                    print(f"\nResults for {classifier_name}:\n")

                    # Train the classifier
                    clss = classifier
                    logging.info("fitting model")
                    clss.fit(X_train, y_train)

                    # Make predictions on Train
                    logging.info("making prediction on test partition")
                    y_train_pred = clss.predict(X_train)

                    # Make predictions on Test
                    y_pred = clss.predict(X_test)

                    # Train info: Calculate and print metrics
                    Train_accuracy = accuracy_score(y_train, y_train_pred)
                    Train_precision = precision_score(y_train, y_train_pred)
                    Train_recall = recall_score(y_train, y_train_pred)
                    Train_f1 = f1_score(y_train, y_train_pred)


                    # Test info: Calculate and print metrics
                    Test_accuracy = accuracy_score(y_test, y_pred)
                    Test_precision = precision_score(y_test, y_pred)
                    Test_recall = recall_score(y_test, y_pred)
                    Test_f1 = f1_score(y_test, y_pred)

                    # log train result
                    logging.info(f"\n Results from Train:")
                    logging.info(f"Accuracy: {Train_accuracy:.4f}")
                    
                    logging.info(f"Precision: {Train_precision:.4f}")
                    logging.info(f"Recall: {Train_recall:.4f}")
                    logging.info(f"F1 Score: {Train_f1:.4f}")

                    # log test result
                    logging.info(f"\n Results from Test:")
                    logging.info(f"Accuracy: {Test_accuracy:.4f}")
                    logging.info(f"Precision: {Test_precision:.4f}")
                    logging.info(f"Recall: {Test_recall:.4f}")
                    logging.info(f"F1 Score: {Test_f1:.4f}")

                    # Train final model on both train and test data
                    logging.info("Training final model on all both "
                                "train and test partition")
                    clss = classifier
                    logging.info("fitting final model")
                    final_model = clss.fit(X_data, y_data)

                    # save final model as pickle file
                    logging.info("save the model")
                    save_to_pickle(obj_path=model_dir, obj=final_model)
                    logging.info("model has been saved")
        except Exception as e:
            raise CustomException(e,sys)