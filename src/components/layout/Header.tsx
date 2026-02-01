import { Menu, Moon, Sun, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useProgress } from "@/hooks/useProgress";
import { GATE_DATA } from "@/data/gateData";

interface HeaderProps {
  toggleTheme?: () => void;
  isDarkMode?: boolean;
}

/**
 * Application header with branding, progress overview, and theme toggle
 * Research: Clean, minimal header reduces cognitive load (Sweller, 1988)
 */
export const Header = ({ toggleTheme, isDarkMode = true }: HeaderProps) => {
  const { progress } = useProgress();
  
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center px-4 gap-4">
        {/* Sidebar trigger */}
        <SidebarTrigger className="lg:hidden">
          <Menu className="h-5 w-5" />
        </SidebarTrigger>
        
        {/* Logo and branding */}
        <div className="flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-primary" />
          <div className="flex flex-col">
            <span className="font-semibold text-sm leading-none">GATE 2026</span>
            <span className="text-xs text-muted-foreground">CS Prep</span>
          </div>
        </div>
        
        {/* Progress summary - Hidden on mobile */}
        <div className="hidden md:flex items-center gap-6 ml-8">
          <div className="flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">Questions:</span>
            <span className="font-medium">
              {progress.overall.totalAttempted} / {GATE_DATA.meta.total_questions}
            </span>
          </div>
          
          {progress.overall.totalAttempted > 0 && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-muted-foreground">Accuracy:</span>
              <span className="font-medium text-success">
                {progress.overall.accuracy.toFixed(1)}%
              </span>
            </div>
          )}
          
          {progress.studyStreak > 0 && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-muted-foreground">Streak:</span>
              <span className="font-medium">🔥 {progress.studyStreak} days</span>
            </div>
          )}
        </div>
        
        {/* Spacer */}
        <div className="flex-1" />
        
        {/* Theme toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {isDarkMode ? (
            <Sun className="h-5 w-5" />
          ) : (
            <Moon className="h-5 w-5" />
          )}
        </Button>
      </div>
    </header>
  );
};
