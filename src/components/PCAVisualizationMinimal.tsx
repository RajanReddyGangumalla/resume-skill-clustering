import React, { useState, useEffect } from 'react';
import { MapPin } from 'lucide-react';
import { motion } from 'framer-motion';
import { getPCAVisualizationWithUser } from '../services/api';

interface PCAVisualizationProps {
  userText: string;
  isActive: boolean;
}

const PCAVisualizationMinimal: React.FC<PCAVisualizationProps> = ({ userText, isActive }) => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('PCA Visualization useEffect called:', { isActive, userText });
    if (isActive && userText) {
      loadVisualizationData();
    }
  }, [isActive, userText]);

  const loadVisualizationData = async () => {
    console.log('Loading PCA visualization data...');
    setLoading(true);
    setError(null);
    try {
      const response = await getPCAVisualizationWithUser(userText);
      console.log('PCA API Response:', response);
      setData(response.data);
    } catch (err) {
      console.error('PCA visualization error:', err);
      setError('Failed to load visualization data');
    } finally {
      setLoading(false);
    }
  };

  if (!isActive) {
    console.log('PCA Visualization not active');
    return null;
  }

  if (loading) {
    console.log('PCA Visualization loading...');
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-white">Loading PCA visualization...</div>
      </div>
    );
  }

  if (error) {
    console.log('PCA Visualization error:', error);
    return (
      <div className="text-center py-12 text-red-400">
        <p>{error}</p>
      </div>
    );
  }

  console.log('PCA Visualization data length:', data.length);

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-white flex items-center">
        <MapPin className="w-6 h-6 mr-2 text-purple-400" />
        PCA Visualization (Minimal Version)
      </h3>
      
      <div className="bg-slate-800/30 rounded-lg border border-purple-500/20 p-6">
        <p className="text-white mb-4">Data points loaded: {data.length}</p>
        
        {data.length > 0 && (
          <div className="space-y-2">
            <p className="text-green-400">✅ Data loaded successfully!</p>
            <p className="text-sm text-gray-300">
              User point found: {data.find(p => p.is_user) ? 'Yes' : 'No'}
            </p>
            <p className="text-sm text-gray-300">
              Total clusters: {new Set(data.map(p => p.cluster_id)).size}
            </p>
            
            {data.find(p => p.is_user) && (
              <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                <p className="text-green-400 text-sm">
                  🎯 You are in cluster: {data.find(p => p.is_user)?.cluster_name}
                </p>
                <p className="text-green-300 text-xs mt-1">
                  Coordinates: ({data.find(p => p.is_user)?.x.toFixed(3)}, {data.find(p => p.is_user)?.y.toFixed(3)})
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PCAVisualizationMinimal;
