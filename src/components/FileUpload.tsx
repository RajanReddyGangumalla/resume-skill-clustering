import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, AlertCircle, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  loading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, loading }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    disabled: loading
  });

  return (
    <div>
      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200
          ${isDragActive 
            ? 'border-purple-400 bg-purple-500/10' 
            : isDragReject 
              ? 'border-red-400 bg-red-500/10' 
              : 'border-purple-500/30 bg-slate-700/30 hover:border-purple-400 hover:bg-purple-500/5'
          }
          ${loading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          {loading ? (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            >
              <Upload className="w-12 h-12 text-purple-400" />
            </motion.div>
          ) : (
            <Upload className="w-12 h-12 text-purple-400" />
          )}
          
          <div>
            <p className="text-lg font-medium text-white mb-2">
              {loading ? 'Analyzing...' : isDragActive 
                ? 'Drop your resume here' 
                : 'Drop your resume here, or click to browse'
              }
            </p>
            <p className="text-sm text-gray-400">
              Supports TXT and PDF files (max 10MB)
            </p>
          </div>

          {!loading && (
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <File className="w-4 h-4" />
              <span>Resume.pdf</span>
              <span>•</span>
              <span>Resume.txt</span>
            </div>
          )}
        </div>

        {isDragReject && (
          <div className="absolute inset-0 flex items-center justify-center bg-red-500/10 rounded-xl">
            <div className="flex items-center space-x-2 text-red-400">
              <AlertCircle className="w-5 h-5" />
              <span className="font-medium">Invalid file type</span>
            </div>
          </div>
        )}
      </div>

      <div className="mt-4 p-4 bg-slate-700/30 rounded-lg border border-purple-500/20">
        <h4 className="text-sm font-medium text-purple-400 mb-2">File Requirements:</h4>
        <ul className="text-xs text-gray-400 space-y-1">
          <li>• PDF or TXT format</li>
          <li>• Maximum file size: 10MB</li>
          <li>• Contains technical skills and experience</li>
          <li>• English language only</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUpload;
