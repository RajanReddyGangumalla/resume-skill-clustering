import React from 'react';
import { BarChart3, Users } from 'lucide-react';
import { motion } from 'framer-motion';
import { ClusterDistribution } from '../types';

interface ClusterVisualizationProps {
  data: ClusterDistribution[];
}

const ClusterVisualization: React.FC<ClusterVisualizationProps> = ({ data }) => {
  const maxCount = Math.max(...data.map(d => d.count));
  const colors = [
    'bg-blue-500',
    'bg-purple-500',
    'bg-green-500',
    'bg-yellow-500',
    'bg-red-500',
    'bg-indigo-500',
    'bg-pink-500',
    'bg-teal-500',
    'bg-orange-500',
    'bg-cyan-500',
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-5 h-5 text-purple-400" />
          <span className="text-sm text-gray-400">
            Total Students: {data.reduce((sum, d) => sum + d.count, 0).toLocaleString()}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {data.sort((a, b) => b.count - a.count).map((cluster, index) => {
          const percentage = (cluster.count / maxCount) * 100;
          const colorClass = colors[index % colors.length];
          
          return (
            <motion.div
              key={cluster.cluster_id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className="group"
            >
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <div className={`w-3 h-3 rounded-full ${colorClass}`} />
                      <span className="text-sm font-medium text-white">
                        {cluster.cluster_name}
                      </span>
                      <span className="text-xs text-gray-400">
                        (Cluster {cluster.cluster_id})
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Users className="w-4 h-4 text-gray-400" />
                      <span className="text-sm font-semibold text-white">
                        {cluster.count.toLocaleString()}
                      </span>
                    </div>
                  </div>
                  
                  <div className="relative h-6 bg-slate-700/50 rounded-full overflow-hidden group-hover:bg-slate-700/70 transition-colors duration-200">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${percentage}%` }}
                      transition={{ delay: index * 0.05 + 0.2, duration: 0.5 }}
                      className={`absolute inset-y-0 left-0 ${colorClass} rounded-full opacity-80 group-hover:opacity-100 transition-opacity duration-200`}
                    />
                    <div className="absolute inset-0 flex items-center justify-end pr-3">
                      <span className="text-xs text-white font-medium drop-shadow-lg">
                        {((cluster.count / data.reduce((sum, d) => sum + d.count, 0)) * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="mt-6 p-4 bg-slate-700/30 rounded-lg border border-purple-500/20">
        <h4 className="text-sm font-medium text-purple-400 mb-2">Cluster Insights:</h4>
        <div className="text-xs text-gray-400 space-y-1">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full" />
            <span>Largest cluster: {data[0]?.cluster_name} ({data[0]?.count} students)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full" />
            <span>Total clusters identified: {data.length}</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full" />
            <span>Average cluster size: {Math.round(data.reduce((sum, d) => sum + d.count, 0) / data.length)} students</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClusterVisualization;
