"""
Diabetes Prediction Model Training with Comparison
Trains multiple ML models, compares performance, and saves the best model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import json
import os

def load_data():
    """Load PIMA Indians Diabetes Dataset"""
    try:
        df = pd.read_csv('diabetes.csv')
        print("✓ Dataset loaded successfully")
    except FileNotFoundError:
        print("Creating sample diabetes dataset...")
        np.random.seed(42)
        n_samples = 768
        
        data = {
            'Pregnancies': np.random.randint(0, 17, n_samples),
            'Glucose': np.random.randint(0, 200, n_samples),
            'BloodPressure': np.random.randint(0, 130, n_samples),
            'SkinThickness': np.random.randint(0, 100, n_samples),
            'Insulin': np.random.randint(0, 850, n_samples),
            'BMI': np.random.uniform(0, 70, n_samples),
            'DiabetesPedigreeFunction': np.random.uniform(0, 2.5, n_samples),
            'Age': np.random.randint(21, 81, n_samples)
        }
        
        df = pd.DataFrame(data)
        df['Outcome'] = ((df['Glucose'] > 120) & (df['BMI'] > 30)).astype(int)
        df.to_csv('diabetes.csv', index=False)
        print("✓ Dataset created and saved")
    
    return pd.read_csv('diabetes.csv')

def preprocess_data(df):
    """Handle missing values and normalize data"""
    print("\nPreprocessing data...")
    
    # Replace zeros with NaN for certain columns
    cols_with_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)
    
    # Fill missing values with median
    df.fillna(df.median(), inplace=True)
    
    # Separate features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✓ Training samples: {len(X_train)}")
    print(f"✓ Testing samples: {len(X_test)}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns

def train_models(X_train, X_test, y_train, y_test):
    """Train and compare multiple models"""
    print("\nTraining and comparing models...\n")
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(probability=True, random_state=42, kernel='rbf')
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        metrics = {
            'accuracy': round(accuracy_score(y_test, y_pred), 4),
            'precision': round(precision_score(y_test, y_pred), 4),
            'recall': round(recall_score(y_test, y_pred), 4),
            'f1': round(f1_score(y_test, y_pred), 4),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        results[name] = {
            'model': model,
            'metrics': metrics,
            'predictions_count': len(y_test)
        }
        
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1 Score:  {metrics['f1']:.4f}")
        print()
    
    return results

def select_best_model(results):
    """Select model with best F1 score"""
    best_model_name = max(results.keys(), key=lambda k: results[k]['metrics']['f1'])
    print(f"\n{'='*60}")
    print(f"✓ Best Model: {best_model_name}")
    print(f"  F1 Score: {results[best_model_name]['metrics']['f1']:.4f}")
    print(f"{'='*60}\n")
    return best_model_name, results[best_model_name]['model']

def save_model(model, scaler, feature_names, best_model_name, results, X_train):
    """Save the best model and scaler"""
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'model_name': best_model_name,
        'all_models_metrics': {k: v['metrics'] for k, v in results.items()}
    }
    
    joblib.dump(model_data, 'model.pkl')
    print(f"✓ Model saved as 'model.pkl'")
    
    # Save feature importance if available
    if hasattr(model, 'feature_importances_'):
        importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        importance.to_csv('feature_importance.csv', index=False)
        print("✓ Feature importance saved")
    
    # Save comparison data for dashboard
    comparison_data = {
        'models': {},
        'best_model': best_model_name
    }
    
    for name, data in results.items():
        comparison_data['models'][name] = {
            'accuracy': data['metrics']['accuracy'],
            'precision': data['metrics']['precision'],
            'recall': data['metrics']['recall'],
            'f1_score': data['metrics']['f1'],
            'training_samples': len(X_train),
            'testing_samples': data['predictions_count']
        }
    
    # Save to backend folder for API access
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    if not os.path.exists(backend_dir):
        os.makedirs(backend_dir)
    
    comparison_file = os.path.join(backend_dir, 'model_comparison.json')
    with open(comparison_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"✓ Model comparison data saved to 'backend/model_comparison.json'")
    
    return comparison_data

def display_comparison_table(comparison_data):
    """Display formatted comparison table"""
    print("\n" + "="*80)
    print("MODEL PERFORMANCE COMPARISON TABLE")
    print("="*80)
    print(f"{'Model':<25} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1 Score':<10}")
    print("-"*80)
    
    for model_name, metrics in comparison_data['models'].items():
        marker = " ⭐ BEST" if model_name == comparison_data['best_model'] else ""
        print(f"{model_name:<25} {metrics['accuracy']:<10.4f} {metrics['precision']:<10.4f} "
              f"{metrics['recall']:<10.4f} {metrics['f1_score']:<10.4f}{marker}")
    
    print("="*80)

def main():
    print("="*80)
    print("DIABETES PREDICTION - MULTI-MODEL TRAINING")
    print("="*80)
    
    # Load data
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    print(f"Class distribution:\n{df['Outcome'].value_counts()}")
    
    # Preprocess
    X_train, X_test, y_train, y_test, scaler, feature_names = preprocess_data(df)
    
    # Train models
    results = train_models(X_train, X_test, y_train, y_test)
    
    # Select best model
    best_model_name, best_model = select_best_model(results)
    
    # Save model and comparison data
    comparison_data = save_model(best_model, scaler, feature_names, best_model_name, results, X_train)
    
    # Display comparison table
    display_comparison_table(comparison_data)
    
    print("\n" + "="*80)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*80)
    print(f"\nBest Model: {best_model_name}")
    print(f"All models trained and compared!")
    print(f"Dashboard can access: backend/model_comparison.json\n")

if __name__ == "__main__":
    main()
