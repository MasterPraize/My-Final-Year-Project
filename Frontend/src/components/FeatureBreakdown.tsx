
import React from 'react';
import { Check, AlertTriangle } from 'lucide-react';

interface FeatureBreakdownProps {
  features: {
    length: number;
    hasUppercase: boolean;
    hasLowercase: boolean;
    hasDigits: boolean;
    hasSymbols: boolean;
    hasCommonWords: boolean;
    hasKeyboardPatterns: boolean;
  };
  entropy: number;
  isDarkMode: boolean;
}

const FeatureBreakdown: React.FC<FeatureBreakdownProps> = ({ features, entropy, isDarkMode }) => {
  const featureItems = [
    {
      label: 'Length',
      value: `${features.length} characters`,
      status: features.length >= 8,
      description: 'Minimum 8 characters recommended'
    },
    {
      label: 'Uppercase Letters',
      value: features.hasUppercase ? 'Present' : 'Missing',
      status: features.hasUppercase,
      description: 'A-Z characters'
    },
    {
      label: 'Lowercase Letters',
      value: features.hasLowercase ? 'Present' : 'Missing',
      status: features.hasLowercase,
      description: 'a-z characters'
    },
    {
      label: 'Numbers',
      value: features.hasDigits ? 'Present' : 'Missing',
      status: features.hasDigits,
      description: '0-9 digits'
    },
    {
      label: 'Special Characters',
      value: features.hasSymbols ? 'Present' : 'Missing',
      status: features.hasSymbols,
      description: '!@#$%^&* symbols'
    },
    {
      label: 'Common Words',
      value: features.hasCommonWords ? 'Found' : 'None',
      status: !features.hasCommonWords,
      description: 'Avoid dictionary words'
    },
    {
      label: 'Keyboard Patterns',
      value: features.hasKeyboardPatterns ? 'Found' : 'None',
      status: !features.hasKeyboardPatterns,
      description: 'Avoid sequences like qwerty'
    }
  ];

  return (
    <div className="space-y-4">
      <h3 className={`text-lg font-semibold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
        Security Features
      </h3>

      {/* Entropy Score */}
      <div className={`p-4 rounded-lg border ${
        isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-blue-50 border-blue-200'
      }`}>
        <div className="flex items-center justify-between">
          <span className={`font-medium ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`}>
            Password Entropy
          </span>
          <span className={`text-2xl font-bold ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`}>
            {entropy.toFixed(1)} bits
          </span>
        </div>
        <p className={`text-sm mt-1 ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          Higher entropy means better randomness and security
        </p>
      </div>

      {/* Feature List */}
      <div className="space-y-2">
        {featureItems.map((item, index) => (
          <div
            key={index}
            className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-200 hover:shadow-md ${
              isDarkMode 
                ? 'bg-gray-700 border-gray-600' 
                : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-center space-x-3">
              <div className={`p-1 rounded-full ${
                item.status 
                  ? 'bg-green-100 text-green-600' 
                  : 'bg-red-100 text-red-600'
              }`}>
                {item.status ? (
                  <Check className="w-4 h-4" />
                ) : (
                  <AlertTriangle className="w-4 h-4" />
                )}
              </div>
              <div>
                <div className={`font-medium ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                  {item.label}
                </div>
                <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                  {item.description}
                </div>
              </div>
            </div>
            <span className={`text-sm font-medium ${
              item.status 
                ? 'text-green-600' 
                : 'text-red-600'
            }`}>
              {item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FeatureBreakdown;
