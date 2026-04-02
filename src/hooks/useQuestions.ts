import { useState, useEffect, useMemo, useCallback } from 'react';
import { 
  Question, 
  getAllQuestions, 
  getQuestionsBySubject, 
  getQuestionsByTopic,
  getQuestionsByMicroTopic,
  getTopicsForSubject,
  getMicroTopicsForTopic,
  getAllSubjects,
  getYearsCovered
} from '@/data/gateData';

interface UseQuestionsOptions {
  subject?: string;
  topic?: string;
  microTopic?: string;
  year?: number;
  questionType?: 'MCQ' | 'NAT' | 'MSQ';
  shuffle?: boolean;
}

interface UseQuestionsReturn {
  questions: Question[];
  currentIndex: number;
  currentQuestion: Question | null;
  totalQuestions: number;
  isLoading: boolean;
  goToNext: () => void;
  goToPrevious: () => void;
  goToQuestion: (index: number) => void;
  resetQuestions: () => void;
  subjects: string[];
  topics: string[];
  microTopics: string[];
  years: number[];
}

/**
 * Hook for managing question data and navigation
 * Provides filtered questions based on subject, topic, micro-topic, year, and type
 */
export const useQuestions = (options: UseQuestionsOptions = {}): UseQuestionsReturn => {
  const { subject, topic, microTopic, year, questionType, shuffle = false } = options;
  
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  // Get all available subjects and years
  const subjects = useMemo(() => getAllSubjects(), []);
  const years = useMemo(() => getYearsCovered(), []);
  
  // Get topics for selected subject
  const topics = useMemo(() => {
    if (!subject) return [];
    return getTopicsForSubject(subject);
  }, [subject]);

  // Get micro topics for selected topic
  const microTopics = useMemo(() => {
    if (!subject || !topic) return [];
    return getMicroTopicsForTopic(subject, topic);
  }, [subject, topic]);

  // Filter questions based on options
  const questions = useMemo(() => {
    setIsLoading(true);
    
    let filteredQuestions: Question[];
    
    // Start with subject/topic/micro filtering
    if (subject && topic && microTopic) {
      filteredQuestions = getQuestionsByMicroTopic(subject, topic, microTopic);
    } else if (subject && topic) {
      filteredQuestions = getQuestionsByTopic(subject, topic);
    } else if (subject) {
      filteredQuestions = getQuestionsBySubject(subject);
    } else {
      filteredQuestions = getAllQuestions();
    }
    
    // Filter by year
    if (year) {
      filteredQuestions = filteredQuestions.filter(q => q.year === year);
    }
    
    // Filter by question type
    if (questionType) {
      filteredQuestions = filteredQuestions.filter(q => q.question_type === questionType);
    }
    
    // Shuffle if requested
    if (shuffle) {
      filteredQuestions = [...filteredQuestions].sort(() => Math.random() - 0.5);
    }
    
    setIsLoading(false);
    return filteredQuestions;
  }, [subject, topic, microTopic, year, questionType, shuffle]);

  // Current question
  const currentQuestion = useMemo(() => {
    return questions[currentIndex] || null;
  }, [questions, currentIndex]);

  // Reset index when questions change
  useEffect(() => {
    setCurrentIndex(0);
  }, [subject, topic, microTopic, year, questionType]);

  // Navigation functions
  const goToNext = useCallback(() => {
    setCurrentIndex(prev => Math.min(prev + 1, questions.length - 1));
  }, [questions.length]);

  const goToPrevious = useCallback(() => {
    setCurrentIndex(prev => Math.max(prev - 1, 0));
  }, []);

  const goToQuestion = useCallback((index: number) => {
    if (index >= 0 && index < questions.length) {
      setCurrentIndex(index);
    }
  }, [questions.length]);

  const resetQuestions = useCallback(() => {
    setCurrentIndex(0);
  }, []);

  return {
    questions,
    currentIndex,
    currentQuestion,
    totalQuestions: questions.length,
    isLoading,
    goToNext,
    goToPrevious,
    goToQuestion,
    resetQuestions,
    subjects,
    topics,
    microTopics,
    years,
  };
};

// Custom hook for question session management
interface SessionState {
  answered: Set<number>;
  correct: Set<number>;
  incorrect: Set<number>;
  bookmarked: Set<number>;
  selectedAnswers: { [questionId: number]: string };
}

interface UseQuestionSessionReturn extends UseQuestionsReturn {
  sessionState: SessionState;
  selectAnswer: (questionId: number, answer: string) => void;
  checkAnswer: (questionId: number) => boolean | null;
  toggleBookmark: (questionId: number) => void;
  isBookmarked: (questionId: number) => boolean;
  isAnswered: (questionId: number) => boolean;
  getSelectedAnswer: (questionId: number) => string | null;
  getSessionStats: () => { total: number; answered: number; correct: number; accuracy: number };
  resetSession: () => void;
}

export const useQuestionSession = (options: UseQuestionsOptions = {}): UseQuestionSessionReturn => {
  const questionsData = useQuestions(options);
  
  const [sessionState, setSessionState] = useState<SessionState>({
    answered: new Set(),
    correct: new Set(),
    incorrect: new Set(),
    bookmarked: new Set(),
    selectedAnswers: {},
  });

  // Load bookmarks from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('gate_bookmarks');
    if (saved) {
      try {
        const bookmarks = JSON.parse(saved);
        setSessionState(prev => ({
          ...prev,
          bookmarked: new Set(bookmarks),
        }));
      } catch (e) {
        console.error('Failed to load bookmarks:', e);
      }
    }
  }, []);

  // Save bookmarks to localStorage
  useEffect(() => {
    localStorage.setItem('gate_bookmarks', JSON.stringify([...sessionState.bookmarked]));
  }, [sessionState.bookmarked]);

  const selectAnswer = useCallback((questionId: number, answer: string) => {
    setSessionState(prev => ({
      ...prev,
      selectedAnswers: { ...prev.selectedAnswers, [questionId]: answer },
    }));
  }, []);

  const checkAnswer = useCallback((questionId: number): boolean | null => {
    const question = questionsData.questions.find(q => q.id === questionId);
    const selectedAnswer = sessionState.selectedAnswers[questionId];
    
    if (!question || !selectedAnswer) return null;
    
    const isCorrect = selectedAnswer === question.answer;
    
    setSessionState(prev => {
      const newAnswered = new Set(prev.answered).add(questionId);
      const newCorrect = new Set(prev.correct);
      const newIncorrect = new Set(prev.incorrect);
      
      if (isCorrect) {
        newCorrect.add(questionId);
        newIncorrect.delete(questionId);
      } else {
        newIncorrect.add(questionId);
        newCorrect.delete(questionId);
      }
      
      return {
        ...prev,
        answered: newAnswered,
        correct: newCorrect,
        incorrect: newIncorrect,
      };
    });
    
    return isCorrect;
  }, [questionsData.questions, sessionState.selectedAnswers]);

  const toggleBookmark = useCallback((questionId: number) => {
    setSessionState(prev => {
      const newBookmarked = new Set(prev.bookmarked);
      if (newBookmarked.has(questionId)) {
        newBookmarked.delete(questionId);
      } else {
        newBookmarked.add(questionId);
      }
      return { ...prev, bookmarked: newBookmarked };
    });
  }, []);

  const isBookmarked = useCallback((questionId: number): boolean => {
    return sessionState.bookmarked.has(questionId);
  }, [sessionState.bookmarked]);

  const isAnswered = useCallback((questionId: number): boolean => {
    return sessionState.answered.has(questionId);
  }, [sessionState.answered]);

  const getSelectedAnswer = useCallback((questionId: number): string | null => {
    return sessionState.selectedAnswers[questionId] || null;
  }, [sessionState.selectedAnswers]);

  const getSessionStats = useCallback(() => {
    const total = questionsData.questions.length;
    const answered = sessionState.answered.size;
    const correct = sessionState.correct.size;
    const accuracy = answered > 0 ? (correct / answered) * 100 : 0;
    
    return { total, answered, correct, accuracy };
  }, [questionsData.questions.length, sessionState.answered, sessionState.correct]);

  const resetSession = useCallback(() => {
    setSessionState(prev => ({
      answered: new Set(),
      correct: new Set(),
      incorrect: new Set(),
      bookmarked: prev.bookmarked, // Keep bookmarks
      selectedAnswers: {},
    }));
    questionsData.resetQuestions();
  }, [questionsData]);

  return {
    ...questionsData,
    sessionState,
    selectAnswer,
    checkAnswer,
    toggleBookmark,
    isBookmarked,
    isAnswered,
    getSelectedAnswer,
    getSessionStats,
    resetSession,
  };
};
