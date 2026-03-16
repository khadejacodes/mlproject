import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion method")
        try:
            # reading both files, raw and labels data
            df_raw = pd.read_csv('notebook/data/data_set_ALL_AML_train.csv') 
            df_labels = pd.read_csv('notebook/data/actual.csv')
            logging.info("Read both gene data and labels")

            # transpose - preparing the gene data
            # i. removing 'Gene Description' and 'Gene Accession Number' if they exist to keep only numbers
            accession_col = df_raw.columns[1]
            df_genes_raw = df_raw.drop(columns=[df_raw.columns[0]])
            df_genes = df_genes_raw.set_index(accession_col).T 
            # ii. cleaning the index so it matches the label ids
            df_genes.index = df_genes.index.astype(str).str.split('.').str[0]
            df_genes.index = pd.to_numeric(df_genes.index, errors='coerce')
            df_genes.index.name = 'patient'
            df_genes = df_genes.reset_index()

            # merge labels with genes
            df_labels['patient'] = pd.to_numeric(df_labels['patient'], errors='coerce')
            
            df = pd.merge(df_genes, df_labels, on='patient')
            
            if 'cancer' in df.columns:
                df.rename(columns={'cancer': 'Class'}, inplace=True)

            logging.info(f"Successfully merged data. Shape: {df.shape}")

            # saving
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # splitting
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42, stratify=df['Class'])

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    model_trainer=ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))