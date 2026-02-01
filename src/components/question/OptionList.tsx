import { cn } from "@/lib/utils";
import { Check, X } from "lucide-react";

interface OptionListProps {
  choices: string[];
  selectedAnswer: string | null;
  correctAnswer: string | null;
  isAnswered: boolean;
  onSelect: (answer: string) => void;
}

/**
 * Option list component with clear visual feedback
 * Research: Adequate touch targets (48px minimum) for accessibility
 * Visual feedback following Gestalt proximity principle (12px gap)
 */
export const OptionList = ({
  choices,
  selectedAnswer,
  correctAnswer,
  isAnswered,
  onSelect,
}: OptionListProps) => {
  const getOptionLabel = (index: number): string => {
    return String.fromCharCode(65 + index); // A, B, C, D
  };

  const isOptionCorrect = (choice: string, index: number): boolean => {
    if (!correctAnswer) return false;
    // Handle various answer formats: "(A)", "Option A", "A", etc.
    const label = getOptionLabel(index);
    return (
      correctAnswer === `(${label})` ||
      correctAnswer === `Option ${label}` ||
      correctAnswer === label ||
      correctAnswer.toLowerCase().includes(choice.toLowerCase().substring(0, 20))
    );
  };

  const isSelected = (choice: string, index: number): boolean => {
    if (!selectedAnswer) return false;
    const label = getOptionLabel(index);
    return (
      selectedAnswer === choice ||
      selectedAnswer === `(${label})` ||
      selectedAnswer === `Option ${label}` ||
      selectedAnswer === label
    );
  };

  return (
    <div className="space-y-3" role="radiogroup" aria-label="Answer options">
      {choices.map((choice, index) => {
        const label = getOptionLabel(index);
        const selected = isSelected(choice, index);
        const correct = isOptionCorrect(choice, index);
        const showCorrect = isAnswered && correct;
        const showIncorrect = isAnswered && selected && !correct;
        
        return (
          <button
            key={index}
            onClick={() => !isAnswered && onSelect(`(${label})`)}
            disabled={isAnswered}
            role="radio"
            aria-checked={selected}
            className={cn(
              "option-item w-full text-left flex items-start gap-4",
              "min-h-[48px]", // WCAG touch target
              selected && !isAnswered && "selected",
              showCorrect && "correct",
              showIncorrect && "incorrect",
              isAnswered && "cursor-default"
            )}
          >
            {/* Option label circle */}
            <div
              className={cn(
                "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                "border-2 font-medium text-sm transition-colors",
                !isAnswered && !selected && "border-muted-foreground/30 text-muted-foreground",
                !isAnswered && selected && "border-primary bg-primary text-primary-foreground",
                showCorrect && "border-correct bg-correct text-correct-foreground",
                showIncorrect && "border-incorrect bg-incorrect text-incorrect-foreground"
              )}
            >
              {showCorrect ? (
                <Check className="h-4 w-4" />
              ) : showIncorrect ? (
                <X className="h-4 w-4" />
              ) : (
                label
              )}
            </div>
            
            {/* Option text */}
            <span className={cn(
              "flex-1 text-option leading-relaxed pt-1",
              isAnswered && !correct && !selected && "text-muted-foreground"
            )}>
              {/* Remove the option prefix if present (A), (B), etc. */}
              {choice.replace(/^\([A-D]\)\s*/, '')}
            </span>
          </button>
        );
      })}
    </div>
  );
};
