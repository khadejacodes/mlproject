import os
import sys
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import numpy as np
from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        model_list = list(models.items())
        for i in range(len(model_list)):
            model_name, model = model_list[i]
            model.fit(X_train, y_train) # Train model
            
            y_test_pred = model.predict(X_test)
            test_model_score = accuracy_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score

            cv_score = cross_val_score(model, X_train, y_train, cv=3)
            mean_cv_score = np.mean(cv_score)
            logging.info(f"{model_name} Mean CV Score: {mean_cv_score}")

        return report
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)