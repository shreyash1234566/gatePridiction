import { useState } from "react";
import { Question } from "@/data/gateData";
import { OptionList } from "./OptionList";
import { SolutionReveal } from "./SolutionReveal";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  Bookmark, 
  BookmarkCheck, 
  ChevronLeft, 
  ChevronRight,
  Check,
  RotateCcw
} from "lucide-react";
import { cn } from "@/lib/utils";

interface QuestionCardProps {
  question: Question;
  questionNumber: number;
  totalQuestions: number;
  selectedAnswer: string | null;
  isAnswered: boolean;
  isCorrect: boolean | null;
  isBookmarked: boolean;
  onSelectAnswer: (answer: string) => void;
  onCheckAnswer: () => void;
  onToggleBookmark: () => void;
  onNext: () => void;
  onPrevious: () => void;
  hasPrevious: boolean;
  hasNext: boolean;
}

/**
 * Question display card - Single task focus interface
 * Research: Sweller's Cognitive Load Theory - One question at a time
 * Typography: Source Serif Pro at 18px with 1.75 line-height (Dyson & Haselgrove)
 */
export const QuestionCard = ({
  question,
  questionNumber,
  totalQuestions,
  selectedAnswer,
  isAnswered,
  isCorrect,
  isBookmarked,
  onSelectAnswer,
  onCheckAnswer,
  onToggleBookmark,
  onNext,
  onPrevious,
  hasPrevious,
  hasNext,
}: QuestionCardProps) => {
  const [showSolution, setShowSolution] = useState(false);

  // Reset solution visibility when question changes
  const handleNext = () => {
    setShowSolution(false);
    onNext();
  };

  const handlePrevious = () => {
    setShowSolution(false);
    onPrevious();
  };

  return (
    <div className="w-full max-w-reading mx-auto animate-fade-in">
      {/* Question header with metadata */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3 flex-wrap">
          <Badge variant="secondary" className="text-xs">
            {question.subject}
          </Badge>
          <Badge variant="outline" className="text-xs">
            {question.topic}
          </Badge>
          <Badge variant="outline" className="text-xs">
            GATE {question.year}
          </Badge>
        </div>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleBookmark}
          aria-label={isBookmarked ? "Remove bookmark" : "Add bookmark"}
          className={cn(
            "transition-colors text-slate-900 hover:bg-emerald-500 hover:text-white",
            isBookmarked && "text-emerald-600 bg-emerald-100 hover:bg-emerald-600"
          )}
        >
          {isBookmarked ? (
            <BookmarkCheck className="h-5 w-5" />
          ) : (
            <Bookmark className="h-5 w-5" />
          )}
        </Button>
      </div>

      {/* Progress indicator */}
      <div className="flex items-center gap-3 mb-6 text-sm font-mono text-slate-500">
        <span className="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-xs font-bold border border-slate-200">
          Q{questionNumber}
        </span>
        <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <div 
            className="h-full bg-blue-500 transition-all duration-300"
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          />
        </div>
        <span className="font-semibold text-slate-400">{totalQuestions - questionNumber} left</span>
      </div>

      {/* Question card */}
      <Card className="question-card mb-8 border-none shadow-none bg-transparent">
        {/* Question text - Research: Serif font for reading comprehension */}
        <div className="font-serif text-xl md:text-2xl leading-relaxed text-slate-900 mb-8 font-medium">
          <p className="whitespace-pre-wrap">{question.question_text}</p>
        </div>

        {/* Options */}
        {question.question_type === 'MCQ' && question.choices && (
          <OptionList
            choices={question.choices}
            selectedAnswer={selectedAnswer}
            correctAnswer={isAnswered ? question.answer : null}
            isAnswered={isAnswered}
            onSelect={onSelectAnswer}
          />
        )}

        {/* NAT Input */}
        {question.question_type === 'NAT' && (
          <div className="mt-8">
            <label className="block text-sm font-semibold text-slate-700 mb-3 uppercase tracking-wider">
              Numerical Answer:
            </label>
            <input
              type="text"
              value={selectedAnswer || ''}
              onChange={(e) => onSelectAnswer(e.target.value)}
              disabled={isAnswered}
              className="w-full max-w-sm px-4 py-3 rounded-lg bg-white border border-slate-300 
                         focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:outline-none 
                         disabled:opacity-60 font-mono text-xl text-slate-900 placeholder:text-slate-400 shadow-sm"
              placeholder="Enter value..."
            />
          </div>
        )}
      </Card>

      {/* Action buttons */}
      <div className="flex items-center justify-between gap-4 pt-4 border-t border-slate-100">
        <Button
          variant="ghost"
          onClick={handlePrevious}
          disabled={!hasPrevious}
          className="gap-2 text-slate-500 hover:text-slate-900 hover:bg-slate-100"
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </Button>

        <div className="flex items-center gap-3">
          {!isAnswered && selectedAnswer && (
            <Button onClick={onCheckAnswer} className="gap-2 bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/30 transition-all">
              <Check className="h-4 w-4" />
              Check Answer
            </Button>
          )}
          
          {isAnswered && !showSolution && (
            <Button 
              variant="secondary" 
              onClick={() => setShowSolution(true)}
              className="gap-2 bg-amber-100 text-amber-900 hover:bg-amber-200 border border-amber-200"
            >
              Show Solution
            </Button>
          )}
          
          {isAnswered && showSolution && (
            <Button 
              variant="ghost" 
              onClick={() => setShowSolution(false)}
              className="gap-2 text-slate-500"
            >
              Hide Solution
            </Button>
          )}
        </div>

        <Button
          onClick={handleNext}
          disabled={!hasNext}
          className="gap-2 bg-slate-900 hover:bg-slate-800 text-white shadow-md"
        >
          Next
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>

      {/* Solution reveal - Progressive disclosure */}
      {isAnswered && showSolution && (
        <SolutionReveal
          question={question}
          isCorrect={isCorrect}
          selectedAnswer={selectedAnswer}
        />
      )}
    </div>
  );
};
