import { cn } from "@/lib/utils";
import { Check, CheckCircle, X } from "lucide-react";

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
    <div className="grid md:grid-cols-2 gap-4" role="radiogroup" aria-label="Answer options">
      {choices.map((choice, index) => {
        const label = getOptionLabel(index);
        const selected = isSelected(choice, index);
        const correct = isOptionCorrect(choice, index);
        const showCorrect = isAnswered && correct;
        
        // AFCAT "Interactive Row" Logic
        // If answered, incorrect ones get dim, correct gets green glow
        const dim = isAnswered && !selected && !correct;

        return (
          <button
            key={index}
            onClick={() => !isAnswered && onSelect(`(${label})`)}
            disabled={isAnswered}
            role="radio"
            aria-checked={selected}
            className={cn(
              "relative group flex items-center gap-4 w-full text-left p-5",
               "rounded-xl border transition-all duration-200 shadow-sm",
               // Selected State: Bright Blue Border & Light Blue BG
               selected && !isAnswered && "bg-blue-50 border-blue-500 ring-1 ring-blue-500 text-blue-900 shadow-md",
               // Unselected State: Clean Paper
               !selected && !isAnswered && "bg-white border-slate-200 text-slate-700 hover:border-blue-300 hover:bg-slate-50 hover:shadow",
               // Correct State
               showCorrect && "bg-emerald-50 border-emerald-500 text-emerald-900 ring-1 ring-emerald-500",
               // Incorrect Selected State
               isAnswered && selected && !correct && "bg-red-50 border-red-500 text-red-900 ring-1 ring-red-500",
               // Dimmed State
               dim && "opacity-40 grayscale"
            )}
          >
            {/* The "Bubble" Index */}
            <span className={cn(
              "flex items-center justify-center w-8 h-8 rounded-lg text-xs font-bold transition-colors",
              selected && !isAnswered ? "bg-blue-600 text-white" : "bg-slate-100 text-slate-500 group-hover:bg-slate-200",
              showCorrect && "bg-emerald-600 text-white",
              isAnswered && selected && !correct && "bg-red-600 text-white"
            )}>
              {label}
            </span>
            
            {/* Option Text */}
            <span className={cn(
              "font-medium text-base leading-relaxed flex-1",
              selected && !isAnswered ? 'text-blue-900' : 'text-slate-700',
               showCorrect && 'text-emerald-900',
               isAnswered && selected && !correct && 'text-red-900'
            )}>
              {/* Remove the option prefix if present (A), (B), etc. */}
              {choice.replace(/^\([A-D]\)\s*/, '')}
            </span>

            {/* Status Icon */}
            <div className="ml-auto flex-shrink-0">
               {showCorrect && <CheckCircle className="w-5 h-5 text-emerald-600" />}
               {isAnswered && selected && !correct && <X className="w-5 h-5 text-red-600" />}
            </div>
          </button>
        );
      })}
    </div>
  );
};
