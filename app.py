from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os
import traceback  # Add this for better error reporting
from src.pipeline.predict_pipeline import PredictPipeline

# 1. Initialize the app FIRST
app = Flask(__name__)

# 2. NOW you can define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    print("--- SIGNAL RECEIVED FROM BROWSER ---")
    if request.method == 'GET':
        return render_template('home.html')
    
    else:
        print("--- POST REQUEST DETECTED ---")
        try:
            # 1. Get the file
            file = request.files.get('file')
            if not file or file.filename == '':
                print("No file selected")
                return render_template('home.html', error="No file uploaded")

            print(f"File received: {file.filename}")
                
            # 2. Read the CSV file
            # We use file.stream.seek(0) to make sure we start reading from the top
            file.stream.seek(0)
            data = pd.read_csv(file)
            print(f"Data Loaded. Shape: {data.shape}")
                
            # 3. Clean the data
            if 'patient' in data.columns:
                data.drop(columns=['patient'], inplace=True)
            if 'Class' in data.columns:
                data.drop(columns=['Class'], inplace=True)
            print(f"Data Cleaned. New Shape: {data.shape}")

            # 4. Initialize and Predict (ONLY ONCE)
            predict_pipeline = PredictPipeline()
            print("Pipeline Initialized. Starting Prediction...")
            
            results = predict_pipeline.predict(data)
            print(f"Prediction Success: {results}")
            
            # 5. Return results to the UI
            return render_template('home.html', results=results)

        except Exception as e:
            # This will print the EXACT error to your terminal
            import traceback
            print("!!! CRITICAL ERROR !!!")
            print(traceback.format_exc()) 
            return render_template('home.html', error=str(e))
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)