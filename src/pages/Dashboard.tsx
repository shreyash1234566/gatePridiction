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
    <div className="space-y-10 max-w-7xl mx-auto p-6 md:p-8 animate-fade-in">
      {/* Hero section - Open & Luminous */}
      <div className="text-center py-12 relative">
        <div className="relative z-10 animate-slide-up">
            <div className="inline-flex items-center gap-2.5 bg-white px-4 py-1.5 rounded-full border border-border mb-8 shadow-sm">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500"></span>
                </span>
                <span className="text-xs text-foreground font-bold uppercase tracking-widest font-mono">System Online</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-heading font-extrabold mb-6 tracking-tight text-foreground leading-tight">
               GATE <span className="text-primary">Flow</span>
            </h1>
            
            <p className="text-muted-foreground text-xl max-w-2xl mx-auto font-sans leading-relaxed font-light">
               Intelligent prediction and analysis engine.
               <br/>
               <span className="text-foreground font-medium">Predict. Practice. Perform.</span>
            </p>
        </div>
      </div>

      {/* Quick stats - Command Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 animate-slide-up [animation-delay:100ms]">
        {[
            { label: "Total Questions", value: GATE_DATA.meta.total_questions.toLocaleString(), icon: BookOpen, color: "text-primary", bg: "bg-primary/10", border: "border-t-primary" },
            { label: "Questions Attempted", value: progress.overall.totalAttempted, icon: Trophy, color: "text-secondary", bg: "bg-secondary/10", border: "border-t-secondary" },
            { label: "Accuracy Rate", value: `${progress.overall.accuracy.toFixed(1)}%`, icon: Target, color: "text-emerald-600", bg: "bg-emerald-100", border: "border-t-emerald-600" },
            { label: "Study Streak", value: "3 Days", icon: Flame, color: "text-orange-500", bg: "bg-orange-100", border: "border-t-orange-500" }
        ].map((stat, i) => (
            <Card key={i} className={`rounded-xl border border-border border-t-4 ${stat.border} bg-card shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group`}>
            <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                <div className={`p-3 rounded-lg ${stat.bg} ${stat.color} group-hover:scale-110 transition-transform duration-300`}>
                    <stat.icon className="h-6 w-6" />
                </div>
                <div>
                    <div className="text-2xl md:text-3xl font-bold font-mono text-foreground tracking-tight">{stat.value}</div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider font-bold mt-0.5">{stat.label}</div>
                </div>
                </div>
            </CardContent>
            </Card>
        ))}
      </div>

      {/* Quick actions - Clean Interactive Cards */}
      <div className="grid md:grid-cols-3 gap-6 animate-slide-up [animation-delay:200ms]">
        <Link to="/practice" className="block group">
          <Card className="h-full border border-border hover:border-primary/50 hover:shadow-lg transition-all duration-300 bg-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-xl text-foreground">
                <div className="p-2.5 rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-white transition-colors duration-300">
                   <BookOpen className="h-5 w-5" />
                </div>
                Start Practice
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-6 leading-relaxed">
                Practice PYQs from 2011-2025 with instant feedback and detailed solutions.
              </p>
              <Button className="w-full gap-2 bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/30 hover:shadow-primary/50 animate-[pulse_3s_infinite] group-hover:translate-x-1 transition-all">
                Begin Session <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </Link>
        <Link to="/predictions" className="block group">
          <Card className="h-full border border-border hover:border-secondary/50 hover:shadow-lg transition-all duration-300 bg-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-xl text-foreground">
                 <div className="p-2.5 rounded-lg bg-secondary/10 text-secondary-foreground group-hover:bg-secondary group-hover:text-white transition-colors duration-300">
                    <Target className="h-5 w-5" />
                 </div>
                2026 Predictions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-6 leading-relaxed">
                AI analysis revealing likely topics based on patterns.
              </p>
              <Button variant="secondary" className="w-full gap-2 bg-secondary text-secondary-foreground hover:bg-secondary/80 shadow-md group-hover:translate-x-1 transition-all">
                View Predictions <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </Link>
        <Link to="/trends" className="block group">
           <Card className="h-full border border-border hover:border-accent/50 hover:shadow-lg transition-all duration-300 bg-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-xl text-foreground">
                <div className="p-2.5 rounded-lg bg-accent/10 text-accent group-hover:bg-accent group-hover:text-white transition-colors duration-300">
                    <TrendingUp className="h-5 w-5" />
                </div>
                Trend Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-6 leading-relaxed">
                Deep dive into topic frequency and weightage.
              </p>
              <Button variant="outline" className="w-full gap-2 border-accent/20 text-accent hover:bg-accent/10 hover:text-accent-foreground shadow-sm group-hover:translate-x-1 transition-all">
                Explore Trends <ArrowRight className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        </Link>
      </div>

      {/* Rising topics highlight */}
      {risingTopics.length > 0 && (
        <Card className="border border-border bg-card animate-slide-up [animation-delay:300ms]">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg text-foreground">
              <TrendingUp className="h-5 w-5 text-secondary" />
              Rising Topics
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
                    variant="secondary" 
                    className="bg-yellow-50 text-yellow-800 border-yellow-200 hover:bg-yellow-100 cursor-pointer hover:scale-105 transition-all py-1.5 px-3"
                  >
                    {topic.topic}
                    <span className="ml-1.5 text-[10px] text-yellow-600/70 uppercase tracking-wider font-semibold">
                      {topic.subject.replace("Engineering ", "").replace("Computer ", "").substring(0, 3)}
                    </span>
                  </Badge>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Subject grid */}
      <div className="animate-slide-up [animation-delay:400ms]">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3 text-foreground">
          <Brain className="h-6 w-6 text-primary" />
          Subject Command Center
        </h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {subjects.map((subject, idx) => {
            const icon = subjectIcons[subject] || "📚";
            const stats = subjectStats[subject] || { total: 0, topics: 0 };
            const subjectProgress = getSubjectProgress(subject);
            
            return (
              <Link
                key={subject}
                to={`/practice?subject=${encodeURIComponent(subject)}`}
              >
                <Card className="subject-card h-full bg-card border border-border hover:border-primary/30 hover:shadow-md transition-all duration-300 group">
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-4 mb-4">
                      <span className="text-2xl p-3 bg-secondary/10 rounded-xl border border-border group-hover:scale-110 group-hover:border-primary/30 transition-all duration-300 shadow-sm block">{icon}</span>
                      <div className="flex-1 min-w-0 pt-1">
                        <h3 className="font-semibold text-base leading-tight truncate text-foreground group-hover:text-primary transition-colors">
                          {subject.replace("Engineering", "Eng.")}
                        </h3>
                        <p className="text-xs text-muted-foreground mt-1.5 font-medium">
                          {stats.total} questions • {stats.topics} topics
                        </p>
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-muted-foreground">Mastery</span>
                        <span className="font-bold text-primary">
                          {subjectProgress.percentage.toFixed(0)}%
                        </span>
                      </div>
                      <Progress value={subjectProgress.percentage} className="h-1.5 bg-secondary/20" indicatorClassName="bg-primary shadow-sm" />
                      
                      {subjectProgress.attempted > 0 && (
                        <p className="text-xs text-muted-foreground text-right">
                          <span className={subjectProgress.accuracy > 70 ? "text-green-600" : "text-yellow-600"}>
                             {subjectProgress.accuracy.toFixed(1)}% Accuracy
                          </span>
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
