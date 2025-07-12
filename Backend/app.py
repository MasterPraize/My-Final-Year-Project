from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests
from src.password_analyzer import PasswordAnalyzer
import src.breach_checker as breach_checker

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")  # Log to file for production
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, resources={r"/api/*": {"origins": " http://localhost:8080/"}})  # Restrict to your frontend URL in production

# Initialize analyzers
password_analyzer = PasswordAnalyzer()

# Endpoints
@app.route("/api/analyze-password", methods=["POST"])
def analyze_password():
    """Analyze the strength of a provided password."""
    try:
        data = request.get_json()
        password = data.get("password")
        if not password:
            logger.error("Empty password provided")
            return jsonify({"error": "Password cannot be empty"}), 400
        
        result = password_analyzer.analyze_password(password)
        logger.info(f"Analyzed password (hash prefix: {result.get('password_hash_prefix', 'N/A')})")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error analyzing password: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/api/check-breach", methods=["POST"])
def check_breach():
    """Check if a password has been exposed in known breaches."""
    try:
        data = request.get_json()
        password = data.get("password")
        if not password:
            logger.error("Empty password provided")
            return jsonify({"error": "Password cannot be empty"}), 400
        
        result = breach_checker.check_password_breach(password)
        logger.info(f"Checked password for breaches (is_breached: {result.get('is_breached', False)})")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error checking breach: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/api/batch-check-breach", methods=["POST"])
def batch_check_breach():
    """Check multiple passwords for breaches."""
    try:
        data = request.get_json()
        passwords = data.get("passwords", [])
        if not passwords:
            logger.error("Empty password list provided")
            return jsonify({"error": "Password list cannot be empty"}), 400
        if len(passwords) > 50:
            logger.error("Too many passwords provided")
            return jsonify({"error": "Too many passwords (max 50)"}), 400
        
        results = breach_checker.batch_check_breaches(passwords)
        logger.info(f"Batch checked {len(passwords)} passwords for breaches")
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error in batch breach check: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/api/analyze-and-check", methods=["POST"])
def analyze_and_check():
    """Analyze password strength and check for breaches in one request."""
    try:
        data = request.get_json()
        password = data.get("password")
        if not password:
            logger.error("Empty password provided")
            return jsonify({"error": "Password cannot be empty"}), 400
        
        analysis_result = password_analyzer.analyze_password(password)
        breach_result = breach_checker.check_password_breach(password)
        logger.info(f"Analyzed and checked password (hash prefix: {analysis_result.get('password_hash_prefix', 'N/A')}, is_breached: {breach_result.get('is_breached', False)})")
        combined_result = {
            "analysis": analysis_result,
            "breach_check": breach_result
        }
        return jsonify(combined_result), 200
    except Exception as e:
        logger.error(f"Error in analyze-and-check: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring."""
    try:
        model_status = "Models loaded" if password_analyzer.models else "No models loaded"
        api_status = "API accessible"
        try:
            response = requests.head("https://api.pwnedpasswords.com/range/00000", timeout=5)
            if response.status_code != 200:
                api_status = "API connectivity issue"
        except requests.exceptions.RequestException:
            api_status = "API connectivity unavailable"
        return jsonify({
            "status": "healthy",
            "model_status": model_status,
            "breach_api_status": api_status
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"error": "Service unhealthy"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)  # Set debug=False for production