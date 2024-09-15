# Project: Classification Machine Learning Pipeline

## Folder Structure
```plaintext
Classification/
├── artifacts/
│   ├── clean_data.csv
│   ├── classification_data.csv
│   ├── data_transformer/
│   │   └── transformer.pkl
│   └── model/
│       └── model.pkl
├── model_prediction/
│   ├── prediction_config.yaml
│   └── prediction_pipeline.py
├── model_trainer/
│   ├── components/
│   │   ├── data_cleaning.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_training.py
│   ├── pipelines/
│   │   └── training_pipeline.py
│   └── training_config.yaml
├── notebook/
│   ├── data_cleaning.ipynb
│   ├── EDA.ipynb
│   └── modeling.ipynb
├── utils/
│   ├── exception.py
│   ├── helper.py
│   └── logger.py
├── app.py
├── README.md
├── requirements.txt
└── setup.py

## Overview
This project focuses on building a machine learning classification model using Python. The goal is to predict outcomes based on a labeled dataset through a series of data processing steps and model training. Initially, experimentation was performed in Jupyter notebooks, and once the process was refined, the project was broken down into modular scripts. This enabled the creation of a structured pipeline for model training and inference, making it easier to manage and deploy.

### Key Components
- Experimentation with Notebooks: Early stages of the project involved using Jupyter notebooks to explore the data, clean it, and build a basic classification model. Key notebooks include:

    - Data cleaning.
    - Exploratory Data Analysis (EDA).
    - Model building and testing.

- Modular Scripts: The project was later organized into separate scripts to automate and streamline the process:   
    - Data Cleaning: Prepares and cleans raw data.
    - Data Ingestion: Loads the data for use in the model.
    - Data Transformation: Applies transformations like scaling and encoding.
    - Model Training: Trains the machine learning model using the cleaned and transformed data.
    
- Pipeline for Model Training: The training pipeline integrates all the necessary steps to clean data, prepare it, and train the model in a structured, repeatable way. This pipeline also includes configuration files for customizing the process.

- Model Prediction: After the model is trained, a separate pipeline is used to make predictions on new data based on a configuration file.


### Technologies Used
Python: For scripting the model, data processing, and pipeline automation.
Jupyter Notebooks: For initial experimentation and exploration.
YAML Configurations: To make the pipeline processes flexible and easy to adjust.
Pickle Files: To save and load trained models and transformers.