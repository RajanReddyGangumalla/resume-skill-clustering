import React from 'react';
import { Users, Brain, TrendingUp, Zap } from 'lucide-react';
import { motion } from 'framer-motion';
import { DatasetInfo } from '../types';

interface DatasetOverviewProps {
  info: DatasetInfo;
}

const DatasetOverview: React.FC<DatasetOverviewProps> = ({ info }) => {
  const metrics = [
    {
      label: 'Students',
      value: info.n_samples.toLocaleString(),
      icon: Users,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      label: 'Skills',
      value: info.n_features.toString(),
      icon: Brain,
      color: 'from-purple-500 to-pink-500'
    },
    {
      label: 'Clusters',
      value: info.n_clusters.toString(),
      icon: TrendingUp,
      color: 'from-green-500 to-emerald-500'
    },
    {
      label: 'Algorithm',
      value: info.best_algorithm.charAt(0).toUpperCase() + info.best_algorithm.slice(1),
      icon: Zap,
      color: 'from-orange-500 to-red-500'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {metrics.map((metric, index) => {
        const Icon = metric.icon;
        return (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-20 rounded-xl transition-opacity duration-300 blur-xl"
                 style={{ backgroundImage: `linear-gradient(to right, var(--tw-gradient-stops))` }}
            />
            <div className="relative bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-purple-500/20 hover:border-purple-400/40 transition-all duration-300">
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg bg-gradient-to-r ${metric.color}`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="text-xs text-gray-400 uppercase tracking-wide">
                  {metric.label}
                </div>
              </div>
              <div className="text-2xl font-bold text-white mb-1">
                {metric.value}
              </div>
              <div className="text-sm text-gray-400">
                {metric.label === 'Students' && 'Total analyzed'}
                {metric.label === 'Skills' && 'Technical skills tracked'}
                {metric.label === 'Clusters' && 'Skill groups identified'}
                {metric.label === 'Algorithm' && 'Clustering method used'}
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

export default DatasetOverview;
