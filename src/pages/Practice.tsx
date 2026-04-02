import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { QuestionCard } from "@/components/question/QuestionCard";
import { useQuestionSession } from "@/hooks/useQuestions";
import { useProgress } from "@/hooks/useProgress";
import { subjectIcons, getAllSubjects, getYearsCovered } from "@/data/gateData";
import { BookOpen, Filter, RotateCcw, Trophy, CheckCircle, BarChart2 } from "lucide-react";

/**
 * Practice page: "Digital Paper" Theme
 * Design Principle: Minimizing Extraneous Cognitive Load
 * Background: Light (#F8FAFC) for maximum readability.
 * Contrast: Dark Grey (#1E293B) text for sustained reading.
 */
const Practice = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSubject = searchParams.get("subject") || undefined;
  
  const [selectedSubject, setSelectedSubject] = useState<string | undefined>(initialSubject);
  const [selectedTopic, setSelectedTopic] = useState<string | undefined>();
  const [selectedMicroTopic, setSelectedMicroTopic] = useState<string | undefined>();
  const [selectedYear, setSelectedYear] = useState<number | undefined>();
  
  const subjects = getAllSubjects();
  const years = getYearsCovered();
  
  const session = useQuestionSession({
    subject: selectedSubject,
    topic: selectedTopic,
    microTopic: selectedMicroTopic,
    year: selectedYear,
  });
  
  const { recordAttempt } = useProgress();

  // Handle filter changes
  const handleSubjectChange = (value: string) => {
    const newSubject = value === "all" ? undefined : value;
    setSelectedSubject(newSubject);
    setSelectedTopic(undefined);
    setSelectedMicroTopic(undefined);
    if (newSubject) {
      setSearchParams({ subject: newSubject });
    } else {
      setSearchParams({});
    }
  };

  const handleTopicChange = (value: string) => {
    setSelectedTopic(value === "all" ? undefined : value);
    setSelectedMicroTopic(undefined);
  };

  const handleMicroTopicChange = (value: string) => {
    setSelectedMicroTopic(value === "all" ? undefined : value);
  };

  const handleYearChange = (value: string) => {
    setSelectedYear(value === "all" ? undefined : parseInt(value));
  };

  // Handle answer checking
  const handleCheckAnswer = () => {
    if (!session.currentQuestion) return;
    
    const isCorrect = session.checkAnswer(session.currentQuestion.id);
    if (isCorrect !== null && session.currentQuestion) {
      recordAttempt(session.currentQuestion.subject, isCorrect);
    }
  };

  // Session stats
  const stats = session.getSessionStats();

  return (
    // 1. BACKGROUND: Deep Midnight Navy (Slate 950) - Cinema Mode
    <div className="bg-slate-950 min-h-[calc(100vh-3.5rem)] -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 text-slate-100 transition-colors duration-500">
      <div className="space-y-8 max-w-5xl mx-auto animate-fade-in relative z-10">
        
        {/* Header Section - Dimmed/Subtle */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/5 pb-4">
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-3 text-slate-300">
              <span className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
                <BookOpen className="h-5 w-5 text-blue-400" />
              </span>
              Practice Session
            </h1>
            <p className="text-slate-500 text-sm mt-1 ml-1 font-medium">
              Cinema Focus Mode • <span className="text-slate-400">{session.totalQuestions} questions</span>
            </p>
          </div>
          
          <Button
            variant="ghost"
            onClick={session.resetSession}
            className="gap-2 text-slate-500 hover:text-slate-300 hover:bg-white/5 transition-all"
          >
            <RotateCcw className="h-4 w-4" />
            Reset
          </Button>
        </div>

        {/* Filters - Glass/Dimmed Control Panel */}
        {/* Hidden/Collapsed by default or Subtle styling so it doesn't distract */}
        <Card className="bg-slate-900/50 border border-white/5 shadow-none backdrop-blur-sm">
           <CardContent className="px-6 py-4">
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Subject filter */}
              <div className="relative group">
                <label className="text-xs text-slate-500 mb-1.5 block font-semibold uppercase tracking-wider group-hover:text-blue-400 transition-colors">
                  Subject
                </label>
                <Select
                  value={selectedSubject || "all"}
                  onValueChange={handleSubjectChange}
                >
                  <SelectTrigger className="bg-slate-900 border-slate-800 text-slate-300 focus:ring-blue-500/50 focus:border-blue-500/50">
                    <SelectValue placeholder="All Subjects" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800 text-slate-300">
                    <SelectItem value="all" className="focus:bg-slate-800 focus:text-white">All Subjects</SelectItem>
                    {subjects.map((subject) => (
                      <SelectItem key={subject} value={subject} className="focus:bg-slate-800 focus:text-white">
                        <span className="flex items-center gap-2">
                           {subjectIcons[subject]} {subject}
                        </span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Topic filter */}
              <div className="relative group">
                <label className="text-xs text-slate-500 mb-1.5 block font-semibold uppercase tracking-wider group-hover:text-blue-400 transition-colors">
                  Topic
                </label>
                <Select
                  value={selectedTopic || "all"}
                  onValueChange={handleTopicChange}
                  disabled={!selectedSubject}
                >
                  <SelectTrigger className="bg-slate-900 border-slate-800 text-slate-300 focus:ring-blue-500/50 focus:border-blue-500/50">
                    <SelectValue placeholder="All Topics" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800 text-slate-300">
                    <SelectItem value="all" className="focus:bg-slate-800 focus:text-white">All Topics</SelectItem>
                    {session.topics.map((topic) => (
                      <SelectItem key={topic} value={topic} className="focus:bg-slate-800 focus:text-white">
                        {topic}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Micro-topic filter */}
              <div className="relative group">
                <label className="text-xs text-slate-500 mb-1.5 block font-semibold uppercase tracking-wider group-hover:text-blue-400 transition-colors">
                  Micro Topic
                </label>
                <Select
                  value={selectedMicroTopic || "all"}
                  onValueChange={handleMicroTopicChange}
                  disabled={!selectedTopic}
                >
                  <SelectTrigger className="bg-slate-900 border-slate-800 text-slate-300 focus:ring-blue-500/50 focus:border-blue-500/50">
                    <SelectValue placeholder="All Micro Topics" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800 text-slate-300">
                    <SelectItem value="all" className="focus:bg-slate-800 focus:text-white">All Micro Topics</SelectItem>
                    {session.microTopics.map((mTopic) => (
                      <SelectItem key={mTopic} value={mTopic} className="focus:bg-slate-800 focus:text-white">
                        {mTopic}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Year filter */}
              <div className="relative group">
                <label className="text-xs text-slate-500 mb-1.5 block font-semibold uppercase tracking-wider group-hover:text-blue-400 transition-colors">
                  Year
                </label>
                <Select
                  value={selectedYear?.toString() || "all"}
                  onValueChange={handleYearChange}
                >
                  <SelectTrigger className="bg-slate-900 border-slate-800 text-slate-300 focus:ring-blue-500/50 focus:border-blue-500/50">
                    <SelectValue placeholder="All Years" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800 text-slate-300">
                    <SelectItem value="all" className="focus:bg-slate-800 focus:text-white">All Years</SelectItem>
                    {years.slice().reverse().map((year) => (
                      <SelectItem key={year} value={year.toString()} className="focus:bg-slate-800 focus:text-white">
                        GATE {year}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 3. PROGRESS INDICATORS: Minimalist Neon */}
        {stats.answered > 0 && (
          <div className="flex items-center justify-center gap-4 flex-wrap text-sm animate-fade-in opacity-80 hover:opacity-100 transition-opacity">
            <div className="flex items-center gap-2 text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
              <CheckCircle className="h-4 w-4" />
              <span className="font-mono font-bold">{stats.correct}</span> Correct
            </div>
            <div className="flex items-center gap-2 text-slate-400 bg-slate-800/50 px-3 py-1 rounded-full border border-white/5">
              <BarChart2 className="h-4 w-4" />
              <span>{stats.answered}/{stats.total} Answered</span>
            </div>
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${stats.accuracy >= 70 ? 'text-blue-400 bg-blue-500/10 border-blue-500/20' : 'text-amber-400 bg-amber-500/10 border-amber-500/20'}`}>
              <Trophy className="h-4 w-4" />
              <span className="font-mono font-bold">{stats.accuracy.toFixed(0)}%</span> Accuracy
            </div>
          </div>
        )}

        {/* 4. QUESTION CARD: The Hero Spotlight */}
        {/* Silver White Card floating in Dark Void with Blue Glow */}
        {session.currentQuestion ? (
          <div className="relative group perspective-1000">
            {/* The Glow Effect */}
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
            
            {/* The Card Surface */}
            <div className="relative bg-slate-50 rounded-xl shadow-[0_0_40px_-10px_rgba(59,130,246,0.3)] overflow-hidden border border-slate-200">
               {/* Accent Line */}
               <div className="h-1.5 w-full bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-600"></div>
               
               <div className="p-2 md:p-4">
                <QuestionCard
                  question={session.currentQuestion}
                  questionNumber={session.currentIndex + 1}
                  totalQuestions={session.totalQuestions}
                  selectedAnswer={session.getSelectedAnswer(session.currentQuestion.id)}
                  isAnswered={session.isAnswered(session.currentQuestion.id)}
                  isCorrect={
                    session.isAnswered(session.currentQuestion.id)
                      ? session.sessionState.correct.has(session.currentQuestion.id)
                      : null
                  }
                  isBookmarked={session.isBookmarked(session.currentQuestion.id)}
                  onSelectAnswer={(answer) =>
                    session.selectAnswer(session.currentQuestion!.id, answer)
                  }
                  onCheckAnswer={handleCheckAnswer}
                  onToggleBookmark={() =>
                    session.toggleBookmark(session.currentQuestion!.id)
                  }
                  onNext={session.goToNext}
                  onPrevious={session.goToPrevious}
                  hasPrevious={session.currentIndex > 0}
                  hasNext={session.currentIndex < session.totalQuestions - 1}
                />
              </div>
            </div>
          </div>
        ) : (
          <Card className="p-16 text-center bg-transparent border border-dashed border-slate-800 shadow-none">
            <div className="flex flex-col items-center gap-3">
              <div className="p-4 bg-slate-900 rounded-full border border-slate-800">
                <Filter className="h-8 w-8 text-slate-700" />
              </div>
              <h3 className="text-xl font-bold text-slate-400">Ready to Focus?</h3>
              <p className="text-slate-600 max-w-sm mx-auto">
                {session.isLoading
                  ? "Initializing Focus Mode..."
                  : "No questions match your criteria. Adjust filters to begin."}
              </p>
              <Button 
                variant="outline" 
                onClick={() => {
                   handleSubjectChange("all");
                   handleYearChange("all");
                }}
                className="mt-6 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800 hover:border-slate-600"
              >
                Clear Filters
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Practice;