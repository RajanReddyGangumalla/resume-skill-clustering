import React, { useState, useEffect } from 'react';
import { ScatterPlot } from 'react-plotly.js';
import { MapPin, Users, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';
import { getPCAVisualizationWithUser } from '../services/api';
import { VisualizationPoint } from '../types';

interface PCAVisualizationProps {
  userText: string;
  isActive: boolean;
}

const PCAVisualization: React.FC<PCAVisualizationProps> = ({ userText, isActive }) => {
  const [data, setData] = useState<VisualizationPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const colors = [
    '#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444',
    '#06b6d4', '#ec4899', '#84cc16', '#f97316', '#6366f1'
  ];

  useEffect(() => {
    if (isActive && userText) {
      loadVisualizationData();
    }
  }, [isActive, userText]);

  const loadVisualizationData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getPCAVisualizationWithUser(userText);
      setData(response.data);
    } catch (err) {
      setError('Failed to load visualization data');
      console.error('PCA visualization error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isActive) {
    return null;
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        >
          <MapPin className="w-8 h-8 text-purple-400" />
        </motion.div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-400">
        <MapPin className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>{error}</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <MapPin className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No visualization data available</p>
      </div>
    );
  }

  // Separate user and cluster data
  const userPoint = data.find(point => point.is_user);
  const clusterPoints = data.filter(point => !point.is_user);

  // Create traces for each cluster
  const traces: any[] = [];
  
  // Group cluster points by cluster
  const clusterGroups = clusterPoints.reduce((groups, point) => {
    if (!groups[point.cluster_id]) {
      groups[point.cluster_id] = [];
    }
    groups[point.cluster_id].push(point);
    return groups;
  }, {} as Record<number, VisualizationPoint[]>);

  // Add trace for each cluster
  Object.entries(clusterGroups).forEach(([clusterId, points]) => {
    const clusterName = points[0].cluster_name;
    const color = colors[parseInt(clusterId) % colors.length];
    
    traces.push({
      x: points.map(p => p.x),
      y: points.map(p => p.y),
      mode: 'markers',
      type: 'scatter',
      name: clusterName,
      marker: {
        size: 6,
        color: color,
        opacity: 0.7,
        line: {
          color: 'white',
          width: 1
        }
      },
      hovertemplate: `<b>${clusterName}</b><br>` +
                     `PC1: %{x:.3f}<br>` +
                     `PC2: %{y:.3f}<extra></extra>`
    });
  });

  // Add user trace
  if (userPoint) {
    traces.push({
      x: [userPoint.x],
      y: [userPoint.y],
      mode: 'markers',
      type: 'scatter',
      name: `You: ${userPoint.cluster_name}`,
      marker: {
        size: 20,
        color: 'red',
        symbol: 'star',
        line: {
          color: 'white',
          width: 3
        }
      },
      hovertemplate: `<b>You: ${userPoint.cluster_name}</b><br>` +
                     `PC1: %{x:.3f}<br>` +
                     `PC2: %{y:.3f}<extra></extra>`
    });
  }

  const layout = {
    title: {
      text: 'Your Position in the Skill Cluster Map',
      font: {
        size: 16,
        color: '#ffffff',
        family: 'Inter'
      }
    },
    xaxis: {
      title: 'PC1 (Principal Component 1)',
      gridcolor: '#334155',
      zerolinecolor: '#334155',
      color: '#e2e8f0',
      titlefont: { color: '#e2e8f0' }
    },
    yaxis: {
      title: 'PC2 (Principal Component 2)',
      gridcolor: '#334155',
      zerolinecolor: '#334155',
      color: '#e2e8f0',
      titlefont: { color: '#e2e8f0' }
    },
    plot_bgcolor: '#0f172a',
    paper_bgcolor: '#1e293b',
    font: {
      color: '#e2e8f0',
      family: 'Inter'
    },
    legend: {
      x: 1.02,
      y: 1,
      bgcolor: '#1e293b',
      bordercolor: '#334155',
      borderwidth: 1,
      font: {
        color: '#e2e8f0'
      }
    },
    margin: {
      l: 50,
      r: 50,
      t: 50,
      b: 50
    },
    height: 500,
    hovermode: 'closest'
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'select2d', 'lasso2d', 'autoScale2d'],
    toImageButtonOptions: {
      format: 'png',
      filename: 'skill-cluster-map',
      height: 500,
      width: 700,
      scale: 2
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white flex items-center">
          <MapPin className="w-6 h-6 mr-2 text-purple-400" />
          PCA Visualization - Your Position in Skill Space
        </h3>
        <div className="flex items-center space-x-4 text-sm text-gray-400">
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 bg-red-500 rounded-full" />
            <span>You</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-3 h-3 bg-blue-500 rounded-full" />
            <span>Other Students</span>
          </div>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="bg-slate-800/30 rounded-lg border border-purple-500/20 p-4"
      >
        <ScatterPlot
          data={traces}
          layout={layout}
          config={config}
          className="w-full"
        />
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div className="bg-slate-700/30 rounded-lg p-3 border border-purple-500/20">
          <div className="flex items-center space-x-2 mb-1">
            <TrendingUp className="w-4 h-4 text-purple-400" />
            <span className="text-purple-400 font-medium">PC1</span>
          </div>
          <p className="text-gray-300 text-xs">
            First principal component - captures the most variance in the data
          </p>
        </div>
        
        <div className="bg-slate-700/30 rounded-lg p-3 border border-purple-500/20">
          <div className="flex items-center space-x-2 mb-1">
            <TrendingUp className="w-4 h-4 text-purple-400" />
            <span className="text-purple-400 font-medium">PC2</span>
          </div>
          <p className="text-gray-300 text-xs">
            Second principal component - captures the second most variance
          </p>
        </div>
        
        <div className="bg-slate-700/30 rounded-lg p-3 border border-purple-500/20">
          <div className="flex items-center space-x-2 mb-1">
            <Users className="w-4 h-4 text-purple-400" />
            <span className="text-purple-400 font-medium">Clusters</span>
          </div>
          <p className="text-gray-300 text-xs">
            Each color represents a different skill cluster group
          </p>
        </div>
      </div>

      {userPoint && (
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
          <p className="text-green-400 text-sm">
            🎯 You are positioned in the <span className="font-semibold">{userPoint.cluster_name}</span> cluster
            at coordinates ({userPoint.x.toFixed(3)}, {userPoint.y.toFixed(3)})
          </p>
        </div>
      )}
    </div>
  );
};

export default PCAVisualization;
