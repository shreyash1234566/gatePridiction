import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { 
  Check, 
  X, 
  Bookmark, 
  Circle, 
  ChevronLeft, 
  ChevronRight 
} from "lucide-react";

interface QuestionStatus {
  id: number;
  index: number;
  isAnswered: boolean;
  isCorrect: boolean | null;
  isBookmarked: boolean;
}

interface QuestionPaletteProps {
  questions: QuestionStatus[];
  currentIndex: number;
  onSelectQuestion: (index: number) => void;
  onClose?: () => void;
}

/**
 * Question navigation palette for mock tests
 * Research: Miller's Law - Visual chunking for 7±2 items
 * Uses distinct visual states for quick scanning
 */
export const QuestionPalette = ({
  questions,
  currentIndex,
  onSelectQuestion,
  onClose,
}: QuestionPaletteProps) => {
  // Calculate statistics
  const stats = {
    total: questions.length,
    answered: questions.filter(q => q.isAnswered).length,
    correct: questions.filter(q => q.isCorrect === true).length,
    incorrect: questions.filter(q => q.isCorrect === false).length,
    bookmarked: questions.filter(q => q.isBookmarked).length,
    unanswered: questions.filter(q => !q.isAnswered).length,
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4 w-full max-w-sm">
      {/* Header with stats */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-sm">Question Navigator</h3>
        {onClose && (
          <Button variant="ghost" size="sm" onClick={onClose}>
            Close
          </Button>
        )}
      </div>

      {/* Statistics summary */}
      <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded bg-correct" />
          <span>{stats.correct} Correct</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded bg-incorrect" />
          <span>{stats.incorrect} Wrong</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded bg-muted-foreground/30" />
          <span>{stats.unanswered} Left</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-muted rounded-sm overflow-hidden mb-4 border border-border/50">
        <div 
          className="h-full bg-primary transition-all duration-300"
          style={{ width: `${(stats.answered / stats.total) * 100}%` }}
        />
      </div>

      {/* Question grid */}
      <div className="grid grid-cols-8 gap-1.5 max-h-[300px] overflow-y-auto p-1">
        {questions.map((q) => (
          <button
            key={q.id}
            onClick={() => onSelectQuestion(q.index)}
            className={cn(
              "w-8 h-8 rounded flex items-center justify-center text-xs font-medium",
              "transition-all duration-150 hover:scale-110 focus:ring-2 focus:ring-ring",
              // Current question
              q.index === currentIndex && "ring-2 ring-primary",
              // States
              !q.isAnswered && "bg-muted text-muted-foreground",
              q.isAnswered && q.isCorrect === true && "bg-correct text-correct-foreground",
              q.isAnswered && q.isCorrect === false && "bg-incorrect text-incorrect-foreground",
              q.isAnswered && q.isCorrect === null && "bg-primary/20 text-primary",
              // Bookmarked overlay
              q.isBookmarked && "ring-2 ring-warning"
            )}
            aria-label={`Question ${q.index + 1}${q.isBookmarked ? ' (bookmarked)' : ''}`}
          >
            {q.index + 1}
          </button>
        ))}
      </div>

      {/* Legend */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Check className="h-3 w-3 text-correct" />
            Correct
          </div>
          <div className="flex items-center gap-1">
            <X className="h-3 w-3 text-incorrect" />
            Incorrect
          </div>
          <div className="flex items-center gap-1">
            <Circle className="h-3 w-3" />
            Unanswered
          </div>
          <div className="flex items-center gap-1">
            <Bookmark className="h-3 w-3 text-warning" />
            Bookmarked
          </div>
        </div>
      </div>

      {/* Quick navigation */}
      <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onSelectQuestion(Math.max(0, currentIndex - 1))}
          disabled={currentIndex === 0}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        
        <span className="text-sm text-muted-foreground">
          {currentIndex + 1} / {stats.total}
        </span>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => onSelectQuestion(Math.min(stats.total - 1, currentIndex + 1))}
          disabled={currentIndex === stats.total - 1}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};
