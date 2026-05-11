import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { MapPin, Users, TrendingUp, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';
import { getPCAVisualizationWithUser } from '../services/api';
import { VisualizationPoint } from '../types';

interface PCAVisualizationProps {
  userText: string;
  isActive: boolean;
}

const PCAVisualizationCanvas: React.FC<PCAVisualizationProps> = ({ userText, isActive }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [data, setData] = useState<VisualizationPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [hoveredPoint, setHoveredPoint] = useState<VisualizationPoint | null>(null);

  const colors = useMemo(() => [
    '#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444',
    '#06b6d4', '#ec4899', '#84cc16', '#f97316', '#6366f1',
    '#14b8a6', '#a855f7', '#22c55e', '#eab308', '#dc2626'
  ], []);

  const loadVisualizationData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getPCAVisualizationWithUser(userText);
      console.log('PCA Canvas Data:', response.data);
      setData(response.data);
    } catch (err) {
      setError('Failed to load visualization data');
      console.error('PCA visualization error:', err);
    } finally {
      setLoading(false);
    }
  }, [userText]);

  const drawVisualization = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = 800;
    canvas.height = 400;

    // Clear canvas
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Separate user and cluster data
    const userPoint = data.find(point => point.is_user);
    const clusterPoints = data.filter(point => !point.is_user);

    if (clusterPoints.length === 0) return;

    // Calculate bounds
    const allPoints = [...clusterPoints, ...(userPoint ? [userPoint] : [])];
    const xValues = allPoints.map(p => p.x);
    const yValues = allPoints.map(p => p.y);
    const xMin = Math.min(...xValues);
    const xMax = Math.max(...xValues);
    const yMin = Math.min(...yValues);
    const yMax = Math.max(...yValues);

    // Add padding
    const xPadding = (xMax - xMin) * 0.1;
    const yPadding = (yMax - yMin) * 0.1;

    // Scale functions
    const xScale = (x: number) => ((x - xMin + xPadding) / (xMax - xMin + 2 * xPadding)) * canvas.width;
    const yScale = (y: number) => canvas.height - ((y - yMin + yPadding) / (yMax - yMin + 2 * yPadding)) * canvas.height;

    // Draw grid
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);

    // Vertical grid lines
    for (let i = 0; i <= 10; i++) {
      const x = (canvas.width / 10) * i;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }

    // Horizontal grid lines
    for (let i = 0; i <= 10; i++) {
      const y = (canvas.height / 10) * i;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);

    // Draw axes
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 2;

    // X-axis
    const yZero = yScale(0);
    ctx.beginPath();
    ctx.moveTo(0, yZero);
    ctx.lineTo(canvas.width, yZero);
    ctx.stroke();

    // Y-axis
    const xZero = xScale(0);
    ctx.beginPath();
    ctx.moveTo(xZero, 0);
    ctx.lineTo(xZero, canvas.height);
    ctx.stroke();

    // Draw axis labels
    ctx.fillStyle = '#e2e8f0';
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('PC1', canvas.width - 20, yZero - 10);
    ctx.textAlign = 'left';
    ctx.fillText('PC2', xZero + 10, 20);

    // Group cluster points by cluster
    const clusterGroups = clusterPoints.reduce((groups, point) => {
      if (!groups[point.cluster_id]) {
        groups[point.cluster_id] = [];
      }
      groups[point.cluster_id].push(point);
      return groups;
    }, {} as Record<number, VisualizationPoint[]>);

    // Draw cluster points
    Object.entries(clusterGroups).forEach(([clusterId, points]) => {
      const color = colors[parseInt(clusterId) % colors.length];
      
      points.forEach(point => {
        const x = xScale(point.x);
        const y = yScale(point.y);
        
        // Draw point
        ctx.beginPath();
        ctx.arc(x, y, 6 * zoom, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Highlight on hover
        if (hoveredPoint === point) {
          ctx.beginPath();
          ctx.arc(x, y, 10 * zoom, 0, 2 * Math.PI);
          ctx.fillStyle = color + '40';
          ctx.fill();
          
          // Draw label
          ctx.fillStyle = 'white';
          ctx.font = 'bold 12px Arial';
          ctx.textAlign = 'center';
          ctx.fillText(point.cluster_name, x, y - 15 * zoom);
        }
      });
    });

    // Draw user point with special styling
    if (userPoint) {
      const x = xScale(userPoint.x);
      const y = yScale(userPoint.y);
      
      // Outer glow
      ctx.beginPath();
      ctx.arc(x, y, 20 * zoom, 0, 2 * Math.PI);
      ctx.fillStyle = '#ef444440';
      ctx.fill();
      
      // Middle circle
      ctx.beginPath();
      ctx.arc(x, y, 12 * zoom, 0, 2 * Math.PI);
      ctx.fillStyle = '#ef444480';
      ctx.fill();
      
      // Main user point
      ctx.beginPath();
      ctx.arc(x, y, 8 * zoom, 0, 2 * Math.PI);
      ctx.fillStyle = '#ef4444';
      ctx.fill();
      ctx.strokeStyle = 'white';
      ctx.lineWidth = 3;
      ctx.stroke();
      
      // Draw star in center
      ctx.fillStyle = 'white';
      ctx.font = 'bold 16px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('★', x, y);
      
      // Draw labels
      ctx.fillStyle = 'white';
      ctx.font = 'bold 14px Arial';
      ctx.fillText('YOU', x, y - 25 * zoom);
      
      ctx.fillStyle = '#ef4444';
      ctx.font = '12px Arial';
      ctx.fillText(userPoint.cluster_name, x, y - 40 * zoom);
    }
  }, [data, zoom, hoveredPoint, colors]);

  useEffect(() => {
    if (isActive && userText) {
      loadVisualizationData();
    }
  }, [isActive, userText, loadVisualizationData]);

  useEffect(() => {
    if (data.length > 0 && canvasRef.current) {
      drawVisualization();
    }
  }, [data, zoom, hoveredPoint, drawVisualization]);

  const handleZoomIn = () => setZoom(prev => Math.min(prev * 1.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev / 1.2, 0.5));
  const handleReset = () => setZoom(1);

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Separate user and cluster data
    const userPoint = data.find(point => point.is_user);
    const clusterPoints = data.filter(point => !point.is_user);

    if (clusterPoints.length === 0) return;

    // Calculate bounds
    const allPoints = [...clusterPoints, ...(userPoint ? [userPoint] : [])];
    const xValues = allPoints.map(p => p.x);
    const yValues = allPoints.map(p => p.y);
    const xMin = Math.min(...xValues);
    const xMax = Math.max(...xValues);
    const yMin = Math.min(...yValues);
    const yMax = Math.max(...yValues);

    const xPadding = (xMax - xMin) * 0.1;
    const yPadding = (yMax - yMin) * 0.1;

    const xScale = (xVal: number) => ((xVal - xMin + xPadding) / (xMax - xMin + 2 * xPadding)) * canvas.width;
    const yScale = (yVal: number) => canvas.height - ((yVal - yMin + yPadding) / (yMax - yMin + 2 * yPadding)) * canvas.height;

    // Find clicked point
    let clickedPoint: VisualizationPoint | null = null;
    clusterPoints.forEach(point => {
      const px = xScale(point.x);
      const py = yScale(point.y);
      const distance = Math.sqrt((x - px) ** 2 + (y - py) ** 2);
      if (distance < 10 * zoom) {
        clickedPoint = point;
      }
    });

    setHoveredPoint(clickedPoint);
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

  // Separate user and cluster data for stats
  const userPoint = data.find(point => point.is_user);
  const clusterPoints = data.filter(point => !point.is_user);
  const clusterGroups = clusterPoints.reduce((groups, point) => {
    if (!groups[point.cluster_id]) {
      groups[point.cluster_id] = [];
    }
    groups[point.cluster_id].push(point);
    return groups;
  }, {} as Record<number, VisualizationPoint[]>);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-white flex items-center">
          <MapPin className="w-6 h-6 mr-2 text-purple-400" />
          PCA Skill Space Visualization (Canvas)
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
        <div className="relative w-full bg-slate-900/90 rounded-lg border border-purple-500/30 overflow-hidden shadow-2xl">
          <canvas
            ref={canvasRef}
            width={800}
            height={400}
            className="w-full cursor-pointer"
            onClick={handleCanvasClick}
            style={{ maxHeight: '400px' }}
          />
          
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

export default PCAVisualizationCanvas;
