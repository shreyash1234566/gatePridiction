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
            "transition-colors",
            isBookmarked && "text-primary"
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
      <div className="flex items-center gap-3 mb-4 text-sm text-muted-foreground">
        <span>Question {questionNumber} of {totalQuestions}</span>
        <div className="flex-1 h-1 bg-muted rounded-full overflow-hidden">
          <div 
            className="h-full bg-primary transition-all duration-300"
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          />
        </div>
        <span className="font-medium">{question.marks} mark{question.marks > 1 ? 's' : ''}</span>
      </div>

      {/* Question card */}
      <Card className="question-card mb-6">
        {/* Question text - Research: Serif font for reading comprehension */}
        <div className="font-serif text-question leading-reading mb-8">
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
          <div className="mt-6">
            <label className="block text-sm text-muted-foreground mb-2">
              Enter your answer (Numerical Answer Type):
            </label>
            <input
              type="text"
              value={selectedAnswer || ''}
              onChange={(e) => onSelectAnswer(e.target.value)}
              disabled={isAnswered}
              className="w-full max-w-xs px-4 py-3 rounded-lg bg-input border border-border 
                         focus:ring-2 focus:ring-ring focus:outline-none
                         disabled:opacity-60 font-mono text-lg"
              placeholder="Enter numerical answer..."
            />
          </div>
        )}
      </Card>

      {/* Action buttons */}
      <div className="flex items-center justify-between gap-4">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={!hasPrevious}
          className="gap-2"
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </Button>

        <div className="flex items-center gap-3">
          {!isAnswered && selectedAnswer && (
            <Button onClick={onCheckAnswer} className="gap-2">
              <Check className="h-4 w-4" />
              Check Answer
            </Button>
          )}
          
          {isAnswered && !showSolution && (
            <Button 
              variant="secondary" 
              onClick={() => setShowSolution(true)}
              className="gap-2"
            >
              Show Solution
            </Button>
          )}
          
          {isAnswered && showSolution && (
            <Button 
              variant="ghost" 
              onClick={() => setShowSolution(false)}
              className="gap-2"
            >
              <RotateCcw className="h-4 w-4" />
              Hide Solution
            </Button>
          )}
        </div>

        <Button
          variant="outline"
          onClick={handleNext}
          disabled={!hasNext}
          className="gap-2"
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
