import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  BookOpen, 
  Target, 
  TrendingUp, 
  Trophy,
  ArrowRight,
  Brain,
  Flame,
  BarChart3
} from "lucide-react";
import { 
  GATE_DATA, 
  getAllSubjects, 
  subjectIcons, 
  getSubjectStats 
} from "@/data/gateData";
import { useProgress } from "@/hooks/useProgress";
import { usePredictions } from "@/hooks/usePredictions";

/**
 * Dashboard / Home page with subject overview and quick actions
 * Research: F-pattern reading layout (Nielsen Norman Group)
 * Card-based UI for visual chunking (Gestalt principles)
 */
const Dashboard = () => {
  const { progress, getSubjectProgress } = useProgress();
  const { risingTopics, corePredictions } = usePredictions();
  const subjects = getAllSubjects();
  const subjectStats = getSubjectStats();

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Hero section */}
      <div className="text-center py-8">
        <h1 className="text-3xl md:text-4xl font-bold mb-3">
          GATE 2026 <span className="text-primary">Preparation</span>
        </h1>
        <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
          Master {GATE_DATA.meta.total_questions.toLocaleString()} Previous Year Questions across 12 subjects 
          with AI-powered predictions and trend analysis.
        </p>
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="subject-card">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/10">
                <BookOpen className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-2xl font-bold">{GATE_DATA.meta.total_questions}</p>
                <p className="text-xs text-muted-foreground">Total Questions</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="subject-card">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-success/10">
                <Trophy className="h-5 w-5 text-success" />
              </div>
              <div>
                <p className="text-2xl font-bold">{progress.overall.totalAttempted}</p>
                <p className="text-xs text-muted-foreground">Attempted</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="subject-card">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-chart-2/10">
                <BarChart3 className="h-5 w-5 text-chart-2" />
              </div>
              <div>
                <p className="text-2xl font-bold">
                  {progress.overall.accuracy.toFixed(1)}%
                </p>
                <p className="text-xs text-muted-foreground">Accuracy</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="subject-card">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-warning/10">
                <Flame className="h-5 w-5 text-warning" />
              </div>
              <div>
                <p className="text-2xl font-bold">{progress.studyStreak}</p>
                <p className="text-xs text-muted-foreground">Day Streak</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick actions */}
      <div className="grid md:grid-cols-3 gap-4">
        <Link to="/practice" className="block">
          <Card className="subject-card h-full hover:border-primary/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <BookOpen className="h-5 w-5 text-primary" />
                Start Practice
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Practice PYQs from 2011-2025 with instant feedback
              </p>
              <Button className="w-full gap-2">
                Begin <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </Link>

        <Link to="/predictions" className="block">
          <Card className="subject-card h-full hover:border-primary/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Target className="h-5 w-5 text-primary" />
                2026 Predictions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                AI-powered predictions with {corePredictions.length} core topics
              </p>
              <Button variant="secondary" className="w-full gap-2">
                View Predictions <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </Link>

        <Link to="/trends" className="block">
          <Card className="subject-card h-full hover:border-primary/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <TrendingUp className="h-5 w-5 text-primary" />
                Trend Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                15-year topic frequency analysis and patterns
              </p>
              <Button variant="secondary" className="w-full gap-2">
                Explore Trends <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </Link>
      </div>

      {/* Rising topics highlight */}
      {risingTopics.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <TrendingUp className="h-5 w-5 text-success" />
              Rising Topics - Focus Areas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {risingTopics.slice(0, 10).map((topic, index) => (
                <Link
                  key={index}
                  to={`/practice?subject=${encodeURIComponent(topic.subject)}`}
                >
                  <Badge 
                    variant="outline" 
                    className="trend-rising cursor-pointer hover:scale-105 transition-transform"
                  >
                    {topic.topic}
                    <span className="ml-1 text-xs opacity-70">
                      ({topic.subject.replace("Engineering ", "").replace("Computer ", "")})
                    </span>
                  </Badge>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Subject grid */}
      <div>
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          All Subjects
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {subjects.map((subject) => {
            const icon = subjectIcons[subject] || "📚";
            const stats = subjectStats[subject] || { total: 0, topics: 0 };
            const subjectProgress = getSubjectProgress(subject);
            
            return (
              <Link
                key={subject}
                to={`/practice?subject=${encodeURIComponent(subject)}`}
              >
                <Card className="subject-card h-full hover:border-primary/50 transition-colors cursor-pointer">
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-3 mb-4">
                      <span className="text-2xl">{icon}</span>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-sm leading-tight truncate">
                          {subject}
                        </h3>
                        <p className="text-xs text-muted-foreground mt-1">
                          {stats.total} questions • {stats.topics} topics
                        </p>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-muted-foreground">Progress</span>
                        <span className="font-medium">
                          {subjectProgress.percentage.toFixed(0)}%
                        </span>
                      </div>
                      <Progress value={subjectProgress.percentage} className="h-1.5" />
                      
                      {subjectProgress.attempted > 0 && (
                        <p className="text-xs text-muted-foreground">
                          Accuracy: {subjectProgress.accuracy.toFixed(1)}%
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
