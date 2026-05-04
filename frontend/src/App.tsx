import React, { useState, useEffect } from 'react';
import { Upload, FileText, BarChart3, Users, Brain, TrendingUp, Star, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { toast } from 'react-hot-toast';
import FileUpload from './components/FileUpload';
import TextInput from './components/TextInput';
import Results from './components/Results';
import DatasetOverview from './components/DatasetOverview';
import ClusterVisualization from './components/ClusterVisualization';
import { analyzeText, analyzeFile, getDatasetInfo, getClusterDistribution } from './services/api';
import { ClusterResponse, DatasetInfo as DatasetInfoType, ClusterDistribution } from './types';

function App() {
  const [activeTab, setActiveTab] = useState<'upload' | 'text'>('upload');
  const [datasetInfo, setDatasetInfo] = useState<DatasetInfoType | null>(null);
  const [clusterDistribution, setClusterDistribution] = useState<ClusterDistribution[]>([]);
  const [results, setResults] = useState<ClusterResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [lastUserText, setLastUserText] = useState<string>('');

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [info, distribution] = await Promise.all([
        getDatasetInfo(),
        getClusterDistribution()
      ]);
      setDatasetInfo(info);
      setClusterDistribution(distribution.distribution);
    } catch (error) {
      toast.error('Failed to load dataset information');
      console.error('Error loading initial data:', error);
    }
  };

  const handleTextAnalysis = async (text: string) => {
    setLoading(true);
    try {
      const result = await analyzeText(text);
      setResults(result);
      setLastUserText(text);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      toast.error('Analysis failed. Please try again.');
      console.error('Text analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileAnalysis = async (file: File) => {
    setLoading(true);
    try {
      console.log('Starting file analysis for:', file.name, file.type);
      const result = await analyzeFile(file);
      console.log('Analysis result:', result);
      setResults(result);
      
      // Extract text from file for PCA visualization
      if (file.type === 'text/plain') {
        const text = await file.text();
        setLastUserText(text);
      }
      
      toast.success('Analysis completed successfully!');
    } catch (error) {
      console.error('File analysis error:', error);
      if (error instanceof Error) {
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
      }
      toast.error('File analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center mb-4">
            <Brain className="w-12 h-12 text-purple-400 mr-3" />
            <h1 className="text-5xl font-bold text-white">
              Resume Skill Clustering
            </h1>
          </div>
          <p className="text-xl text-gray-300">
            Find your skill cluster among students
          </p>
        </motion.div>

        {/* Dataset Overview */}
        {datasetInfo && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-12"
          >
            <DatasetOverview info={datasetInfo} />
          </motion.div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Panel - Input */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-1"
          >
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20">
              <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
                <Upload className="w-6 h-6 mr-2 text-purple-400" />
                Analyze Your Resume
              </h2>

              {/* Tab Navigation */}
              <div className="flex mb-6 bg-slate-700/50 rounded-lg p-1">
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 flex items-center justify-center ${
                    activeTab === 'upload'
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  <FileText className="w-4 h-4 mr-2" />
                  File Upload
                </button>
                <button
                  onClick={() => setActiveTab('text')}
                  className={`flex-1 py-2 px-4 rounded-md transition-all duration-200 flex items-center justify-center ${
                    activeTab === 'text'
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  <FileText className="w-4 h-4 mr-2" />
                  Text Input
                </button>
              </div>

              {/* Content based on active tab */}
              {activeTab === 'upload' ? (
                <FileUpload onFileSelect={handleFileAnalysis} loading={loading} />
              ) : (
                <TextInput onTextSubmit={handleTextAnalysis} loading={loading} />
              )}
            </div>
          </motion.div>

          {/* Right Panel - Results */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-2 space-y-8"
          >
            {/* Cluster Distribution */}
            {clusterDistribution.length > 0 && (
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20">
                <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
                  <BarChart3 className="w-6 h-6 mr-2 text-purple-400" />
                  Cluster Distribution
                </h2>
                <ClusterVisualization data={clusterDistribution} />
              </div>
            )}

            {/* Results */}
            {results && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <Results results={results} userText={lastUserText} />
              </motion.div>
            )}

            {/* Placeholder when no results */}
            {!results && !loading && (
              <div className="bg-slate-800/30 backdrop-blur-sm rounded-2xl p-12 border border-purple-500/20 text-center">
                <Star className="w-16 h-16 text-purple-400 mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-semibold text-white mb-2">
                  Ready to Analyze
                </h3>
                <p className="text-gray-400">
                  Upload your resume or paste your text to get started
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}

export default App;
