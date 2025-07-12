
import React from 'react';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';

interface StrengthMeterProps {
  strength: 'weak' | 'moderate' | 'strong';
  score: number;
  isDarkMode: boolean;
}

const StrengthMeter: React.FC<StrengthMeterProps> = ({ strength, score, isDarkMode }) => {
  const getStrengthConfig = () => {
    switch (strength) {
      case 'weak':
        return {
          color: 'bg-red-500',
          textColor: 'text-red-500',
          bgColor: 'bg-red-100',
          icon: AlertTriangle,
          label: 'Weak',
          description: 'Your password is vulnerable to attacks'
        };
      case 'moderate':
        return {
          color: 'bg-orange-500',
          textColor: 'text-orange-500',
          bgColor: 'bg-orange-100',
          icon: Shield,
          label: 'Moderate',
          description: 'Your password has decent security'
        };
      case 'strong':
        return {
          color: 'bg-green-500',
          textColor: 'text-green-500',
          bgColor: 'bg-green-100',
          icon: CheckCircle,
          label: 'Strong',
          description: 'Your password is highly secure'
        };
    }
  };

  const config = getStrengthConfig();
  const Icon = config.icon;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className={`text-lg font-semibold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
          Password Strength
        </h3>
        <div className="flex items-center space-x-2">
          <Icon className={`w-5 h-5 ${config.textColor}`} />
          <span className={`font-bold ${config.textColor}`}>
            {config.label}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className={`w-full h-3 rounded-full overflow-hidden ${
          isDarkMode ? 'bg-gray-700' : 'bg-gray-200'
        }`}>
          <div
            className={`h-full transition-all duration-700 ease-out ${config.color}`}
            style={{ width: `${score}%` }}
          />
        </div>
        <div className="flex justify-between text-sm">
          <span className={isDarkMode ? 'text-gray-400' : 'text-gray-500'}>
            0%
          </span>
          <span className={`font-semibold ${config.textColor}`}>
            {score}%
          </span>
          <span className={isDarkMode ? 'text-gray-400' : 'text-gray-500'}>
            100%
          </span>
        </div>
      </div>

      {/* Description */}
      <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
        {config.description}
      </p>

      {/* Score Breakdown */}
      <div className={`p-4 rounded-lg ${
        isDarkMode ? 'bg-gray-700' : config.bgColor
      }`}>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className={`text-2xl font-bold ${config.textColor}`}>
              {score}
            </div>
            <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              Score
            </div>
          </div>
          <div>
            <div className={`text-2xl font-bold ${config.textColor}`}>
              {strength === 'weak' ? '1' : strength === 'moderate' ? '2' : '3'}
            </div>
            <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              Level
            </div>
          </div>
          <div>
            <div className={`text-2xl font-bold ${config.textColor}`}>
              {strength === 'weak' ? '🔓' : strength === 'moderate' ? '🔒' : '🛡️'}
            </div>
            <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              Security
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StrengthMeter;
