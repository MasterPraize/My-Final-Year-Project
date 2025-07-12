
import React from 'react';
import { Lightbulb, CheckCircle } from 'lucide-react';

interface SuggestionsProps {
  suggestions: string[];
  isDarkMode: boolean;
}

const Suggestions: React.FC<SuggestionsProps> = ({ suggestions, isDarkMode }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <Lightbulb className={`w-5 h-5 ${isDarkMode ? 'text-yellow-400' : 'text-yellow-500'}`} />
        <h3 className={`text-lg font-semibold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
          Improvement Suggestions
        </h3>
      </div>

      {suggestions.length === 0 ? (
        <div className={`p-4 rounded-lg border ${
          isDarkMode ? 'bg-green-900/30 border-green-700' : 'bg-green-50 border-green-200'
        }`}>
          <div className="flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <span className={`font-medium ${isDarkMode ? 'text-green-400' : 'text-green-600'}`}>
              Excellent! Your password meets all security criteria.
            </span>
          </div>
        </div>
      ) : (
        <div className="space-y-2">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg border transition-all duration-200 hover:shadow-md ${
                isDarkMode 
                  ? 'bg-orange-900/30 border-orange-700' 
                  : 'bg-orange-50 border-orange-200'
              }`}
            >
              <div className="flex items-start space-x-3">
                <div className={`mt-0.5 w-2 h-2 rounded-full ${
                  isDarkMode ? 'bg-orange-400' : 'bg-orange-500'
                }`} />
                <span className={`text-sm ${
                  isDarkMode ? 'text-orange-300' : 'text-orange-700'
                }`}>
                  {suggestion}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Security Tips */}
      <div className={`p-4 rounded-lg border ${
        isDarkMode ? 'bg-blue-900/30 border-blue-700' : 'bg-blue-50 border-blue-200'
      }`}>
        <h4 className={`font-medium mb-2 ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`}>
          💡 Security Tips:
        </h4>
        <ul className={`text-sm space-y-1 ${isDarkMode ? 'text-blue-300' : 'text-blue-700'}`}>
          <li>• Use a unique password for each account</li>
          <li>• Consider using a password manager</li>
          <li>• Enable two-factor authentication when available</li>
          <li>• Avoid personal information in passwords</li>
        </ul>
      </div>
    </div>
  );
};

export default Suggestions;
