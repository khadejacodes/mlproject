import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from src.utils import load_object # You'll add this to utils.py
import os

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Paths to the 'brains' we saved earlier
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")

            logging.info("Loading model and preprocessor")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            # 1. Transform the raw input using the training scaling/PCA
            data_scaled = preprocessor.transform(features)
            
            # 2. Get the prediction (0 or 1)
            preds = model.predict(data_scaled)
            
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    '''
    This class is responsible for mapping the HTML/API inputs to the DataFrame
    '''
    def __init__(self, gene_data_dict: dict):
        # In a gene project, you'd likely pass a dictionary of all 7,129 genes
        self.gene_data_dict = gene_data_dict

    def get_data_as_data_frame(self):
        try:
            # Convert the dictionary of gene values into a DataFrame row
            df = pd.DataFrame([self.gene_data_dict])
            return df
        except Exception as e:
            raise CustomException(e, sys)