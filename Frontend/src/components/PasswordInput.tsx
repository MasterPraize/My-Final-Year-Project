
import React, { useState } from 'react';
import { Eye, EyeOff, Copy, Check } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface PasswordInputProps {
  password: string;
  setPassword: (password: string) => void;
  isDarkMode: boolean;
}

const PasswordInput: React.FC<PasswordInputProps> = ({ password, setPassword, isDarkMode }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const handleCopy = async () => {
    if (!password) return;
    
    try {
      await navigator.clipboard.writeText(password);
      setCopied(true);
      toast({
        title: "Copied!",
        description: "Password copied to clipboard",
      });
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast({
        title: "Copy failed",
        description: "Could not copy password to clipboard",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-4">
      <div className="relative">
        <input
          type={showPassword ? 'text' : 'password'}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password..."
          className={`w-full px-4 py-3 pr-20 rounded-xl border-2 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            isDarkMode
              ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400'
              : 'bg-white border-gray-200 text-gray-800 placeholder-gray-500'
          }`}
        />
        
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className={`p-1 rounded-lg transition-all duration-200 hover:scale-110 ${
              isDarkMode ? 'text-gray-400 hover:text-gray-200' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>
          
          {password && (
            <button
              type="button"
              onClick={handleCopy}
              className={`p-1 rounded-lg transition-all duration-200 hover:scale-110 ${
                copied
                  ? 'text-green-500'
                  : isDarkMode
                  ? 'text-gray-400 hover:text-gray-200'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            </button>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <input
          id="show-password"
          type="checkbox"
          checked={showPassword}
          onChange={(e) => setShowPassword(e.target.checked)}
          className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        <label
          htmlFor="show-password"
          className={`text-sm cursor-pointer ${
            isDarkMode ? 'text-gray-300' : 'text-gray-600'
          }`}
        >
          Show password
        </label>
      </div>
    </div>
  );
};

export default PasswordInput;
