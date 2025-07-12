
import React from 'react';
import { Eye, EyeOff } from 'lucide-react';

interface DarkModeToggleProps {
  isDarkMode: boolean;
  setIsDarkMode: (isDarkMode: boolean) => void;
}

const DarkModeToggle: React.FC<DarkModeToggleProps> = ({ isDarkMode, setIsDarkMode }) => {
  return (
    <div className="flex items-center justify-center mt-6">
      <button
        onClick={() => setIsDarkMode(!isDarkMode)}
        className={`relative inline-flex items-center h-8 w-16 rounded-full transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
          isDarkMode ? 'bg-blue-600' : 'bg-gray-300'
        }`}
      >
        <span
          className={`inline-block w-6 h-6 transform transition-all duration-300 bg-white rounded-full shadow-lg ${
            isDarkMode ? 'translate-x-8' : 'translate-x-1'
          }`}
        >
          <span className="flex items-center justify-center w-full h-full">
            {isDarkMode ? (
              <EyeOff className="w-3 h-3 text-blue-600" />
            ) : (
              <Eye className="w-3 h-3 text-gray-600" />
            )}
          </span>
        </span>
      </button>
      <span className={`ml-3 text-sm font-medium ${
        isDarkMode ? 'text-gray-300' : 'text-gray-700'
      }`}>
        {isDarkMode ? 'Dark Mode' : 'Light Mode'}
      </span>
    </div>
  );
};

export default DarkModeToggle;
