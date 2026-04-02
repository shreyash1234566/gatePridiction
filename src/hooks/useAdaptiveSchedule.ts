import { useState, useEffect } from 'react';

// A simple hook to manage a sequential queue-based schedule
export function useAdaptiveSchedule(totalPhases: number = 6, daysPerPhase: number = 5) {
  const [currentDayIndex, setCurrentDayIndex] = useState(0); // 0 to 4 inside the current phase
  const [currentPhase, setCurrentPhase] = useState("1");
  const [streak, setStreak] = useState(0);
  const [lastStudyDate, setLastStudyDate] = useState<string | null>(null);
  const [lowEnergyMode, setLowEnergyMode] = useState(false);

  useEffect(() => {
    const savedDay = localStorage.getItem('adaptive_currentDay');
    if (savedDay) setCurrentDayIndex(parseInt(savedDay, 10));

    const savedPhase = localStorage.getItem('adaptive_currentPhase');
    if (savedPhase) setCurrentPhase(savedPhase);

    const savedStreak = localStorage.getItem('adaptive_streak');
    if (savedStreak) setStreak(parseInt(savedStreak, 10));

    const savedDate = localStorage.getItem('adaptive_lastDate');
    if (savedDate) setLastStudyDate(savedDate);
  }, []);

  const todayStr = new Date().toISOString().split('T')[0];

  const completeDay = () => {
    // If completed today already, do nothing or just update streak logic
    if (lastStudyDate !== todayStr) {
      // Calculate if missed days to reset streak, otherwise increment
      // Simple logic: if lastDate was yesterday, increment. If earlier, reset to 1.
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];

      let newStreak = streak;
      if (lastStudyDate === yesterdayStr) {
        newStreak += 1;
      } else if (lastStudyDate !== todayStr) {
        newStreak = 1; // Restart streak
      }
      
      setStreak(newStreak);
      localStorage.setItem('adaptive_streak', newStreak.toString());
    }
    
    setLastStudyDate(todayStr);
    localStorage.setItem('adaptive_lastDate', todayStr);

    // Only advance the actual curriculum if NOT in low energy mode
    if (!lowEnergyMode) {
      let nextDay = currentDayIndex + 1;
      let nextPhase = currentPhase;

      if (nextDay >= daysPerPhase) {
        nextDay = 0;
        const nextPhaseNum = parseInt(currentPhase, 10) + 1;
        if (nextPhaseNum <= totalPhases) {
          nextPhase = nextPhaseNum.toString();
        }
      }

      setCurrentDayIndex(nextDay);
      setCurrentPhase(nextPhase);
      
      localStorage.setItem('adaptive_currentDay', nextDay.toString());
      localStorage.setItem('adaptive_currentPhase', nextPhase);
    }
    
    // Reset low energy mode for the next day
    setLowEnergyMode(false);
  };

  const toggleLowEnergyMode = () => {
    setLowEnergyMode(!lowEnergyMode);
  };

  return {
    currentDayIndex,
    currentPhase,
    streak,
    lastStudyDate,
    lowEnergyMode,
    toggleLowEnergyMode,
    completeDay,
    todayStr
  };
}