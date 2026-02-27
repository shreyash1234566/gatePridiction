import { useMemo } from 'react';
import { 
  Prediction, 
  getSortedPredictions, 
  getCorePredictions, 
  getPredictionsBySubject,
  GATE_DATA 
} from '@/data/gateData';

interface UsePredictionsOptions {
  subject?: string;
  onlyCore?: boolean;
  minConfidence?: number;
  trend?: 'Rising' | 'Stable' | 'Declining';
}

interface UsePredictionsReturn {
  predictions: Prediction[];
  corePredictions: Prediction[];
  risingTopics: Prediction[];
  decliningTopics: Prediction[];
  highConfidenceTopics: Prediction[];
  subjectDistribution: { [subject: string]: number };
  modelMetrics: {
    MAE: number;
    RMSE: number;
    R2: number;
    Mean_Prediction: number;
  };
}

/**
 * Hook for accessing and filtering 2027 predictions
 * Provides trend analysis and confidence-based recommendations
 */
export const usePredictions = (options: UsePredictionsOptions = {}): UsePredictionsReturn => {
  const { subject, onlyCore, minConfidence, trend } = options;

  const predictions = useMemo(() => {
    let filtered = getSortedPredictions('confidence');
    
    // Filter by subject
    if (subject) {
      filtered = getPredictionsBySubject(subject);
    }
    
    // Filter by core status
    if (onlyCore) {
      filtered = filtered.filter(p => p.is_core === "✓");
    }
    
    // Filter by minimum confidence
    if (minConfidence !== undefined) {
      filtered = filtered.filter(p => p.confidence >= minConfidence);
    }
    
    // Filter by trend
    if (trend) {
      filtered = filtered.filter(p => p.trend === trend);
    }
    
    return filtered;
  }, [subject, onlyCore, minConfidence, trend]);

  const corePredictions = useMemo(() => getCorePredictions(), []);

  const risingTopics = useMemo(() => {
    return getSortedPredictions('confidence').filter(p => p.trend === 'Rising');
  }, []);

  const decliningTopics = useMemo(() => {
    return getSortedPredictions('confidence').filter(p => p.trend === 'Declining');
  }, []);

  const highConfidenceTopics = useMemo(() => {
    return getSortedPredictions('confidence').filter(p => p.confidence >= 82);
  }, []);

  const subjectDistribution = useMemo(() => {
    return GATE_DATA.predictions_2027.subject_distribution;
  }, []);

  const modelMetrics = useMemo(() => {
    return GATE_DATA.predictions_2027.meta.metrics;
  }, []);

  return {
    predictions,
    corePredictions,
    risingTopics,
    decliningTopics,
    highConfidenceTopics,
    subjectDistribution,
    modelMetrics,
  };
};
