"""
Password Strength Analyzer
Core module for analyzing and generating secure passwords
"""

import hashlib
import re
import numpy as np
import pandas as pd
from zxcvbn import zxcvbn
import logging
import joblib
import os
import string
import secrets
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Compiled regex patterns for performance
RE_UPPER = re.compile(r'[A-Z]')
RE_LOWER = re.compile(r'[a-z]')
RE_DIGIT = re.compile(r'\d')
RE_SPECIAL = re.compile(r'[!@#$%^&*(),.?":{}|<>]')

# Utility functions for loading models and scaler
def load_model(file_path: str) -> Optional[Any]:
    """Load a model from a file."""
    if os.path.exists(file_path):
        try:
            model = joblib.load(file_path)
            logger.info(f"Loaded model from {file_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model from {file_path}: {str(e)}")
    return None

def load_scaler() -> Optional[Any]:
    """Load the scaler from a file."""
    scaler_path = 'models/scaler.joblib'
    if os.path.exists(scaler_path):
        try:
            scaler = joblib.load(scaler_path)
            logger.info(f"Loaded scaler from {scaler_path}")
            return scaler
        except Exception as e:
            logger.error(f"Failed to load scaler from {scaler_path}: {str(e)}")
    return None

def sanitize_input(input_string: str, max_length: int = 1000) -> str:
    """Sanitize input string for security."""
    if not isinstance(input_string, str):
        return ""
    sanitized = input_string[:max_length]
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\n\t')
    return sanitized

def check_password_features(password: str) -> Dict[str, Any]:
    """Extract common password features for validation and analysis."""
    features = {
        'length': len(password),
        'has_upper': bool(RE_UPPER.search(password)),
        'has_lower': bool(RE_LOWER.search(password)),
        'has_digit': bool(RE_DIGIT.search(password)),
        'has_special': bool(RE_SPECIAL.search(password)),
        'sequential_chars': 0,
        'repeated_chars': 0,
        'common_patterns': 0,
        'entropy': 0.0,
        'char_diversity': len(set(password)) / len(password) if len(password) > 0 else 0
    }
    for i in range(len(password) - 2):
        if (ord(password[i + 1]) == ord(password[i]) + 1 and
                ord(password[i + 2]) == ord(password[i + 1]) + 1):
            features['sequential_chars'] += 1
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            features['repeated_chars'] += 1
    patterns = ['123', 'abc', 'qwe', 'asd', 'zxc', '!@#', 'password', '123456', 'admin']
    for pattern in patterns:
        if pattern.lower() in password.lower():
            features['common_patterns'] += 1
    if password:
        char_counts = {}
        for char in password:
            char_counts[char] = char_counts.get(char, 0) + 1
        entropy = 0
        length = len(password)
        for count in char_counts.values():
            probability = count / length
            entropy -= probability * np.log2(probability)
        features['entropy'] = entropy
    return features

def generate_feedback(features: Dict[str, Any]) -> list:
    """Generate feedback based on password features."""
    feedback = []
    if features['length'] <= 7:
        feedback.append("Password is too short (minimum 8 characters)")
    elif features['length'] < 12:
        feedback.append("Consider using a longer password (12+ characters)")
    if not features['has_upper']:
        feedback.append("Add uppercase letters")
    if not features['has_lower']:
        feedback.append("Add lowercase letters")
    if not features['has_digit']:
        feedback.append("Add numbers")
    if not features['has_special']:
        feedback.append("Add special characters")
    if features['repeated_chars'] > 0:
        feedback.append("Avoid repeating characters")
    if features['sequential_chars'] > 0:
        feedback.append("Avoid sequential characters")
    if features['common_patterns'] > 0:
        feedback.append("Avoid common patterns")
    return feedback


class PasswordAnalyzer:
    """Class for analyzing password strength using multiple methods."""
    def __init__(self, model_paths: Dict[str, str] = None, config: Dict[str, Any] = None):
        self.models = {}
        self.feature_names = [
            'length', 'has_upper', 'has_lower', 'has_digit', 'has_special',
            'char_diversity', 'sequential_chars', 'repeated_chars',
            'common_patterns', 'entropy'
        ]
        self.model_paths = model_paths or {
            'logistic_regression': 'models/logistic_regression_model.joblib',
            'random_forest': 'models/random_forest_model.joblib',
            'xgboost': 'models/xgboost_model.joblib'
        }
        self.config = config or {
            'min_length': 8,
            'score_thresholds': {'very_weak': 20, 'weak': 40, 'moderate': 60, 'strong': 80}
        }
        self.scaler = load_scaler()
        for model_name, file_path in self.model_paths.items():
            model = load_model(file_path)
            if model:
                self.models[model_name] = model
        if self.models:
            logger.info(f"Successfully loaded {len(self.models)} models")
        else:
            logger.warning("No models loaded")

    def extract_features(self, password: str) -> pd.DataFrame:
        """Extract features for ML model prediction or rule-based analysis."""
        password = sanitize_input(password)
        if not password:
            raise ValueError("Password must be a valid string")
        try:
            password.encode('ascii')
        except UnicodeEncodeError:
            logger.warning("Non-ASCII characters detected in password")
        features = check_password_features(password)
        features_df = pd.DataFrame([features], columns=self.feature_names)
        if self.scaler:
            features_df = pd.DataFrame(
                self.scaler.transform(features_df),
                columns=self.feature_names
            )
        logger.debug(f"Features extracted: {features_df.to_dict('records')[0]}")
        return features_df

    def zxcvbn_analysis(self, password: str) -> Dict[str, Any]:
        """Analyze password using zxcvbn library."""
        password = sanitize_input(password)
        # Truncate password for zxcvbn to avoid 72-character limit
        zxcvbn_password = password[:72]
        try:
            result = zxcvbn(zxcvbn_password)
            strength_levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong']
            return {
                'method': 'zxcvbn',
                'score': result['score'] * 25,
                'strength': strength_levels[result['score']],
                'feedback': result['feedback']['suggestions'],
                'warning': result['feedback']['warning'] or ''
            }
        except Exception as e:
            logger.error(f"zxcvbn analysis failed: {str(e)}")
            return {
                'method': 'zxcvbn',
                'error': str(e),
                'score': 0,
                'strength': 'Unknown',
                'crack_time': 'N/A',
                'feedback': ['Unable to analyze with zxcvbn'],
                'warning': 'Analysis failed'
            }

    def ml_analysis(self, password: str) -> Dict[str, Any]:
        """Analyze password using trained ML models."""
        predictions = {}
        if not self.models:
            return {'method': 'ml_models', 'error': 'No models loaded', 'predictions': predictions}
        features = self.extract_features(password)
        for model_name, model in self.models.items():
            try:
                prob = model.predict_proba(features)[0]
                logger.debug(f"Model {model_name} probabilities: {prob}")
                strength_prob = prob[2] if len(prob) > 2 else prob[1] if len(prob) > 1 else prob[0]
                score = strength_prob * 50  # Scale to 0-100
                thresholds = self.config['score_thresholds']
                strength = (
                    "Very Weak" if score < thresholds['very_weak'] else
                    "Weak" if score < thresholds['weak'] else
                    "Moderate" if score < thresholds['moderate'] else
                    "Strong" if score < thresholds['strong'] else
                    "Very Strong"
                )
                predictions[model_name] = {
                    'score': round(score, 2),
                    'strength': strength,
                    'confidence': round(strength_prob, 3),
                    'model_name': model_name
                }
            except Exception as e:
                logger.error(f"Error with model {model_name}: {str(e)}")
                predictions[model_name] = {'error': str(e), 'model_name': model_name}
        return {'method': 'ml_models', 'predictions': predictions}

    def analyze_password(self, password: str) -> Dict[str, Any]:
        """Comprehensive password analysis using all methods."""
        password = sanitize_input(password)
        if not password:
            return {'error': 'Password cannot be empty'}
        password_hash = hashlib.sha256(password.encode()).hexdigest()[:8]
        logger.info(f"Analyzing password with hash prefix: {password_hash}")
        features_df = self.extract_features(password)
        results = {
            'password_hash_prefix': password_hash,
            'length': len(password),
            'analyses': {},
            'feedback': []
        }
        results['analyses']['zxcvbn'] = self.zxcvbn_analysis(password)
        results['analyses']['ml_models'] = self.ml_analysis(password)
        combined_feedback = set()
        if 'feedback' in results['analyses']['zxcvbn']:
            combined_feedback.update(results['analyses']['zxcvbn']['feedback'])
        # Add zxcvbn warning to combined feedback if present and not empty
        zxcvbn_warning = results['analyses']['zxcvbn'].get('warning', '')
        if zxcvbn_warning:
            combined_feedback.add(zxcvbn_warning)
        results['feedback'] = list(combined_feedback)
        scores = []
        if 'score' in results['analyses']['zxcvbn']:
            scores.append(results['analyses']['zxcvbn']['score'])
        ml_results = results['analyses']['ml_models']
        if isinstance(ml_results.get('predictions'), dict):
            for model_pred in ml_results['predictions'].values():
                if 'score' in model_pred:
                    scores.append(model_pred['score'])
        if scores:
            overall_score = sum(scores) / len(scores)
            thresholds = self.config['score_thresholds']
            strength = (
                "Very Weak" if overall_score < thresholds['very_weak'] else
                "Weak" if overall_score < thresholds['weak'] else
                "Moderate" if overall_score < thresholds['moderate'] else
                "Strong" if overall_score < thresholds['strong'] else
                "Very Strong"
            )
            results['overall'] = {
                'score': round(overall_score, 2),
                'strength': strength
            }
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    analyzer = PasswordAnalyzer()
    test_passwords = ["password123", "Str0ngP@ssw0rd!", "abc123", "", "a" * 1000]

    for password in test_passwords:
        print(f"\nAnalyzing password: {'*' * len(password) if password else '(empty)'}")
        result = analyzer.analyze_password(password)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Password Hash Prefix: {result.get('password_hash_prefix', 'N/A')}")
            print(f"Length: {result.get('length', 'N/A')}")
            print(f"Overall Score: {result['overall']['score']}")
            print(f"Overall Strength: {result['overall']['strength']}")
            print(f"Combined Feedback: {result.get('feedback', [])}")
            print("\nzxcvbn Analysis:")
            zxcvbn_result = result['analyses']['zxcvbn']
            print(f"Score: {zxcvbn_result.get('score', 'N/A')}")
            print(f"Strength: {zxcvbn_result.get('strength', 'N/A')}")
            print(f"Crack Time: {zxcvbn_result.get('crack_time', 'N/A')}")
            print(f"Feedback: {zxcvbn_result.get('feedback', [])}")
            print(f"Warning: {zxcvbn_result.get('warning', 'N/A')}")
            print("\nML Models Analysis:")
            ml_results = result['analyses']['ml_models']
            if isinstance(ml_results.get('predictions'), dict):
                for model_pred in ml_results['predictions'].values():
                    print(f"{model_pred.get('model_name', 'Unknown')}:")
                    print(f"  Score: {model_pred.get('score', 'N/A')}")
                    print(f"  Strength: {model_pred.get('strength', 'N/A')}")
                    print(f"  Confidence: {model_pred.get('confidence', 'N/A')}")
            else:
                print(f"Error: {ml_results.get('error', 'No predictions available')}")
        print("-" * 50)
