# 🔗 Phishing URL Detection

A machine learning-based web application for detecting whether a URL is potentially **phishing** or **legitimate** based on its lexical and structural characteristics.

The application allows users to paste a URL into a web interface. The system automatically extracts URL-based features and uses a trained machine learning model to generate a prediction.

---

## 📌 Project Overview

Phishing websites are commonly designed to imitate legitimate websites in order to steal sensitive information such as credentials, personal data, or financial information.

This project develops a machine learning classification system that analyzes the structure of a URL and predicts whether it is:

- **Phishing (`0`)**
- **Legitimate (`1`)**

Unlike a traditional machine learning demo where users manually enter feature values, this application only requires the user to provide a URL. Feature extraction and prediction are performed automatically by the system.

---

## 📊 Dataset

The project uses the **PhiUSIIL Phishing URL Dataset** from the UCI Machine Learning Repository.

The original dataset contains approximately **235,000 URLs** with phishing and legitimate samples, along with URL and website-related features.

**Dataset source:**  
UCI Machine Learning Repository — PhiUSIIL Phishing URL Dataset

https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+website

### Target Labels

| Label | Class |
|------:|-------|
| `0` | Phishing |
| `1` | Legitimate |

---

## 🔄 Machine Learning Workflow

The main workflow of this project consists of:

1. Dataset Understanding
2. Exploratory Data Analysis (EDA)
3. Data Cleaning and Duplicate Handling
4. Initial Feature Selection
5. Baseline Model Training
6. Model Comparison
7. Hyperparameter Tuning
8. URL Feature Engineering
9. URL Normalization
10. Domain-Based Train-Test Split
11. Final Model Evaluation
12. Model Saving
13. FastAPI Web Integration

---

## 🔍 Exploratory Data Analysis

Several analyses were performed to understand the dataset before model training, including:

- Target class distribution
- Missing value inspection
- Duplicate URL inspection
- URL length distribution
- Domain length distribution
- Feature correlation with the target
- URL and domain characteristics

Duplicate URLs were removed before further modeling to reduce the possibility of data leakage.

---

## ⚙️ Feature Engineering

During the initial experiment, the models used features already provided by the PhiUSIIL dataset.

However, not every precomputed feature can be reproduced consistently when the application receives a completely new raw URL.

Since the deployed application only receives a URL from the user, a custom **URL feature extractor** was developed.

The same feature extraction process is used during both:

```text
Training
   ↓
URL Feature Extraction
   ↓
Machine Learning Model
```

and:

```text
User URL
   ↓
URL Feature Extraction
   ↓
Trained Model
   ↓
Prediction
```

This approach helps prevent **training-serving skew**, where features used during model training differ from those generated during real-world inference.

URL normalization is also applied before feature extraction to improve consistency between equivalent URL representations.

---

## 🧠 Models

Three classification algorithms were evaluated:

### Logistic Regression

Used as a baseline linear classification model.

### Random Forest

An ensemble tree-based model capable of learning nonlinear relationships between URL features.

Random Forest was also used in the **hyperparameter tuning** experiment using cross-validation.

### HistGradientBoosting

A gradient boosting-based classifier designed to efficiently learn complex nonlinear patterns.

After final evaluation, **HistGradientBoosting was selected as the final model** because it provided the best overall balance across the evaluation metrics.

---

## 🔧 Hyperparameter Tuning

Hyperparameter tuning was performed on the Random Forest model.

The tuning process evaluated parameters such as:

- Number of estimators
- Maximum tree depth
- Minimum samples required for splitting
- Minimum samples per leaf
- Number of features considered at each split

The optimization focused particularly on **Phishing Recall**, since failing to detect a phishing URL is considered more critical than incorrectly flagging a legitimate URL.

The tuning experiment showed that optimized parameters did not necessarily improve all test-set metrics compared with the original Random Forest configuration.

---

## 🌐 Domain-Based Evaluation

Instead of relying only on a traditional random train-test split, the final evaluation uses **GroupShuffleSplit based on URL domains**.

This ensures that URLs belonging to the same domain are not distributed across both training and testing data.

For example:

```text
Training:
example.com/page1
example.com/page2

Testing:
another-domain.com/page1
```

rather than:

```text
Training:
example.com/page1

Testing:
example.com/page2
```

The domain overlap between the final training and testing sets was verified to be **0**.

This creates a stricter and more realistic evaluation scenario because the model is tested on domains that were not seen during training.

---

## 📈 Final Model Comparison

| Model | Accuracy | F1-Score | ROC-AUC | Phishing Recall |
|---|---:|---:|---:|---:|
| Logistic Regression | 95.21% | 95.90% | 98.09% | 90.77% |
| Random Forest | 96.68% | 97.12% | 98.71% | **94.06%** |
| **HistGradientBoosting** | **96.72%** | **97.16%** | **98.80%** | 94.05% |

HistGradientBoosting achieved the highest **Accuracy, F1-Score, and ROC-AUC**.

Random Forest achieved a slightly higher Phishing Recall, but the difference was very small. Considering overall classification performance, HistGradientBoosting was selected as the final model.

---

## 🏆 Final Model

The deployed classifier uses:

**HistGradientBoostingClassifier**

Final evaluation results:

```text
Accuracy        : 96.72%
F1-Score        : 97.16%
ROC-AUC         : 98.80%
Phishing Recall : 94.05%
```

The final trained model is stored as:

```text
models/phishing_hgb_normalized.pkl
```

---

## 💻 Web Application

The machine learning model is integrated into a web application using **FastAPI**.

Users can enter a URL through the scanner interface and receive:

- Predicted class
- Model confidence score
- URL analysis information
- Phishing or legitimate classification

### Prediction Flow

```text
User enters URL
        ↓
URL Normalization
        ↓
Feature Extraction
        ↓
HistGradientBoosting Model
        ↓
Prediction
        ↓
SAFE / PHISHING
```

The frontend is rendered using HTML/CSS with Jinja2 templates, while FastAPI handles the backend prediction process.

---

## 🛠️ Tech Stack

**Machine Learning**
- Python
- Pandas
- Scikit-learn
- Joblib

**Backend**
- FastAPI
- Uvicorn

**Frontend**
- HTML
- CSS
- Jinja2

**Development**
- Jupyter Notebook
- Visual Studio Code
- Git
- GitHub

---

## 📁 Project Structure

```text
phishing-url-detection/
│
├── app/
│   ├── templates/
│   │   └── index.html
│   ├── feature_extractor.py
│   └── main.py
│
├── models/
│   └── phishing_hgb_normalized.pkl
│
├── phising_detection.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

The original dataset is not included in the repository and can be obtained from the UCI Machine Learning Repository.

---

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/phishing-url-detection.git
cd phishing-url-detection
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI application

```bash
uvicorn app.main:app --reload
```

### 4. Open the application

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

---

## ⚠️ Model Limitations

The model analyzes patterns derived primarily from the **URL structure itself**.

It does not perform a complete security inspection of the destination website, such as:

- Website reputation checking
- Real-time blacklist lookup
- Full webpage content inspection
- Malware analysis
- Domain ownership verification

Therefore, the prediction should be interpreted as a **machine learning-based assessment**, not as a guarantee that a website is completely safe or malicious.

---

## 🔮 Future Improvements

Potential improvements include:

- Improving URL feature engineering for unseen URL structures
- Probability calibration for more reliable confidence scores
- Adding domain reputation information
- Integrating real-time phishing intelligence APIs
- Improving robustness against new phishing techniques
- Model monitoring and logging
- Automated retraining pipeline
- Containerization using Docker

---

## 🌐 Live Demo

> Deployment link will be added after the application is deployed.

---

## 📄 License

This project is intended for educational and research purposes.

The PhiUSIIL dataset is provided separately through the UCI Machine Learning Repository and is subject to its respective license.
