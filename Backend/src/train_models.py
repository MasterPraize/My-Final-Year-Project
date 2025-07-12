"""
Model Trainer Script
Trains and evaluates ML models for password strength prediction using real or synthetic datasets
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import joblib
import logging
import os
from password_analyzer import check_password_features, PasswordAnalyzer


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# i imported password_analyzer so that the Feature names matches PasswordAnalyzer.feature_names
feature_names = [
    'length', 'has_upper', 'has_lower', 'has_digit', 'has_special',
    'char_diversity', 'sequential_chars', 'repeated_chars', 'common_patterns', 'entropy'
]


def load_dataset(file_path: str, password_column: str = 'password', strength_column: str = None) -> pd.DataFrame:
    """
    Load dataset from CSV and preprocess it.
    If strength_column is None, generate labels using zxcvbn.
    """
    try:
        if strength_column:
            df = pd.read_csv(file_path, usecols=[password_column, strength_column],
                             dtype={password_column: str, strength_column: int})
        else:
            df = pd.read_csv(file_path, usecols=[password_column], dtype=str)
        logger.info(f"Loaded dataset from {file_path}")
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {str(e)}")
        raise

    df = df.dropna(subset=[password_column])
    df[password_column] = df[password_column].astype(str)

    analyzer = PasswordAnalyzer()
    data = []
    for _, row in df.iterrows():
        try:
            password = row[password_column]
            features = check_password_features(password)
            if strength_column and strength_column in df.columns:
                label = min(2, int(row[strength_column]))  # Ensure labels are 0-2
            else:
                analysis = analyzer.zxcvbn_analysis(password)
                label = min(2, analysis.get('score', 0) // 25)  # Map zxcvbn score to 0-2
            data.append({**features, 'strength': label})
        except Exception as e:
            logger.warning(f"Skipping password due to error: {str(e)}")
            continue

    columns = feature_names + ['strength']
    result_df = pd.DataFrame(data, columns=columns)
    logger.info(f"Processed dataset with {len(result_df)} samples")
    logger.info(f"Class distribution: {result_df['strength'].value_counts().to_dict()}")

    # Balance dataset
    if not result_df.empty:
        target_samples = 15000
        samples_per_class = target_samples // 3
        balanced_df = pd.DataFrame()
        for strength in range(3):
            class_df = result_df[result_df['strength'] == strength]
            if not class_df.empty:
                sampled_df = class_df.sample(n=samples_per_class, random_state=42, replace=True)
                balanced_df = pd.concat([balanced_df, sampled_df], ignore_index=True)
        result_df = balanced_df
        logger.info(f"Balanced dataset with {len(result_df)} samples")
        logger.info(f"Class distribution after balancing: {result_df['strength'].value_counts().to_dict()}")

    return result_df


def generate_synthetic_dataset(n_samples: int = 15000) -> pd.DataFrame:
    """Generate synthetic dataset if real data is unavailable."""
    logger.info(f"Generating synthetic dataset with {n_samples} samples")
    passwords = []
    labels = []
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
    weak_patterns = ['password', '123456', 'qwerty', 'abc123', 'admin']
    samples_per_class = n_samples // 3
    for strength in [0, 1, 2]:
        for _ in range(samples_per_class):
            if strength == 0:
                password = np.random.choice(weak_patterns)
            elif strength == 1:
                base = np.random.choice(weak_patterns)
                password = base + str(np.random.randint(1, 100)) + np.random.choice(['!', '@', '#'])
            else:
                password = ''.join(np.random.choice(list(chars), size=np.random.randint(12, 16)))
            passwords.append(password)
            labels.append(strength)

    data = []
    for password, label in zip(passwords, labels):
        try:
            features = check_password_features(password)
            data.append({**features, 'strength': label})
        except Exception as e:
            logger.warning(f"Skipping synthetic password due to error: {str(e)}")
            continue

    columns = feature_names + ['strength']
    df = pd.DataFrame(data, columns=columns)
    logger.info(f"Generated dataset with {len(df)} samples")
    logger.info(f"Class distribution: {df['strength'].value_counts().to_dict()}")
    return df


def evaluate_model(model, model_name: str, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Evaluate a model and return performance metrics."""
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
        metrics = {
            'accuracy': round(accuracy, 3),
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1, 3)
        }
        logger.info(f"Evaluation metrics for {model_name}: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Failed to evaluate {model_name}: {str(e)}")
        return {'error': str(e)}


# Load datasets
data_files = [
    r"C:\Users\Cornell O. David\Desktop\Password Strength Analyser\Backend\src\data\common_passwords.csv",
    r"C:\Users\Cornell O. David\Desktop\Password Strength Analyser\Backend\src\data\passwords.csv"
]
datasets = []
for file_path in data_files:
    if os.path.exists(file_path):
        datasets.append(load_dataset(file_path))
    else:
        logger.warning(f"Dataset not found: {file_path}")

if not datasets:
    logger.info("No real datasets found, using synthetic data")
    datasets.append(generate_synthetic_dataset(n_samples=10000))

df = pd.concat(datasets, ignore_index=True) if datasets else pd.DataFrame()

# Prepare training and test data
if df.empty:
    raise ValueError("No valid data available for training")
X = df[feature_names]
y = df['strength']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
logger.info(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_train_df = pd.DataFrame(X_train_scaled, columns=feature_names)
X_test_scaled = scaler.transform(X_test)
X_test_df = pd.DataFrame(X_test_scaled, columns=feature_names)

# Define models
models = {
    'logistic_regression': LogisticRegression(random_state=42, max_iter=2000),
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'xgboost': XGBClassifier(random_state=42, eval_metric='logloss')
}

# Train, evaluate, and save models
os.makedirs('models', exist_ok=True)
evaluation_results = {}
for model_name, model in models.items():
    try:
        # Train model
        model.fit(X_train_df, y_train)
        joblib.dump(model, f'models/{model_name}_model.joblib')
        logger.info(f"Trained and saved {model_name} model")

        # Evaluate model
        metrics = evaluate_model(model, model_name, X_test_df, y_test)
        evaluation_results[model_name] = metrics
    except Exception as e:
        logger.error(f"Failed to train or evaluate {model_name} model: {str(e)}")

# Save scaler
joblib.dump(scaler, 'models/scaler.joblib')
logger.info("Saved scaler")

# # Print evaluation summary
# print("\nModel Evaluation Summary:")
# print("-" * 50)
# print(f"{'Model':<20} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
# print("-" * 50)
# for model_name, metrics in evaluation_results.items():
#     if 'error' not in metrics:
#         print(
#             f"{model_name:<20} {metrics['accuracy']:<10.3f} {metrics['precision']:<10.3f} {metrics['recall']:<10.3f} {metrics['f1_score']:<10.3f}")
#     else:
#         print(f"{model_name:<20} Error: {metrics['error']}")
# print("-" * 50)
