import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException

class TrainPipeline:
    def __init__(self):
        # We initialize the components we built earlier
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def run_pipeline(self):
        try:
            # Step 1: Ingestion
            train_path, test_path = self.data_ingestion.initiate_data_ingestion()

            # Step 2: Transformation
            # This returns the numpy arrays and the path to the saved pkl
            train_arr, test_arr, _ = self.data_transformation.initiate_data_transformation(
                train_path, test_path
            )

            # Step 3: Model Training
            # This returns the accuracy of the best model
            accuracy = self.model_trainer.initiate_model_trainer(train_arr, test_arr)

            print(f"Training Pipeline Completed. Best Model Accuracy: {accuracy}")
            return accuracy

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()