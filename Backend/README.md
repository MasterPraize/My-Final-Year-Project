# Password Strength Analyzer with Machine Learning

A comprehensive password strength analysis system that combines rule-based analysis, the zxcvbn library, machine learning models, and breach checking using the "Have I Been Pwned" API.

## Features

### Core Analysis Methods
- **zxcvbn Integration**: Advanced pattern matching and entropy calculation
- **Machine Learning Models**: 
  - Logistic Regression
  - Random Forest
  - XGBoost
- **Breach Checking**: Integration with Have I Been Pwned API using k-anonymity

### API Endpoints
- `GET /health` - Health check
- `POST /analyze` - Analyze single password
- `POST /batch-analyze` - Analyze multiple passwords
- `POST /train` - Train ML models
- `GET /model-performance` - Get model performance metrics

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd password-strength-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Usage

### Single Password Analysis

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "password": "MySecureP@ssw0rd123!",
    "check_breach": true
  }'
```

### Batch Password Analysis

```bash
curl -X POST http://localhost:5000/batch-analyze \
  -H "Content-Type: application/json" \
  -d '{
    "passwords": ["password123", "SecureP@ss!", "VeryStr0ng!"],
    "check_breach": false
  }'
```

### Train Models

```bash
curl -X POST http://localhost:5000/train \
  -H "Content-Type: application/json" \
  -d '{}'
```

## API Response Format

### Password Analysis Response
```json
{
  "password_hash_prefix": "a665a45e",
  "length": 16,
  "analyses": {
    "rule_based": {
      "method": "rule_based",
      "score": 85,
      "strength": "Strong",
      "feedback": []
    },
    "zxcvbn": {
      "method": "zxcvbn",
      "score": 75,
      "strength": "Good",
      "crack_time": "centuries",
      "feedback": [],
      "warning": ""
    },
    "ml_models": {
      "method": "ml_models",
      "predictions": {
        "logistic_regression": {
          "score": 82.5,
          "strength": "Very Strong",
          "confidence": 0.825
        },
        "random_forest": {
          "score": 78.3,
          "strength": "Strong",
          "confidence": 0.783
        },
        "xgboost": {
          "score": 80.1,
          "strength": "Very Strong",
          "confidence": 0.801
        }
      }
    }
  },
  "breach_check": {
    "is_breached": false,
    "breach_count": 0,
    "message": "Password not found in known breaches",
    "recommendation": "Good! This password has not been found in known data breaches."
  },
  "overall": {
    "score": 80.2,
    "strength": "Very Strong"
  }
}
```

## Machine Learning Features

The system extracts the following features from passwords for ML analysis:

1. **Length** - Total character count
2. **Character Types** - Presence of uppercase, lowercase, digits, special characters
3. **Character Diversity** - Ratio of unique characters to total length
4. **Sequential Characters** - Count of sequential character patterns
5. **Repeated Characters** - Count of repeated character patterns
6. **Common Patterns** - Detection of keyboard patterns and common words
7. **Entropy** - Shannon entropy calculation

## Model Training

The system can train models using:
- Custom datasets (CSV format)
- Synthetic dataset generation (default)

Models are automatically saved to the `models/` directory and loaded on application startup.

### Performance Metrics

All models are evaluated using:
- Accuracy
- Precision
- Recall
- F1 Score
- Cross-validation scores

## Security Features

### Breach Checking
- Uses Have I Been Pwned API with k-anonymity
- Rate limiting to respect API guidelines
- Secure SHA-1 hashing (only first 5 characters sent)

### Privacy Protection
- Passwords are never logged in plain text
- Only SHA-256 hash prefixes are logged for debugging
- Secure handling of sensitive data

## Testing

Run the test suite:

```bash
python test_api.py
```

This will test all API endpoints with various password examples.

## Project Structure

```
password-strength-analyzer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── test_api.py           # API test suite
├── src/
│   ├── __init__.py
│   ├── password_analyzer.py    # Core analysis logic
│   ├── breach_checker.py       # Breach checking functionality
│   ├── model_trainer.py        # ML model training
│   └── utils.py                # Utility functions
├── models/               # Trained ML models (created automatically)
└── data/                # Dataset storage (created automatically)
```

## Configuration

### Environment Variables
- `FLASK_ENV` - Set to 'development' for debug mode
- `FLASK_PORT` - Port to run the application (default: 5000)

### Rate Limiting
The breach checker implements rate limiting (1.5 seconds between requests) to respect the Have I Been Pwned API guidelines.

## Extensibility

The system is designed for easy extension:

1. **Add New Models**: Extend `ModelTrainer` class
2. **Custom Features**: Add feature extraction methods to `PasswordAnalyzer`
3. **Additional APIs**: Integrate other security APIs in similar modules
4. **Custom Datasets**: Support for various dataset formats

## Dependencies

- **Flask**: Web framework
- **pandas**: Data manipulation
- **scikit-learn**: Machine learning algorithms
- **xgboost**: Gradient boosting framework
- **zxcvbn**: Password strength estimation
- **requests**: HTTP client for API calls
- **joblib**: Model serialization
- **numpy**: Numerical computing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request


## Acknowledgments

- Have I Been Pwned API for breach data
- zxcvbn library for advanced password analysis
- scikit-learn and XGBoost communities for ML frameworks
