import React, { useState, useEffect } from 'react';
import { MapPin, Users, TrendingUp, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';
import { getPCAVisualizationWithUser } from '../services/api';
import { VisualizationPoint } from '../types';

interface PCAVisualizationProps {
  userText: string;
  isActive: boolean;
}

const PCAVisualizationGraph: React.FC<PCAVisualizationProps> = ({ userText, isActive }) => {
  const [data, setData] = useState<VisualizationPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [hoveredPoint, setHoveredPoint] = useState<VisualizationPoint | null>(null);

  const colors = [
    '#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444',
    '#06b6d4', '#ec4899', '#84cc16', '#f97316', '#6366f1',
    '#14b8a6', '#a855f7', '#22c55e', '#eab308', '#dc2626'
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

  const handleZoomIn = () => setZoom(prev => Math.min(prev * 1.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev / 1.2, 0.5));
  const handleReset = () => setZoom(1);

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

  // Group cluster points by cluster
  const clusterGroups = clusterPoints.reduce((groups, point) => {
    if (!groups[point.cluster_id]) {
      groups[point.cluster_id] = [];
    }
    groups[point.cluster_id].push(point);
    return groups;
  }, {} as Record<number, VisualizationPoint[]>);

  // Calculate bounds for proper scaling with padding
  const allPoints = [...clusterPoints, ...(userPoint ? [userPoint] : [])];
  const xValues = allPoints.map(p => p.x);
  const yValues = allPoints.map(p => p.y);
  const xMin = Math.min(...xValues);
  const xMax = Math.max(...xValues);
  const yMin = Math.min(...yValues);
  const yMax = Math.max(...yValues);
  
  // Add 20% padding on all sides
  const xPadding = (xMax - xMin) * 0.2;
  const yPadding = (yMax - yMin) * 0.2;
  
  const xRange = xMax - xMin + 2 * xPadding;
  const yRange = yMax - yMin + 2 * yPadding;
  const xMinView = xMin - xPadding;
  const yMinView = yMin - yPadding;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white flex items-center">
          <MapPin className="w-6 h-6 mr-2 text-purple-400" />
          PCA Skill Space Visualization
        </h3>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-4 text-sm text-gray-400">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-red-500 rounded-full" />
              <span>You</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-blue-500 rounded-full" />
              <span>Students</span>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleZoomOut}
              className="p-1 text-gray-400 hover:text-white transition-colors"
              title="Zoom out"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <button
              onClick={handleReset}
              className="p-1 text-gray-400 hover:text-white transition-colors"
              title="Reset zoom"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={handleZoomIn}
              className="p-1 text-gray-400 hover:text-white transition-colors"
              title="Zoom in"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="bg-slate-800/30 rounded-lg border border-purple-500/20 p-4"
      >
        <div className="relative w-full h-96 bg-slate-900/90 rounded-lg border border-purple-500/30 overflow-hidden shadow-2xl">
          <svg 
            className="w-full h-full cursor-move" 
            viewBox={`${xMinView} ${yMinView} ${xRange} ${yRange}`}
            style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }}
          >
            {/* Background */}
            <rect x={xMinView} y={yMinView} width={xRange} height={yRange} fill="#0f172a" />

            {/* Grid lines */}
            {Array.from({ length: 10 }, (_, i) => {
              const x = xMinView + (i * xRange / 9);
              const y = yMinView + (i * yRange / 9);
              return (
                <g key={`grid-${i}`}>
                  <line
                    x1={x} y1={yMinView} x2={x} y2={yMinView + yRange}
                    stroke="#334155" strokeWidth="0.02" opacity="0.5"
                  />
                  <line
                    x1={xMinView} y1={y} x2={xMinView + xRange} y2={y}
                    stroke="#334155" strokeWidth="0.02" opacity="0.5"
                  />
                </g>
              );
            })}

            {/* Main axes */}
            <line x1={xMinView} y1={0} x2={xMinView + xRange} y2={0} stroke="#64748b" strokeWidth="0.04" />
            <line x1={0} y1={yMinView} x2={0} y2={yMinView + yRange} stroke="#64748b" strokeWidth="0.04" />
            
            {/* Cluster points with actual graph visualization */}
            {Object.entries(clusterGroups).map(([clusterId, points]) => {
              const color = colors[parseInt(clusterId) % colors.length];
              return points.map((point, index) => (
                <g key={`${clusterId}-${index}`}>
                  <circle
                    cx={point.x}
                    cy={point.y}
                    r={hoveredPoint === point ? "0.08" : "0.04"}
                    fill={color}
                    opacity="0.8"
                    stroke="white"
                    strokeWidth="0.01"
                    className="hover:opacity-100 transition-all cursor-pointer"
                    onMouseEnter={() => setHoveredPoint(point)}
                    onMouseLeave={() => setHoveredPoint(null)}
                  />
                  {hoveredPoint === point && (
                    <text
                      x={point.x}
                      y={point.y - 0.06}
                      fill="white"
                      fontSize="0.06"
                      textAnchor="middle"
                      className="font-semibold pointer-events-none"
                    >
                      {point.cluster_name}
                    </text>
                  )}
                </g>
              ));
            })}
            
            {/* User point - highlighted with pulsing effect */}
            {userPoint && (
              <g>
                {/* Outer glow effect */}
                <circle
                  cx={userPoint.x}
                  cy={userPoint.y}
                  r="0.15"
                  fill="#ef4444"
                  opacity="0.3"
                  className="animate-pulse"
                />
                {/* Middle circle */}
                <circle
                  cx={userPoint.x}
                  cy={userPoint.y}
                  r="0.12"
                  fill="#ef4444"
                  opacity="0.6"
                  className="animate-pulse"
                />
                {/* Main user point */}
                <circle
                  cx={userPoint.x}
                  cy={userPoint.y}
                  r="0.08"
                  fill="#ef4444"
                  stroke="white"
                  strokeWidth="0.03"
                  className="animate-pulse"
                />
                {/* Star shape in center */}
                <path
                  d={`M ${userPoint.x} ${userPoint.y - 0.04} L ${userPoint.x + 0.01} ${userPoint.y - 0.01} L ${userPoint.x + 0.04} ${userPoint.y} L ${userPoint.x + 0.01} ${userPoint.y + 0.01} L ${userPoint.x} ${userPoint.y + 0.04} L ${userPoint.x - 0.01} ${userPoint.y + 0.01} L ${userPoint.x - 0.04} ${userPoint.y} L ${userPoint.x - 0.01} ${userPoint.y - 0.01} Z`}
                  fill="white"
                  opacity="0.9"
                />
                <text
                  x={userPoint.x}
                  y={userPoint.y - 0.18}
                  fill="white"
                  fontSize="0.08"
                  textAnchor="middle"
                  className="font-bold"
                >
                  YOU
                </text>
                <text
                  x={userPoint.x}
                  y={userPoint.y - 0.24}
                  fill="#ef4444"
                  fontSize="0.06"
                  textAnchor="middle"
                  className="font-semibold"
                >
                  {userPoint.cluster_name}
                </text>
              </g>
            )}
            
            {/* Axis labels */}
            <text x={xMinView + xRange - 0.2} y="0.1" fill="#e2e8f0" fontSize="0.12" textAnchor="end" fontWeight="bold">
              PC1
            </text>
            <text x="0.1" y={yMinView + 0.3} fill="#e2e8f0" fontSize="0.12" fontWeight="bold">
              PC2
            </text>
          </svg>

          {/* Hover tooltip */}
          {hoveredPoint && !hoveredPoint.is_user && (
            <div className="absolute top-4 right-4 bg-slate-800/90 backdrop-blur-sm rounded-lg p-3 border border-purple-500/30 text-sm">
              <p className="text-white font-semibold">{hoveredPoint.cluster_name}</p>
              <p className="text-gray-400 text-xs">Cluster {hoveredPoint.cluster_id}</p>
              <p className="text-gray-300 text-xs mt-1">
                PC1: {hoveredPoint.x.toFixed(3)}, PC2: {hoveredPoint.y.toFixed(3)}
              </p>
            </div>
          )}
        </div>
      </motion.div>

      {/* Cluster Legend */}
      <div className="bg-slate-700/30 rounded-lg p-4 border border-purple-500/20">
        <h4 className="text-sm font-medium text-purple-400 mb-3">Cluster Distribution</h4>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {Object.entries(clusterGroups).map(([clusterId, points]) => {
            const color = colors[parseInt(clusterId) % colors.length];
            const clusterName = points[0].cluster_name;
            return (
              <div key={clusterId} className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full`} style={{ backgroundColor: color }} />
                <span className="text-xs text-gray-300">
                  {clusterName} ({points.length})
                </span>
              </div>
            );
          })}
        </div>
      </div>

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
            <span className="text-purple-400 font-medium">Total Points</span>
          </div>
          <p className="text-gray-300 text-xs">
            {clusterPoints.length} students + 1 user = {data.length} total
          </p>
        </div>
      </div>

      {userPoint && (
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
          <p className="text-green-400 text-sm">
            🎯 You are positioned in the <span className="font-semibold">{userPoint.cluster_name}</span> cluster
            at coordinates ({userPoint.x.toFixed(3)}, {userPoint.y.toFixed(3)})
          </p>
          <p className="text-green-300 text-xs mt-1">
            You are among {clusterGroups[userPoint.cluster_id]?.length || 0} other students with similar skill profiles
          </p>
        </div>
      )}
    </div>
  );
};

export default PCAVisualizationGraph;
