// GATE 2026 Comprehensive Website Data
// Type definitions and exports for TypeScript

export interface Question {
  id: number;
  year: number;
  paper_id: string;
  subject: string;
  topic: string;
  question_text: string;
  question_type: "MCQ" | "NAT" | "MSQ";
  choices?: string[];
  answer: string;
  marks: number;
  negative_marks: number;
}

export interface Prediction {
  subject: string;
  topic: string;
  predicted_count: number;
  confidence: number;
  raw_confidence: number;
  uncertainty: number;
  trend: "Rising" | "Stable" | "Declining";
  historical_avg: number;
  recent_avg: number;
  last_seen: number;
  appearances: number;
  is_core: string;
}

export interface TrendData {
  [year: string]: number;
}

export interface SubjectTrends {
  [topic: string]: TrendData;
}

export interface GateDataMeta {
  generated_at: string;
  version: string;
  description: string;
  total_questions: number;
  years_covered: number[];
  subjects: string[];
  target_year: number;
}

export interface SubjectQuestions {
  [topic: string]: Question[];
}

export interface GateData {
  meta: GateDataMeta;
  predictions_2026: {
    meta: {
      version: string;
      generated_at: string;
      total_analyzed: number;
      features: number;
      models: number;
      metrics: {
        MAE: number;
        RMSE: number;
        R2: number;
        Mean_Prediction: number;
      };
    };
    subject_distribution: { [subject: string]: number };
    predictions: Prediction[];
  };
  trends: {
    [subject: string]: SubjectTrends;
  };
  questions: {
    all: Question[];
    by_subject: {
      [subject: string]: SubjectQuestions;
    };
  };
}

// Import the raw data
import { GATE_DATA as RAW_DATA } from './rawData';

// Cast and export with proper typing
export const GATE_DATA = RAW_DATA as unknown as GateData;

// Helper function to get all questions as flat array
export const getAllQuestions = (): Question[] => {
  return GATE_DATA.questions.all;
};

// Helper to get questions by subject
export const getQuestionsBySubject = (subject: string): Question[] => {
  const subjectData = GATE_DATA.questions.by_subject[subject];
  if (!subjectData) return [];
  
  const questions: Question[] = [];
  Object.values(subjectData).forEach((topicQuestions) => {
    questions.push(...topicQuestions);
  });
  
  return questions;
};

// Helper to get questions by subject and topic
export const getQuestionsByTopic = (subject: string, topic: string): Question[] => {
  const subjectData = GATE_DATA.questions.by_subject[subject];
  if (!subjectData) return [];
  return subjectData[topic] || [];
};

// Helper to get unique topics for a subject
export const getTopicsForSubject = (subject: string): string[] => {
  const subjectData = GATE_DATA.questions.by_subject[subject];
  return subjectData ? Object.keys(subjectData) : [];
};

// Helper to get predictions sorted by confidence
export const getSortedPredictions = (sortBy: 'confidence' | 'trend' = 'confidence'): Prediction[] => {
  const predictions = [...GATE_DATA.predictions_2026.predictions];
  
  if (sortBy === 'confidence') {
    return predictions.sort((a, b) => b.confidence - a.confidence);
  }
  
  return predictions.sort((a, b) => {
    const trendOrder = { Rising: 0, Stable: 1, Declining: 2 };
    return trendOrder[a.trend] - trendOrder[b.trend];
  });
};

// Get core topics (marked as essential)
export const getCorePredictions = (): Prediction[] => {
  return GATE_DATA.predictions_2026.predictions.filter(p => p.is_core === "✓");
};

// Get predictions by subject
export const getPredictionsBySubject = (subject: string): Prediction[] => {
  return GATE_DATA.predictions_2026.predictions.filter(p => p.subject === subject);
};

// Get subject statistics
export const getSubjectStats = () => {
  const stats: { [subject: string]: { total: number; topics: number } } = {};
  
  Object.entries(GATE_DATA.questions.by_subject).forEach(([subject, topics]) => {
    const topicCount = Object.keys(topics).length;
    const totalQuestions = Object.values(topics).reduce((sum, questions) => sum + questions.length, 0);
    stats[subject] = { total: totalQuestions, topics: topicCount };
  });
  
  return stats;
};

// Get subject icon mapping
export const subjectIcons: { [key: string]: string } = {
  "Engineering Mathematics": "📐",
  "Digital Logic": "🔌",
  "Computer Organization": "🖥️",
  "Programming": "💻",
  "Data Structures": "🏗️",
  "Algorithms": "⚙️",
  "Theory of Computation": "🧮",
  "Compiler Design": "🔧",
  "Operating Systems": "🖧",
  "Databases": "🗃️",
  "Computer Networks": "🌐",
  "General Aptitude": "🧠",
};

// Subject color mapping for charts (Okabe-Ito color-blind friendly)
export const subjectColors: { [key: string]: string } = {
  "Engineering Mathematics": "hsl(38, 70%, 55%)",
  "Digital Logic": "hsl(200, 70%, 50%)",
  "Computer Organization": "hsl(142, 50%, 45%)",
  "Programming": "hsl(280, 60%, 60%)",
  "Data Structures": "hsl(24, 70%, 55%)",
  "Algorithms": "hsl(340, 65%, 55%)",
  "Theory of Computation": "hsl(180, 50%, 45%)",
  "Compiler Design": "hsl(60, 60%, 50%)",
  "Operating Systems": "hsl(220, 60%, 55%)",
  "Databases": "hsl(300, 50%, 55%)",
  "Computer Networks": "hsl(160, 55%, 45%)",
  "General Aptitude": "hsl(0, 0%, 60%)",
};

// Get years covered
export const getYearsCovered = (): number[] => {
  return GATE_DATA.meta.years_covered;
};

// Get all subjects
export const getAllSubjects = (): string[] => {
  return GATE_DATA.meta.subjects;
};
