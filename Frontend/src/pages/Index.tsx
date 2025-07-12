
import React, { useState, useEffect } from 'react';
import PasswordInput from '../components/PasswordInput';
import StrengthMeter from '../components/StrengthMeter';
import FeatureBreakdown from '../components/FeatureBreakdown';
import Suggestions from '../components/Suggestions';
import DarkModeToggle from '../components/DarkModeToggle';
import { Shield, Lock } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface PasswordAnalysis {
  strength: 'weak' | 'moderate' | 'strong';
  score: number;
  entropy: number;
  suggestions: string[];
  features: {
    length: number;
    hasUppercase: boolean;
    hasLowercase: boolean;
    hasDigits: boolean;
    hasSymbols: boolean;
    hasCommonWords: boolean;
    hasKeyboardPatterns: boolean;
  };
}

const Index = () => {
  const [password, setPassword] = useState('');
  const [analysis, setAnalysis] = useState<PasswordAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const { toast } = useToast();

  // Real-time analysis for immediate feedback
  useEffect(() => {
    if (password) {
      analyzePasswordLocally();
    } else {
      setAnalysis(null);
    }
  }, [password]);

  const analyzePasswordLocally = () => {
    const features = {
      length: password.length,
      hasUppercase: /[A-Z]/.test(password),
      hasLowercase: /[a-z]/.test(password),
      hasDigits: /\d/.test(password),
      hasSymbols: /[^A-Za-z0-9]/.test(password),
      hasCommonWords: checkCommonWords(password),
      hasKeyboardPatterns: checkKeyboardPatterns(password),
    };

    const score = calculateScore(features);
    const strength = getStrengthLevel(score);
    const suggestions = generateSuggestions(features);
    const entropy = calculateEntropy(password);

    setAnalysis({
      strength,
      score,
      entropy,
      suggestions,
      features,
    });
  };

  const calculateScore = (features: any) => {
    let score = 0;
    if (features.length >= 8) score += 20;
    if (features.length >= 12) score += 10;
    if (features.hasUppercase) score += 15;
    if (features.hasLowercase) score += 15;
    if (features.hasDigits) score += 15;
    if (features.hasSymbols) score += 20;
    if (!features.hasCommonWords) score += 15;
    if (!features.hasKeyboardPatterns) score += 10;
    return Math.min(score, 100);
  };

  const getStrengthLevel = (score: number): 'weak' | 'moderate' | 'strong' => {
    if (score < 40) return 'weak';
    if (score < 70) return 'moderate';
    return 'strong';
  };

  const generateSuggestions = (features: any) => {
    const suggestions = [];
    if (features.length < 8) suggestions.push('Use at least 8 characters');
    if (!features.hasUppercase) suggestions.push('Add uppercase letters');
    if (!features.hasLowercase) suggestions.push('Add lowercase letters');
    if (!features.hasDigits) suggestions.push('Include numbers');
    if (!features.hasSymbols) suggestions.push('Add special characters (!@#$%^&*)');
    if (features.hasCommonWords) suggestions.push('Avoid common words');
    if (features.hasKeyboardPatterns) suggestions.push('Avoid keyboard patterns (qwerty, 123)');
    return suggestions;
  };

  const checkCommonWords = (password: string) => {
    const commonWords = ['password', '123456', 'qwerty', 'admin', 'login', 'welcome'];
    return commonWords.some(word => password.toLowerCase().includes(word));
  };

  const checkKeyboardPatterns = (password: string) => {
    const patterns = ['qwerty', 'asdf', '1234', 'abcd'];
    return patterns.some(pattern => password.toLowerCase().includes(pattern));
  };

  const calculateEntropy = (password: string) => {
    const charset = getCharsetSize(password);
    return Math.log2(Math.pow(charset, password.length));
  };

  const getCharsetSize = (password: string) => {
    let size = 0;
    if (/[a-z]/.test(password)) size += 26;
    if (/[A-Z]/.test(password)) size += 26;
    if (/\d/.test(password)) size += 10;
    if (/[^A-Za-z0-9]/.test(password)) size += 32;
    return size;
  };

  const submitToBackend = async () => {
    if (!password) {
      toast({
        title: "Error",
        description: "Please enter a password to analyze",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      // In a real implementation, replace with your Flask backend URL
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      if (response.ok) {
        const backendAnalysis = await response.json();
        setAnalysis(backendAnalysis);
        toast({
          title: "Analysis Complete",
          description: "Password analyzed successfully",
        });
      } else {
        throw new Error('Backend analysis failed');
      }
    } catch (error) {
      console.error('Backend analysis error:', error);
      toast({
        title: "Analysis Failed",
        description: "Using local analysis instead",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen transition-all duration-500 ${isDarkMode ? 'dark bg-gray-900' : 'bg-gradient-to-br from-blue-50 via-white to-green-50'}`}>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="flex items-center justify-center mb-6">
            <div className="p-3 rounded-full bg-gradient-to-r from-blue-500 to-green-500 mr-4">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h1 className={`text-4xl font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent ${isDarkMode ? 'text-white' : ''}`}>
              Password Strength Analyzer
            </h1>
          </div>
          <p className={`text-lg ${isDarkMode ? 'text-gray-300' : 'text-gray-600'} max-w-2xl mx-auto`}>
            Analyze your password security in real-time with comprehensive feedback and suggestions
          </p>
          <DarkModeToggle isDarkMode={isDarkMode} setIsDarkMode={setIsDarkMode} />
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column - Input and Strength */}
            <div className="space-y-6">
              <div className={`p-6 rounded-2xl shadow-xl backdrop-blur-sm border transition-all duration-300 hover:shadow-2xl ${
                isDarkMode 
                  ? 'bg-gray-800/50 border-gray-700' 
                  : 'bg-white/80 border-white/20'
              }`}>
                <div className="flex items-center mb-4">
                  <Lock className={`w-5 h-5 mr-2 ${isDarkMode ? 'text-blue-400' : 'text-blue-600'}`} />
                  <h2 className={`text-xl font-semibold ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                    Enter Password
                  </h2>
                </div>
                <PasswordInput 
                  password={password} 
                  setPassword={setPassword}
                  isDarkMode={isDarkMode}
                />
              </div>

              {password && analysis && (
                <div className={`p-6 rounded-2xl shadow-xl backdrop-blur-sm border transition-all duration-300 hover:shadow-2xl animate-fade-in ${
                  isDarkMode 
                    ? 'bg-gray-800/50 border-gray-700' 
                    : 'bg-white/80 border-white/20'
                }`}>
                  <StrengthMeter 
                    strength={analysis.strength}
                    score={analysis.score}
                    isDarkMode={isDarkMode}
                  />
                </div>
              )}

              {/* Submit Button */}
              <button
                onClick={submitToBackend}
                disabled={!password || isLoading}
                className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 ${
                  isLoading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600 shadow-lg hover:shadow-xl'
                }`}
              >
                {isLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                    Analyzing with Backend...
                  </div>
                ) : (
                  'Analyze with Backend'
                )}
              </button>
            </div>

            {/* Right Column - Analysis Results */}
            <div className="space-y-6">
              {password && analysis && (
                <>
                  <div className={`p-6 rounded-2xl shadow-xl backdrop-blur-sm border transition-all duration-300 hover:shadow-2xl animate-fade-in ${
                    isDarkMode 
                      ? 'bg-gray-800/50 border-gray-700' 
                      : 'bg-white/80 border-white/20'
                  }`}>
                    <FeatureBreakdown 
                      features={analysis.features}
                      entropy={analysis.entropy}
                      isDarkMode={isDarkMode}
                    />
                  </div>

                  <div className={`p-6 rounded-2xl shadow-xl backdrop-blur-sm border transition-all duration-300 hover:shadow-2xl animate-fade-in ${
                    isDarkMode 
                      ? 'bg-gray-800/50 border-gray-700' 
                      : 'bg-white/80 border-white/20'
                  }`}>
                    <Suggestions 
                      suggestions={analysis.suggestions}
                      isDarkMode={isDarkMode}
                    />
                  </div>
                </>
              )}

              {!password && (
                <div className={`p-8 rounded-2xl border-2 border-dashed text-center transition-all duration-300 ${
                  isDarkMode 
                    ? 'border-gray-600 text-gray-400' 
                    : 'border-gray-300 text-gray-500'
                }`}>
                  <Shield className={`w-16 h-16 mx-auto mb-4 ${isDarkMode ? 'text-gray-600' : 'text-gray-400'}`} />
                  <p className="text-lg">Enter a password to see detailed analysis</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
