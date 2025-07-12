"""
Breach Checker Module
Checks if passwords have been exposed in known data breaches using Have I Been Pwned API
"""

import hashlib
import requests
import logging
import time

logger = logging.getLogger(__name__)


class BreachChecker:
    """
    Class for checking password breaches using Have I Been Pwned API
    Uses k-anonymity model for privacy protection
    """

    def __init__(self):
        self.api_url = "https://api.pwnedpasswords.com/range/"
        self.request_delay = 1.5  # Delay between requests to be respectful to API
        self.last_request_time = 0

    def _rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    @staticmethod
    def _hash_password(password):
        """
        Hash password using SHA-1 for Have I Been Pwned API

        Args:
            password (str): Password to hash

        Returns:
            str: SHA-1 hash in uppercase
        """
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    def check_password_breach(self, password):
        """
        Check if password has been exposed in known breaches

        Args:
            password (str): Password to check

        Returns:
            dict: Breach check results
        """
        try:
            # Hash the password
            password_hash = self._hash_password(password)
            hash_prefix = password_hash[:5]
            hash_suffix = password_hash[5:]

            # Rate limit requests
            self._rate_limit()

            # Make API request
            response = requests.get(
                f"{self.api_url}{hash_prefix}",
                headers={'User-Agent': 'Password-Strength-Analyzer'},
                timeout=10
            )

            if response.status_code == 200:
                # Parse response
                hash_list = response.text.strip().split('\n')

                for hash_entry in hash_list:
                    if ':' in hash_entry:
                        hash_part, count = hash_entry.split(':')
                        if hash_part == hash_suffix:
                            return {
                                'is_breached': True,
                                'breach_count': int(count),
                                'message': f'Password found in {count} breaches',
                                'recommendation': 'This password has been exposed in data breaches. Choose a different password.'
                            }

                # Password not found in breaches
                return {
                    'is_breached': False,
                    'breach_count': 0,
                    'message': 'Password not found in known breaches',
                    'recommendation': 'Good! This password has not been found in known data breaches.'
                }

            elif response.status_code == 429:
                # Rate limited
                logger.warning("Rate limited by Have I Been Pwned API")
                return {
                    'error': 'Rate limited',
                    'message': 'Too many requests. Please try again later.',
                    'recommendation': 'Wait a moment before checking again.'
                }

            else:
                logger.error(f"API request failed with status code: {response.status_code}")
                return {
                    'error': 'API request failed',
                    'message': f'Unable to check breaches (HTTP {response.status_code})',
                    'recommendation': 'Breach check temporarily unavailable.'
                }

        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return {
                'error': 'Timeout',
                'message': 'Request timed out',
                'recommendation': 'Breach check temporarily unavailable due to network issues.'
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during breach check: {str(e)}")
            return {
                'error': 'Network error',
                'message': 'Unable to connect to breach database',
                'recommendation': 'Breach check temporarily unavailable due to network issues.'
            }

        except Exception as e:
            logger.error(f"Unexpected error during breach check: {str(e)}")
            return {
                'error': 'Unexpected error',
                'message': 'An unexpected error occurred',
                'recommendation': 'Breach check temporarily unavailable.'
            }

    def batch_check_breaches(self, passwords):
        """
        Check multiple passwords for breaches with rate limiting

        Args:
            passwords (list): List of passwords to check

        Returns:
            list: List of breach check results
        """
        results = []

        for i, password in enumerate(passwords):
            logger.info(f"Checking password {i + 1}/{len(passwords)} for breaches")
            result = self.check_password_breach(password)
            results.append(result)

            # Add extra delay for batch processing
            if i < len(passwords) - 1:  # Don't delay after the last request
                time.sleep(0.5)

        return results

# if __name__ == '__main__':
#     # Create an instance of BreachChecker
#     checker = BreachChecker()
#
#     # Test 1: Hash a password
#     test_password = "password123"
#     hashed = checker._hash_password(test_password)
#     print(f"Hashed {test_password}: {hashed}")
#     print(f"Prefix: {hashed[:5]}, Suffix: {hashed[5:]}")
#
#     # Test 2: Check a single password (note: this requires internet and API access)
#     result = checker.check_password_breach(test_password)
#     print(f"Single password check: {result}")
#
#     # Test 3: Check multiple passwords
#     test_passwords = ["password123", "unique_password"]
#     batch_results = checker.batch_check_breaches(test_passwords)
#     print(f"Batch check results: {batch_results}")
#
#     # Test 4: Test rate limiting (manual check by running multiple times)
#     print("Testing rate limit - run this block again after a few seconds to see delay.")
#
#     # Test 5: Test edge case (empty password)
#     try:
#         empty_result = checker.check_password_breach("")
#         print(f"Empty password check: {empty_result}")
#     except ValueError as e:
#         print(f"Empty password test: {str(e)}")
#
#     # Test 6: Test invalid input
#     try:
#         checker.check_password_breach(None)
#     except ValueError as e:
#         print(f"Invalid input test: {str(e)}")
#
#     try:
#         checker.batch_check_breaches(["password", 123])
#     except ValueError as e:
#         print(f"Invalid batch input test: {str(e)}")