import { useState, useMemo } from "react";
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
import { BookOpen, Filter, RotateCcw, Trophy } from "lucide-react";

/**
 * Practice page with subject and topic filtering
 * Research: Single-task focus interface (Sweller's Cognitive Load Theory)
 * Progressive disclosure with one question at a time
 */
const Practice = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSubject = searchParams.get("subject") || undefined;
  
  const [selectedSubject, setSelectedSubject] = useState<string | undefined>(initialSubject);
  const [selectedTopic, setSelectedTopic] = useState<string | undefined>();
  const [selectedYear, setSelectedYear] = useState<number | undefined>();
  
  const subjects = getAllSubjects();
  const years = getYearsCovered();
  
  const session = useQuestionSession({
    subject: selectedSubject,
    topic: selectedTopic,
    year: selectedYear,
  });
  
  const { recordAttempt } = useProgress();

  // Handle filter changes
  const handleSubjectChange = (value: string) => {
    const newSubject = value === "all" ? undefined : value;
    setSelectedSubject(newSubject);
    setSelectedTopic(undefined);
    if (newSubject) {
      setSearchParams({ subject: newSubject });
    } else {
      setSearchParams({});
    }
  };

  const handleTopicChange = (value: string) => {
    setSelectedTopic(value === "all" ? undefined : value);
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
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <BookOpen className="h-6 w-6 text-primary" />
            Practice Questions
          </h1>
          <p className="text-muted-foreground text-sm mt-1">
            {session.totalQuestions} questions available
          </p>
        </div>
        
        <Button
          variant="outline"
          onClick={session.resetSession}
          className="gap-2"
        >
          <RotateCcw className="h-4 w-4" />
          Reset Session
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center gap-2">
            <Filter className="h-4 w-4" />
            Filters
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-3 gap-4">
            {/* Subject filter */}
            <div>
              <label className="text-xs text-muted-foreground mb-1.5 block">
                Subject
              </label>
              <Select
                value={selectedSubject || "all"}
                onValueChange={handleSubjectChange}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Subjects" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Subjects</SelectItem>
                  {subjects.map((subject) => (
                    <SelectItem key={subject} value={subject}>
                      {subjectIcons[subject]} {subject}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Topic filter */}
            <div>
              <label className="text-xs text-muted-foreground mb-1.5 block">
                Topic
              </label>
              <Select
                value={selectedTopic || "all"}
                onValueChange={handleTopicChange}
                disabled={!selectedSubject}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Topics" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Topics</SelectItem>
                  {session.topics.map((topic) => (
                    <SelectItem key={topic} value={topic}>
                      {topic}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Year filter */}
            <div>
              <label className="text-xs text-muted-foreground mb-1.5 block">
                Year
              </label>
              <Select
                value={selectedYear?.toString() || "all"}
                onValueChange={handleYearChange}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Years" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Years</SelectItem>
                  {years.slice().reverse().map((year) => (
                    <SelectItem key={year} value={year.toString()}>
                      GATE {year}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Session stats */}
      {stats.answered > 0 && (
        <div className="flex items-center gap-4 flex-wrap text-sm">
          <Badge variant="secondary" className="gap-1">
            <Trophy className="h-3 w-3" />
            {stats.correct} correct
          </Badge>
          <Badge variant="outline">
            {stats.answered} / {stats.total} answered
          </Badge>
          <Badge 
            variant="outline"
            className={stats.accuracy >= 70 ? "text-success border-success" : ""}
          >
            {stats.accuracy.toFixed(1)}% accuracy
          </Badge>
        </div>
      )}

      {/* Question display */}
      {session.currentQuestion ? (
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
      ) : (
        <Card className="p-12 text-center">
          <p className="text-muted-foreground">
            {session.isLoading
              ? "Loading questions..."
              : "No questions found matching your filters. Try adjusting the filters."}
          </p>
        </Card>
      )}
    </div>
  );
};

export default Practice;
