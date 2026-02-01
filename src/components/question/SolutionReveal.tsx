import { Question } from "@/data/gateData";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, XCircle, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface SolutionRevealProps {
  question: Question;
  isCorrect: boolean | null;
  selectedAnswer: string | null;
}

/**
 * Solution reveal component with progressive disclosure
 * Research: Nielsen Norman Group - Progressive disclosure reduces cognitive overload
 * Smooth animation (200ms) based on research on optimal transition timing
 */
export const SolutionReveal = ({
  question,
  isCorrect,
  selectedAnswer,
}: SolutionRevealProps) => {
  return (
    <Card className={cn(
      "mt-6 p-6 animate-slide-up border-l-4",
      isCorrect === true && "border-l-correct bg-correct/5",
      isCorrect === false && "border-l-incorrect bg-incorrect/5",
      isCorrect === null && "border-l-warning bg-warning/5"
    )}>
      {/* Result header */}
      <div className="flex items-center gap-3 mb-4">
        {isCorrect === true && (
          <>
            <CheckCircle2 className="h-6 w-6 text-correct" />
            <span className="font-semibold text-correct">Correct!</span>
          </>
        )}
        {isCorrect === false && (
          <>
            <XCircle className="h-6 w-6 text-incorrect" />
            <span className="font-semibold text-incorrect">Incorrect</span>
          </>
        )}
        {isCorrect === null && (
          <>
            <AlertCircle className="h-6 w-6 text-warning" />
            <span className="font-semibold text-warning">Answer Not Checked</span>
          </>
        )}
      </div>

      {/* Answer details */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <span className="text-muted-foreground text-sm">Your answer:</span>
          <Badge variant={isCorrect ? "default" : "destructive"} className="font-mono">
            {selectedAnswer || "Not selected"}
          </Badge>
        </div>
        
        <div className="flex items-center gap-2">
          <span className="text-muted-foreground text-sm">Correct answer:</span>
          <Badge className="bg-correct text-correct-foreground font-mono">
            {question.answer}
          </Badge>
        </div>
      </div>

      {/* Marks information */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex items-center gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Marks: </span>
            <span className="font-medium">
              {isCorrect ? `+${question.marks}` : isCorrect === false ? question.negative_marks : 0}
            </span>
          </div>
          <div>
            <span className="text-muted-foreground">Question Type: </span>
            <span className="font-medium">{question.question_type}</span>
          </div>
          <div>
            <span className="text-muted-foreground">Year: </span>
            <span className="font-medium">{question.year}</span>
          </div>
        </div>
      </div>

      {/* Study tip based on result */}
      {isCorrect === false && (
        <div className="mt-4 p-4 bg-muted/50 rounded-lg">
          <p className="text-sm text-muted-foreground">
            💡 <strong>Study Tip:</strong> Review the topic "{question.topic}" in {question.subject}. 
            This topic has appeared in GATE {question.year} and may appear again based on trend analysis.
          </p>
        </div>
      )}
    </Card>
  );
};
