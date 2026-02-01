import { useState, useEffect, useCallback } from 'react';
import { getSubjectStats, getAllSubjects } from '@/data/gateData';

interface SubjectProgress {
  attempted: number;
  correct: number;
  total: number;
  percentage: number;
  accuracy: number;
}

interface ProgressData {
  subjects: { [subject: string]: SubjectProgress };
  overall: {
    totalAttempted: number;
    totalCorrect: number;
    totalQuestions: number;
    percentage: number;
    accuracy: number;
  };
  lastStudyDate: string | null;
  studyStreak: number;
}

const STORAGE_KEY = 'gate_study_progress';

/**
 * Hook for managing and persisting study progress
 * Based on cognitive research for learning optimization
 */
export const useProgress = () => {
  const [progress, setProgress] = useState<ProgressData>(() => {
    // Initialize from localStorage
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error('Failed to parse progress data:', e);
      }
    }
    
    // Default state
    const stats = getSubjectStats();
    const subjects: { [subject: string]: SubjectProgress } = {};
    let totalQuestions = 0;
    
    getAllSubjects().forEach(subject => {
      const subjectStat = stats[subject] || { total: 0 };
      totalQuestions += subjectStat.total;
      subjects[subject] = {
        attempted: 0,
        correct: 0,
        total: subjectStat.total,
        percentage: 0,
        accuracy: 0,
      };
    });
    
    return {
      subjects,
      overall: {
        totalAttempted: 0,
        totalCorrect: 0,
        totalQuestions,
        percentage: 0,
        accuracy: 0,
      },
      lastStudyDate: null,
      studyStreak: 0,
    };
  });

  // Save to localStorage whenever progress changes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  // Update study streak on load
  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    
    if (progress.lastStudyDate === today) {
      // Already studied today, no change
      return;
    }
    
    if (progress.lastStudyDate === yesterday) {
      // Studied yesterday, increment streak
      setProgress(prev => ({
        ...prev,
        lastStudyDate: today,
        studyStreak: prev.studyStreak + 1,
      }));
    } else if (progress.lastStudyDate !== today) {
      // Streak broken or first time
      setProgress(prev => ({
        ...prev,
        lastStudyDate: today,
        studyStreak: prev.lastStudyDate ? 1 : 0,
      }));
    }
  }, []);

  const recordAttempt = useCallback((subject: string, isCorrect: boolean) => {
    const today = new Date().toISOString().split('T')[0];
    
    setProgress(prev => {
      const subjectProgress = prev.subjects[subject] || {
        attempted: 0,
        correct: 0,
        total: 0,
        percentage: 0,
        accuracy: 0,
      };
      
      const newAttempted = subjectProgress.attempted + 1;
      const newCorrect = isCorrect ? subjectProgress.correct + 1 : subjectProgress.correct;
      
      const newSubjectProgress = {
        ...subjectProgress,
        attempted: newAttempted,
        correct: newCorrect,
        percentage: subjectProgress.total > 0 
          ? (newAttempted / subjectProgress.total) * 100 
          : 0,
        accuracy: newAttempted > 0 
          ? (newCorrect / newAttempted) * 100 
          : 0,
      };
      
      const newOverallAttempted = prev.overall.totalAttempted + 1;
      const newOverallCorrect = isCorrect 
        ? prev.overall.totalCorrect + 1 
        : prev.overall.totalCorrect;
      
      return {
        ...prev,
        subjects: {
          ...prev.subjects,
          [subject]: newSubjectProgress,
        },
        overall: {
          ...prev.overall,
          totalAttempted: newOverallAttempted,
          totalCorrect: newOverallCorrect,
          percentage: prev.overall.totalQuestions > 0 
            ? (newOverallAttempted / prev.overall.totalQuestions) * 100 
            : 0,
          accuracy: newOverallAttempted > 0 
            ? (newOverallCorrect / newOverallAttempted) * 100 
            : 0,
        },
        lastStudyDate: today,
      };
    });
  }, []);

  const getSubjectProgress = useCallback((subject: string): SubjectProgress => {
    return progress.subjects[subject] || {
      attempted: 0,
      correct: 0,
      total: 0,
      percentage: 0,
      accuracy: 0,
    };
  }, [progress.subjects]);

  const resetProgress = useCallback(() => {
    const stats = getSubjectStats();
    const subjects: { [subject: string]: SubjectProgress } = {};
    let totalQuestions = 0;
    
    getAllSubjects().forEach(subject => {
      const subjectStat = stats[subject] || { total: 0 };
      totalQuestions += subjectStat.total;
      subjects[subject] = {
        attempted: 0,
        correct: 0,
        total: subjectStat.total,
        percentage: 0,
        accuracy: 0,
      };
    });
    
    setProgress({
      subjects,
      overall: {
        totalAttempted: 0,
        totalCorrect: 0,
        totalQuestions,
        percentage: 0,
        accuracy: 0,
      },
      lastStudyDate: null,
      studyStreak: 0,
    });
  }, []);

  return {
    progress,
    recordAttempt,
    getSubjectProgress,
    resetProgress,
  };
};
