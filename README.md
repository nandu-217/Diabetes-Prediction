# 🩺 Diabetes Prediction System Using Machine Learning

## 📌 Project Overview

The Diabetes Prediction System is a Machine Learning-based web application that predicts the likelihood of diabetes based on a user's medical information. The system analyzes health parameters and provides instant predictions using trained machine learning models.

This project aims to assist healthcare professionals and individuals in identifying potential diabetes risks at an early stage through data-driven insights.

---

## 🚀 Features

* Diabetes risk prediction using Machine Learning
* Interactive and responsive web interface
* Real-time prediction results
* Model comparison dashboard
* Health analytics visualization
* User-friendly prediction form
* Fast and accurate predictions

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Visualization

* Matplotlib
* Plotly

---

## 📂 Project Structure

```text
Diabetes-Prediction/
│
├── backend/
│   ├── app.py
│   └── model_comparison.json
│
├── frontend/
│   ├── index.html
│   ├── predict.html
│   ├── dashboard.html
│   ├── chatbot.html
│   ├── model_comparison.html
│   ├── style.css
│   └── app.js
│
├── train_model.py
├── start_app.py
├── start.bat
├── requirements.txt
└── README.md
```

---

## 📊 Input Parameters

The model uses the following health-related features:

* Pregnancies
* Glucose Level
* Blood Pressure
* Skin Thickness
* Insulin Level
* BMI (Body Mass Index)
* Diabetes Pedigree Function
* Age

---

## 🤖 Machine Learning Models

The system evaluates and compares multiple machine learning algorithms:

* Logistic Regression
* Decision Tree
* Random Forest
* Support Vector Machine (SVM)
* K-Nearest Neighbors (KNN)

The best-performing model is selected for prediction.

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/nandu-217/Diabetes-Prediction.git
cd Diabetes-Prediction
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

### Option 1

```bash
python start_app.py
```

### Option 2

```bash
python backend/app.py
```

### Option 3

Double-click:

```text
start.bat
```

---

## 📈 Model Training

To retrain the machine learning model:

```bash
python train_model.py
```

---

## 🎯 Prediction Workflow

1. Enter patient health information.
2. Submit the form.
3. Data is sent to the Flask backend.
4. Machine Learning model processes the input.
5. Prediction result is displayed instantly.
6. Dashboard visualizes model performance.

---

## 📸 Screens

* Home Page
* Prediction Page
* Dashboard
* Model Comparison
* Health Chatbot

---

## 🔮 Future Enhancements

* Deep Learning Integration
* Doctor Recommendation System
* Cloud Deployment
* User Authentication
* Medical Report Upload
* Personalized Health Suggestions
* Mobile Application Version

---

## 📚 Learning Outcomes

Through this project:

* Machine Learning model development
* Data preprocessing and analysis
* Flask API development
* Frontend-backend integration
* Model evaluation techniques
* Full-stack project deployment

---

## 👩‍💻 Author

**Nandini Gara**

B.Tech Student | Machine Learning Enthusiast | Full Stack Developer

GitHub: https://github.com/nandu-217

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
