export interface DatasetInfo {
  n_samples: number;
  n_features: number;
  n_clusters: number;
  best_algorithm: string;
}

export interface ClusterDistribution {
  cluster_id: number;
  cluster_name: string;
  count: number;
}

export interface ClusterResponse {
  cluster_id: number;
  cluster_name: string;
  skills: Record<string, number>;
  similar_students: number;
  total_skills: number;
  pca_coordinates: [number, number];
}

export interface VisualizationPoint {
  x: number;
  y: number;
  cluster_id: number;
  cluster_name: string;
  is_user: boolean;
}

export interface VisualizationData {
  data: VisualizationPoint[];
}
