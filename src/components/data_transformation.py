import sys
import os
from dataclasses import dataclass
import numpy as np 
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object # You'll need a utility to save the pickle

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function creates the actual preprocessing pipeline
        '''
        try:
            logging.info("Creating preprocessing pipeline")
            
            # Since all your columns are numerical genes, we create one pipeline
            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("feature_selection", SelectKBest(f_classif, k=10))
            ])

            return num_pipeline

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            # CRITICAL: Handle the 'object' to 'numeric' conversion here
            # We drop 'Class' and 'Sample' before converting
            target_column_name = "Class"
            drop_columns = [target_column_name, "patient"]
            
            logging.info(f"Dropping columns: {drop_columns}")
            
            input_feature_train_df = train_df.drop(columns=drop_columns)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns)
            target_feature_test_df = test_df[target_column_name]

            # Force numeric conversion (fixing the 'object' issue)
            input_feature_train_df = input_feature_train_df.apply(pd.to_numeric, errors='coerce')
            input_feature_test_df = input_feature_test_df.apply(pd.to_numeric, errors='coerce')

            logging.info("Applying preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df, target_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

           # Target encoding
            target_mapping = {'AML': 0, 'ALL': 1}
            train_target_arr = np.array(target_feature_train_df.map(target_mapping))
            test_target_arr = np.array(target_feature_test_df.map(target_mapping))

            train_arr = np.c_[input_feature_train_arr, train_target_arr]
            test_arr = np.c_[input_feature_test_arr, test_target_arr]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)