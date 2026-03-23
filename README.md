Leukemia Type Predictor: Gene Expression Analysis
🧬 Project Overview
This project is a full-stack Machine Learning application designed to classify leukemia subtypes (AML vs. ALL) using high-dimensional gene expression data. Based on the classic Golub et al. (1999) dataset, the model analyzes 7,129 gene features to provide rapid, automated diagnostic insights.

Why this matters:
Traditional diagnosis of leukemia subtypes requires intensive manual laboratory work. This tool demonstrates how Bioinformatics and Supervised Learning can assist medical professionals by providing a secondary validation layer with high statistical confidence.

🛠️ Technical Architecture
The application is built using a modular software engineering approach, ensuring scalability and ease of deployment through containerization.

Model Pipeline: Uses a robust preprocessing suite (Imputation, Scaling, and Feature Selection) followed by a Random Forest Classifier.

Backend: A Flask API handles CSV data ingestion and returns model inferences in real-time.

Logging & Exception Handling: Custom logging scripts track every prediction request, ensuring high observability.

Deployment: Fully containerized via Docker, ensuring "write once, run anywhere" consistency across local and cloud environments.

🚀 Getting Started
Prerequisites
Docker Desktop installed and running.

Installation & Local Run
Clone the repository:

Bash
git clone https://github.com/YOUR_USERNAME/leukemia-prediction-app.git
cd leukemia-prediction-app
Build the Docker Image:

Bash
docker build -t leukemia-app .
Run the Container:

Bash
docker run -p 8080:8080 leukemia-app
Access the App:
Open your browser and navigate to http://localhost:8080.

📊 Dataset & Model Performance
Source: Golub Leukemia Dataset (38 Training samples, 34 Test samples).

Features: 7,129 gene expression intensities.

Algorithm: Random Forest Classifier (Scikit-Learn 1.8.0).

Key Techniques: Recursive Feature Elimination (RFE) and Cross-Validation for hyperparameter tuning.

📂 Project Structure
Plaintext
mlproject/
├── artifacts/           # Saved Model (.pkl) and Preprocessor
├── src/
│   ├── components/      # Data Ingestion, Transformation, Model Training
│   ├── pipeline/        # Prediction and Training logic
│   ├── logger.py        # Custom logging implementation
│   └── exception.py     # Custom error handling
├── templates/           # HTML Frontend
├── app.py               # Flask Entry point
├── Dockerfile           # Container configuration
└── requirements.txt     # Python dependencies
👨‍💻 Author
Khadeja Student & Developer | Machine Learning & Mobile App Dev