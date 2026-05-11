import React, { useState } from 'react';
import { Star, Users, Brain, MapPin, Award, ChevronDown, ChevronUp } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { ClusterResponse } from '../types';
import PCAVisualization from './PCAVisualizationCanvas';

interface ResultsProps {
  results: ClusterResponse;
  userText?: string;
}

const Results: React.FC<ResultsProps> = ({ results, userText }) => {
  const [showAllSkills, setShowAllSkills] = useState(false);
  const [showVisualization, setShowVisualization] = useState(false);
  const [showPCAVisualization, setShowPCAVisualization] = useState(false);

  const topSkills = Object.entries(results.skills)
    .sort(([, a], [, b]) => b - a)
    .slice(0, showAllSkills ? undefined : 10);

  const getSkillLevel = (score: number) => {
    if (score >= 0.8) return { level: 'Expert', color: 'text-green-400' };
    if (score >= 0.6) return { level: 'Advanced', color: 'text-blue-400' };
    if (score >= 0.4) return { level: 'Intermediate', color: 'text-yellow-400' };
    if (score >= 0.2) return { level: 'Beginner', color: 'text-orange-400' };
    return { level: 'Basic', color: 'text-red-400' };
  };

  return (
    <div className="space-y-6">
      {/* Main Results Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-sm rounded-2xl p-8 border border-purple-500/30"
      >
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mb-4">
            <Award className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">
            Your Analysis Results
          </h2>
          <p className="text-gray-300">
            You've been identified as a <span className="font-semibold text-purple-400">{results.cluster_name}</span>
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-slate-800/50 rounded-lg p-4 text-center">
            <div className="flex items-center justify-center mb-2">
              <Star className="w-5 h-5 text-yellow-400 mr-2" />
              <span className="text-sm text-gray-400">Profile</span>
            </div>
            <div className="text-xl font-bold text-white">{results.cluster_name}</div>
            <div className="text-xs text-gray-500">Cluster {results.cluster_id}</div>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-4 text-center">
            <div className="flex items-center justify-center mb-2">
              <Users className="w-5 h-5 text-blue-400 mr-2" />
              <span className="text-sm text-gray-400">Similar Students</span>
            </div>
            <div className="text-xl font-bold text-white">{results.similar_students.toLocaleString()}</div>
            <div className="text-xs text-gray-500">In your cluster</div>
          </div>

          <div className="bg-slate-800/50 rounded-lg p-4 text-center">
            <div className="flex items-center justify-center mb-2">
              <Brain className="w-5 h-5 text-green-400 mr-2" />
              <span className="text-sm text-gray-400">Skills Found</span>
            </div>
            <div className="text-xl font-bold text-white">{results.total_skills}</div>
            <div className="text-xs text-gray-500">Technical skills</div>
          </div>
        </div>

        {/* Success Message */}
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 text-center">
          <p className="text-green-400">
            🎉 Analysis Complete! You're part of a group of {results.similar_students.toLocaleString()} similar students.
          </p>
        </div>
      </motion.div>

      {/* Skills Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20"
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-white flex items-center">
            <Brain className="w-6 h-6 mr-2 text-purple-400" />
            Skills Found in Your Resume
          </h3>
          {Object.keys(results.skills).length > 10 && (
            <button
              onClick={() => setShowAllSkills(!showAllSkills)}
              className="flex items-center space-x-1 text-purple-400 hover:text-purple-300 transition-colors"
            >
              <span className="text-sm">
                {showAllSkills ? 'Show Less' : 'Show All'}
              </span>
              {showAllSkills ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          )}
        </div>

        <div className="space-y-3">
          <AnimatePresence>
            {topSkills.map(([skill, score], index) => {
              const skillLevel = getSkillLevel(score);
              const skillName = skill.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
              
              return (
                <motion.div
                  key={skill}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ delay: index * 0.05 }}
                  className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-purple-500/20 hover:bg-slate-700/50 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-purple-400 rounded-full" />
                    <span className="text-white font-medium">{skillName}</span>
                    <span className={`text-xs ${skillLevel.color}`}>{skillLevel.level}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-24 bg-slate-600/50 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full"
                        style={{ width: `${score * 100}%` }}
                      />
                    </div>
                    <span className="text-sm text-gray-300 w-12 text-right">
                      {(score * 100).toFixed(0)}%
                    </span>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>

        {Object.keys(results.skills).length === 0 && (
          <div className="text-center py-8 text-gray-400">
            <Brain className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No technical skills detected</p>
            <p className="text-sm mt-1">Try adding more specific skill keywords</p>
          </div>
        )}
      </motion.div>

      {/* Position Visualization */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20"
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-white flex items-center">
            <MapPin className="w-6 h-6 mr-2 text-purple-400" />
            Your Position in Skill Space
          </h3>
          <button
            onClick={() => setShowVisualization(!showVisualization)}
            className="flex items-center space-x-1 text-purple-400 hover:text-purple-300 transition-colors"
          >
            <span className="text-sm">
              {showVisualization ? 'Hide Details' : 'Show Details'}
            </span>
            {showVisualization ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>

        <div className="text-center py-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-red-500 to-orange-500 rounded-full mb-4">
            <MapPin className="w-10 h-10 text-white" />
          </div>
          <p className="text-white text-lg font-medium mb-2">
            You are here: {results.cluster_name}
          </p>
          <p className="text-gray-400 text-sm">
            PCA Coordinates: ({results.pca_coordinates[0].toFixed(2)}, {results.pca_coordinates[1].toFixed(2)})
          </p>
        </div>

        <AnimatePresence>
          {showVisualization && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-6 p-4 bg-slate-700/30 rounded-lg border border-purple-500/20"
            >
              <h4 className="text-sm font-medium text-purple-400 mb-3">Technical Details:</h4>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-400">PC1 Coordinate:</span>
                  <span className="text-white ml-2">{results.pca_coordinates[0].toFixed(4)}</span>
                </div>
                <div>
                  <span className="text-gray-400">PC2 Coordinate:</span>
                  <span className="text-white ml-2">{results.pca_coordinates[1].toFixed(4)}</span>
                </div>
                <div>
                  <span className="text-gray-400">Cluster ID:</span>
                  <span className="text-white ml-2">{results.cluster_id}</span>
                </div>
                <div>
                  <span className="text-gray-400">Total Skills:</span>
                  <span className="text-white ml-2">{results.total_skills}</span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* PCA Visualization */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20"
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-white flex items-center">
            <MapPin className="w-6 h-6 mr-2 text-purple-400" />
            PCA Skill Space Visualization
          </h3>
          <button
            onClick={() => setShowPCAVisualization(!showPCAVisualization)}
            className="flex items-center space-x-1 text-purple-400 hover:text-purple-300 transition-colors"
          >
            <span className="text-sm">
              {showPCAVisualization ? 'Hide Visualization' : 'Show Visualization'}
            </span>
            {showPCAVisualization ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>

        <div className="text-center py-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mb-4">
            <MapPin className="w-10 h-10 text-white" />
          </div>
          <p className="text-white text-lg font-medium mb-2">
            Interactive Skill Cluster Map
          </p>
          <p className="text-gray-400 text-sm">
            See your position among all students in the skill space
          </p>
        </div>

        <AnimatePresence>
          {showPCAVisualization && userText && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-6"
            >
              <PCAVisualization 
                userText={userText} 
                isActive={showPCAVisualization} 
              />
            </motion.div>
          )}
        </AnimatePresence>

        {!userText && showPCAVisualization && (
          <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
            <p className="text-yellow-400 text-sm">
              ⚠️ PCA visualization requires the original text data. Please try the analysis again.
            </p>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Results;
