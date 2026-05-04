import React, { useState } from 'react';
import { Send, FileText, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface TextInputProps {
  onTextSubmit: (text: string) => void;
  loading: boolean;
}

const TextInput: React.FC<TextInputProps> = ({ onTextSubmit, loading }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !loading) {
      onTextSubmit(text);
    }
  };

  const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-purple-400 mb-2">
            Paste Your Resume Text
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Copy and paste your complete resume here. Include your skills, experience, education, and projects..."
            className="w-full h-64 px-4 py-3 bg-slate-700/50 border border-purple-500/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            disabled={loading}
          />
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs text-gray-400">
              {wordCount} words
            </span>
            {wordCount < 50 && text.trim() && (
              <div className="flex items-center space-x-1 text-xs text-yellow-400">
                <AlertCircle className="w-3 h-3" />
                <span>Add more text for better analysis</span>
              </div>
            )}
          </div>
        </div>

        <button
          type="submit"
          disabled={!text.trim() || loading}
          className="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium rounded-lg hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              >
                <FileText className="w-5 h-5" />
              </motion.div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Analyze Resume</span>
            </>
          )}
        </button>
      </form>

      <div className="mt-4 p-4 bg-slate-700/30 rounded-lg border border-purple-500/20">
        <h4 className="text-sm font-medium text-purple-400 mb-2">Tips for best results:</h4>
        <ul className="text-xs text-gray-400 space-y-1">
          <li>• Include technical skills and programming languages</li>
          <li>• Mention tools and frameworks you've used</li>
          <li>• Add project descriptions and technologies</li>
          <li>• Include work experience details</li>
          <li>• Minimum 50 words recommended</li>
        </ul>
      </div>

      {text.trim() && (
        <div className="mt-4 p-4 bg-slate-700/30 rounded-lg border border-purple-500/20">
          <h4 className="text-sm font-medium text-purple-400 mb-2">Preview:</h4>
          <div className="text-xs text-gray-300 max-h-32 overflow-y-auto">
            {text.substring(0, 300)}
            {text.length > 300 && '...'}
          </div>
        </div>
      )}
    </div>
  );
};

export default TextInput;
