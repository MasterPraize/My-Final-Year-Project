import os
import logging
import joblib
from password_analyzer import PasswordAnalyzer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_model_loading():
    """Test script to verify that trained models and scaler are found and loaded correctly."""
    # Define model and scaler paths (same as in PasswordAnalyzer)
    model_paths = {
        'logistic_regression': 'models/logistic_regression_model.joblib',
        'random_forest': 'models/random_forest_model.joblib',
        'xgboost': 'models/xgboost_model.joblib'
    }
    scaler_path = 'models/scaler.joblib'

    # Test 1: Check if model and scaler files exist
    logger.info("Test 1: Checking if model and scaler files exist")
    all_files_exist = True
    for model_name, file_path in model_paths.items():
        if os.path.exists(file_path):
            logger.info(f"Found {model_name} model at {file_path}")
        else:
            logger.error(f"Model file not found: {file_path}")
            all_files_exist = False

    if os.path.exists(scaler_path):
        logger.info(f"Found scaler at {scaler_path}")
    else:
        logger.error(f"Scaler file not found: {scaler_path}")
        all_files_exist = False

    if not all_files_exist:
        logger.error("Test 1 Failed: One or more model/scaler files are missing")
        return False
    else:
        logger.info("Test 1 Passed: All model and scaler files found")

    # Test 2: Load and initialize PasswordAnalyzer
    logger.info("Test 2: Loading PasswordAnalyzer with models")
    try:
        analyzer = PasswordAnalyzer(model_paths=model_paths)
        if not analyzer.models:
            logger.error("No models loaded in PasswordAnalyzer")
            return False
        if not analyzer.scaler:
            logger.error("Scaler not loaded in PasswordAnalyzer")
            return False
        logger.info(f"Successfully loaded {len(analyzer.models)} models and scaler")
    except Exception as e:
        logger.error(f"Test 2 Failed: Error loading PasswordAnalyzer - {str(e)}")
        return False
    logger.info("Test 2 Passed: PasswordAnalyzer initialized successfully")

    # Test 3: Analyze a sample password
    logger.info("Test 3: Analyzing a sample password")
    test_password = "TestP@ssw0rd123"
    try:
        result = analyzer.analyze_password(test_password)
        if 'error' in result:
            logger.error(f"Test 3 Failed: Error analyzing password - {result['error']}")
            return False
        
        # Check ML model predictions
        ml_results = result['analyses']['ml_models']
        if not isinstance(ml_results.get('predictions'), dict):
            logger.error("Test 3 Failed: No ML model predictions available")
            return False
        
        for model_name, prediction in ml_results['predictions'].items():
            if 'error' in prediction:
                logger.error(f"Test 3 Failed: Error in {model_name} prediction - {prediction['error']}")
                return False
            logger.info(f"{model_name} prediction: Score={prediction['score']}, Strength={prediction['strength']}, Confidence={prediction['confidence']}")
        
        logger.info(f"Overall Score: {result['overall']['score']}, Strength: {result['overall']['strength']}")
        logger.info(f"Feedback: {result['feedback']}")
        logger.info("Test 3 Passed: Password analysis completed successfully")
    except Exception as e:
        logger.error(f"Test 3 Failed: Error during password analysis - {str(e)}")
        return False

    return True

if __name__ == "__main__":
    logger.info("Starting model loading tests")
    success = test_model_loading()
    if success:
        logger.info("All tests passed successfully!")
    else:
        logger.error("One or more tests failed")