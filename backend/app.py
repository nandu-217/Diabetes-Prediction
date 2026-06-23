"""
Diabetes Prediction System - Flask Backend
Provides API endpoints for prediction and intelligent chatbot
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Load model
model_data = None
try:
    # Try multiple paths to find model.pkl
    model_paths = [
        'model.pkl',
        os.path.join(os.path.dirname(__file__), '..', 'model.pkl'),
        os.path.join(os.getcwd(), 'model.pkl')
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            model_data = joblib.load(path)
            print(f"✓ Model loaded successfully from {path}")
            break
    
    if model_data is None:
        print("⚠ Model not found. Please run train_model.py first")
except Exception as e:
    print(f"⚠ Error loading model: {e}")

# User history storage
user_history = {}

# Model comparison data
model_comparison_data = None
try:
    comparison_file = os.path.join(os.path.dirname(__file__), 'model_comparison.json')
    if os.path.exists(comparison_file):
        with open(comparison_file, 'r') as f:
            model_comparison_data = json.load(f)
        print("✓ Model comparison data loaded")
except Exception as e:
    print(f"⚠ Model comparison data not available: {e}")

# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.route('/predict', methods=['POST'])
def predict():
    """Predict diabetes risk based on health parameters"""
    
    if model_data is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        
        # Extract features
        features = np.array([[
            float(data.get('pregnancies', 0)),
            float(data.get('glucose', 0)),
            float(data.get('blood_pressure', 0)),
            float(data.get('skin_thickness', 0)),
            float(data.get('insulin', 0)),
            float(data.get('bmi', 0)),
            float(data.get('diabetes_pedigree', 0)),
            float(data.get('age', 0))
        ]])
        
        # Scale features
        scaler = model_data['scaler']
        features_scaled = scaler.transform(features)
        
        # Predict
        model = model_data['model']
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.6:
            risk_level = "Moderate"
        else:
            risk_level = "High"
        
        # Store in history
        user_id = data.get('user_id', 'default')
        if user_id not in user_history:
            user_history[user_id] = []
        
        user_history[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'features': data
        })
        
        # Generate recommendations
        recommendations = generate_recommendations(prediction, probability, data)
        
        response = {
            'prediction': 'Diabetic' if prediction == 1 else 'Non-Diabetic',
            'prediction_int': int(prediction),
            'risk_score': float(probability),
            'risk_percentage': round(float(probability) * 100, 2),
            'risk_level': risk_level,
            'recommendations': recommendations,
            'bmi_category': get_bmi_category(data.get('bmi', 0))
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================
# CHATBOT ENDPOINT
# ============================================================

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """Intelligent chatbot for diabetes-related queries"""
    
    try:
        data = request.json
        user_message = data.get('message', '').lower()
        user_prediction = data.get('prediction', None)
        
        # Get response based on query type
        response = generate_chatbot_response(user_message, user_prediction)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_chatbot_response(message, user_prediction=None):
    """Generate intelligent chatbot responses"""
    
    # Greeting responses
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
    if any(greet in message for greet in greetings):
        return "Hello! I'm your Diabetes Health Assistant. How can I help you today? I can explain your prediction results, suggest lifestyle changes, or answer diabetes-related questions."
    
    # Prediction explanation
    if 'explain' in message or 'result' in message or 'prediction' in message:
        if user_prediction is not None:
            if user_prediction == 1:
                return "Based on your health parameters, our model indicates a higher risk of diabetes. This means your glucose levels, BMI, and other factors suggest you should take preventive measures. I recommend consulting with a healthcare provider for a detailed evaluation."
            else:
                return "Great news! Your prediction shows low risk of diabetes. However, it's important to maintain a healthy lifestyle to keep it that way. Regular exercise, balanced diet, and routine check-ups are key."
        return "To explain your prediction, please get a prediction first by entering your health parameters on the prediction page."
    
    # Diet recommendations
    if 'diet' in message or 'food' in message or 'eat' in message or 'nutrition' in message:
        return """Here are my dietary recommendations:
        
🥗 DIET PLAN:
• Focus on whole grains (oats, brown rice, quinoa)
• Eat plenty of vegetables and leafy greens
• Choose lean proteins (fish, chicken, legumes)
• Include healthy fats (nuts, olive oil, avocado)
• Limit sugary foods and refined carbs
• Stay hydrated with 8-10 glasses of water daily
• Eat small, frequent meals (5-6 times/day)
• Avoid processed foods and sweetened beverages"""
    
    # Exercise recommendations
    if 'exercise' in message or 'workout' in message or 'physical activity' in message:
        return """Here's your personalized exercise plan:
        
💪 EXERCISE ROUTINE:
• Aerobic exercise: 30 minutes walking/jogging daily
• Strength training: 2-3 times per week
• Flexibility exercises: Yoga or stretching daily
• Start with 10-minute sessions if you're a beginner
• Gradually increase intensity and duration
• Monitor your blood sugar before and after exercise
• Stay hydrated during workouts"""
    
    # Lifestyle changes
    if 'lifestyle' in message or 'habits' in message or 'change' in message:
        return """Here are important lifestyle modifications:
        
🌟 LIFESTYLE CHANGES:
• Maintain healthy weight (BMI 18.5-24.9)
• Get 7-8 hours of quality sleep daily
• Manage stress through meditation/deep breathing
• Quit smoking and limit alcohol consumption
• Monitor blood pressure regularly
• Schedule regular health check-ups
• Track your progress and stay motivated"""
    
    # Symptoms inquiry
    if 'symptom' in message or 'sign' in message or 'feel' in message:
        return """Common diabetes symptoms to watch for:

⚠️ SYMPTOMS:
• Frequent urination (especially at night)
• Excessive thirst and hunger
• Unexplained weight loss
• Fatigue and weakness
• Blurred vision
• Slow-healing wounds
• Tingling in hands/feet
• Dark patches on skin (acanthosis nigricans)

If you experience these symptoms, consult a healthcare provider immediately."""
    
    # Risk factors
    if 'risk' in message or 'cause' in message or 'why' in message:
        return """Major risk factors for diabetes:

📊 RISK FACTORS:
• Family history of diabetes
• Overweight or obesity (high BMI)
• Sedentary lifestyle
• Age over 45 years
• High blood pressure
• Abnormal cholesterol levels
• History of gestational diabetes
• Polycystic ovary syndrome (PCOS)
• Certain ethnic backgrounds"""
    
    # Prevention
    if 'prevent' in message or 'prevention' in message:
        return """Excellent question! Here's how to prevent diabetes:

🛡️ PREVENTION STRATEGIES:
• Maintain healthy weight through balanced diet
• Exercise regularly (150 min/week moderate activity)
• Eat fiber-rich foods
• Choose whole grains over refined carbs
• Drink water instead of sugary drinks
• Control portion sizes
• Reduce stress levels
• Get adequate sleep
• Regular health screenings"""
    
    # BMI calculation
    if 'bmi' in message or 'weight' in message:
        return """BMI (Body Mass Index) is a key indicator:

📈 BMI CATEGORIES:
• Underweight: BMI < 18.5
• Normal weight: BMI 18.5-24.9
• Overweight: BMI 25-29.9
• Obese: BMI ≥ 30

A healthy BMI range is 18.5-24.9. Use the BMI calculator on our dashboard to check yours!"""
    
    # Thank you
    if 'thank' in message:
        return "You're welcome! I'm here to support your health journey. Feel free to ask me anything about diabetes prevention, management, or healthy living!"
    
    # Default response with suggestions
    return """I'd be happy to help you with diabetes-related information! You can ask me about:

💬 TOPICS I CAN HELP WITH:
• Understanding your prediction results
• Diet and nutrition plans
• Exercise recommendations
• Lifestyle changes
• Diabetes symptoms and risk factors
• Prevention strategies
• BMI and health metrics
• Healthy recipes and meal planning

Just type your question, and I'll provide personalized guidance!"""

def generate_recommendations(prediction, probability, data):
    """Generate personalized health recommendations"""
    
    recommendations = []
    
    # Glucose-based recommendations
    glucose = data.get('glucose', 0)
    if glucose > 140:
        recommendations.append({
            'category': 'Diet',
            'priority': 'high',
            'message': 'Your glucose level is elevated. Reduce sugar intake and refined carbohydrates.',
            'action': 'Limit sweets, sodas, and white bread/pasta'
        })
    
    # BMI-based recommendations
    bmi = data.get('bmi', 0)
    if bmi > 25:
        recommendations.append({
            'category': 'Weight Management',
            'priority': 'medium',
            'message': 'Your BMI indicates overweight. Consider a weight loss plan.',
            'action': 'Aim for 5-10% weight loss through diet and exercise'
        })
    
    # General recommendations based on prediction
    if prediction == 1:
        recommendations.append({
            'category': 'Medical',
            'priority': 'high',
            'message': 'Consult a healthcare provider for comprehensive evaluation.',
            'action': 'Schedule appointment with endocrinologist'
        })
        
        recommendations.append({
            'category': 'Monitoring',
            'priority': 'high',
            'message': 'Regular blood glucose monitoring is essential.',
            'action': 'Check fasting and post-meal glucose levels'
        })
    else:
        recommendations.append({
            'category': 'Prevention',
            'priority': 'low',
            'message': 'Maintain your healthy lifestyle to prevent future risk.',
            'action': 'Continue regular exercise and balanced diet'
        })
    
    # Age-based recommendation
    age = data.get('age', 0)
    if age > 45:
        recommendations.append({
            'category': 'Screening',
            'priority': 'medium',
            'message': 'Regular diabetes screening is recommended for your age group.',
            'action': 'Get HbA1c test annually'
        })
    
    return recommendations

def get_bmi_category(bmi):
    """Categorize BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# ============================================================
# HISTORY ENDPOINT
# ============================================================

@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Get user's prediction history"""
    if user_id in user_history:
        return jsonify({
            'user_id': user_id,
            'predictions': user_history[user_id],
            'total_predictions': len(user_history[user_id])
        })
    return jsonify({'user_id': user_id, 'predictions': [], 'total_predictions': 0})

# ============================================================
# MODEL COMPARISON ENDPOINT
# ============================================================

@app.route('/compare-models', methods=['GET'])
def compare_models():
    """Return performance metrics for all trained models"""
    if model_comparison_data is None:
        return jsonify({
            'error': 'Model comparison data not available. Please run train_enhanced.py first.',
            'models': {},
            'best_model': None
        }), 404
    
    return jsonify(model_comparison_data)

# ============================================================
# SERVE FRONTEND FILES
# ============================================================

import os

# Get the absolute path to frontend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("="*60)
    print("DIABETES PREDICTION SYSTEM - SERVER STARTING")
    print("="*60)
    print("\nAccess the application at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  • GET  /              - Home page")
    print("  • POST /predict       - Make prediction")
    print("  • POST /chatbot       - Chat with assistant")
    print("  • GET  /history/<id>  - Get user history")
    print("="*60)
    
    app.run(debug=True, port=5000)
