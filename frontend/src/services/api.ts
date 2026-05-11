import axios from 'axios';
import { DatasetInfo, ClusterDistribution, ClusterResponse, VisualizationData } from '../types';

const API_BASE_URL = 'https://resume-skill-clustering-new.vercel.app';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const getDatasetInfo = async (): Promise<DatasetInfo> => {
  const response = await api.get('/dataset-info');
  return response.data;
};

export const getClusterDistribution = async (): Promise<{ distribution: ClusterDistribution[] }> => {
  const response = await api.get('/cluster-distribution');
  return response.data;
};

export const getVisualizationData = async (): Promise<VisualizationData> => {
  const response = await api.get('/clusters-visualization');
  return response.data;
};

export const getPCAVisualizationWithUser = async (text: string): Promise<VisualizationData> => {
  const response = await api.post('/pca-visualization', { text });
  return response.data;
};

export const analyzeText = async (text: string): Promise<ClusterResponse> => {
  const response = await api.post('/analyze-text', { text });
  return response.data;
};

export const analyzeFile = async (file: File): Promise<ClusterResponse> => {
  console.log('API: analyzeFile called with:', file.name, file.type, file.size);
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await api.post('/analyze-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log('API: Response received:', response.status, response.data);
    return response.data;
  } catch (error) {
    console.error('API: Error in analyzeFile:', error);
    throw error;
  }
};

export const healthCheck = async (): Promise<{ status: string; model_loaded: boolean }> => {
  const response = await api.get('/health');
  return response.data;
};
