import { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  getAllMicroTopicPredictions,
  getAllSubjects,
  subjectIcons,
  subjectColors,
  MicroTopicPrediction,
  getQuestionsByMicroTopic,
} from "@/data/gateData";
import {
  Microscope,
  TrendingUp,
  TrendingDown,
  Minus,
  Sparkles,
  Search,
  Filter,
  ArrowUpDown,
  Eye,
  ChevronDown,
  ChevronRight,
  BarChart3,
  Clock,
  Flame,
  AlertTriangle,
  Info,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

/**
 * Dedicated Micro-Topics Analysis Page
 * Shows granular sub-topic predictions with rich filtering, search, and analytics
 */
const MicroTopics = () => {
  const [selectedSubject, setSelectedSubject] = useState<string | undefined>();
  const [selectedTrend, setSelectedTrend] = useState<string | undefined>();
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"confidence" | "predicted" | "recency" | "appearances">("confidence");
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());
  const [viewMode, setViewMode] = useState<"table" | "cards">("table");
  const [confidenceFilter, setConfidenceFilter] = useState<"all" | "high" | "medium" | "low">("all");

  const subjects = getAllSubjects();
  const allMicroPredictions = useMemo(() => getAllMicroTopicPredictions(), []);

  // Advanced filtering
  const filteredPredictions = useMemo(() => {
    let filtered = [...allMicroPredictions];

    if (selectedSubject) {
      filtered = filtered.filter((m) => m.subject === selectedSubject);
    }

    if (selectedTrend) {
      filtered = filtered.filter((m) => m.trend === selectedTrend);
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (m) =>
          m.micro_topic.toLowerCase().includes(q) ||
          m.topic.toLowerCase().includes(q) ||
          m.subject.toLowerCase().includes(q)
      );
    }

    if (confidenceFilter !== "all") {
      filtered = filtered.filter((m) => {
        if (confidenceFilter === "high") return m.confidence >= 70;
        if (confidenceFilter === "medium") return m.confidence >= 40 && m.confidence < 70;
        return m.confidence < 40;
      });
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case "predicted":
          return b.predicted_count - a.predicted_count;
        case "recency":
          return b.last_seen - a.last_seen;
        case "appearances":
          return b.appearances - a.appearances;
        default:
          return b.confidence - a.confidence;
      }
    });

    return filtered;
  }, [allMicroPredictions, selectedSubject, selectedTrend, searchQuery, sortBy, confidenceFilter]);

  // Analytics
  const analytics = useMemo(() => {
    const all = allMicroPredictions;
    const bySubject: Record<string, MicroTopicPrediction[]> = {};
    const byTrend: Record<string, number> = { Rising: 0, Stable: 0, Declining: 0, Emerging: 0 };
    
    let highConf = 0;
    let recentlySeen = 0;

    all.forEach((m) => {
      if (!bySubject[m.subject]) bySubject[m.subject] = [];
      bySubject[m.subject].push(m);
      byTrend[m.trend] = (byTrend[m.trend] || 0) + 1;
      if (m.confidence >= 70) highConf++;
      if (m.last_seen >= 2025) recentlySeen++;
    });

    // Top micro-topics per subject (highest predicted_count)
    const topBySubject: Record<string, MicroTopicPrediction[]> = {};
    for (const [subj, micros] of Object.entries(bySubject)) {
      topBySubject[subj] = [...micros]
        .sort((a, b) => b.predicted_count - a.predicted_count)
        .slice(0, 3);
    }

    return { total: all.length, bySubject, byTrend, highConf, recentlySeen, topBySubject };
  }, [allMicroPredictions]);

  const toggleExpand = (key: string) => {
    setExpandedRows((prev) => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "Rising":
        return <TrendingUp className="h-3.5 w-3.5 text-green-500" />;
      case "Declining":
        return <TrendingDown className="h-3.5 w-3.5 text-orange-500" />;
      case "Emerging":
        return <Sparkles className="h-3.5 w-3.5 text-blue-500" />;
      default:
        return <Minus className="h-3.5 w-3.5 text-gray-400" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "Rising": return "bg-green-50 text-green-700 border-green-200";
      case "Declining": return "bg-orange-50 text-orange-700 border-orange-200";
      case "Emerging": return "bg-blue-50 text-blue-700 border-blue-200";
      default: return "bg-gray-50 text-gray-700 border-gray-200";
    }
  };

  const getConfidenceColor = (conf: number) => {
    if (conf >= 70) return "text-green-600";
    if (conf >= 50) return "text-blue-600";
    if (conf >= 30) return "text-yellow-600";
    return "text-gray-500";
  };

  const getConfidenceBarColor = (conf: number) => {
    if (conf >= 70) return "[&>div]:bg-green-500";
    if (conf >= 50) return "[&>div]:bg-blue-500";
    if (conf >= 30) return "[&>div]:bg-yellow-500";
    return "[&>div]:bg-gray-400";
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2.5">
            <Microscope className="h-6 w-6 text-purple-600" />
            Micro-Topic Analysis
          </h1>
          <p className="text-muted-foreground text-sm mt-1">
            Granular sub-topic predictions powered by weighted recency scoring (τ=3.0)
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={viewMode === "table" ? "default" : "outline"}
            size="sm"
            onClick={() => setViewMode("table")}
            className="gap-1.5"
          >
            <BarChart3 className="h-3.5 w-3.5" /> Table
          </Button>
          <Button
            variant={viewMode === "cards" ? "default" : "outline"}
            size="sm"
            onClick={() => setViewMode("cards")}
            className="gap-1.5"
          >
            <Eye className="h-3.5 w-3.5" /> Cards
          </Button>
        </div>
      </div>

      {/* Method info banner */}
      <Card className="bg-gradient-to-r from-purple-50 to-indigo-50 border-purple-200/50">
        <CardContent className="pt-5 pb-4">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 text-purple-600 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm font-medium text-purple-900">Weighted Recency Model (Backtested Winner)</p>
              <p className="text-xs text-purple-700/70 mt-1 leading-relaxed">
                Score = total_count × e<sup>−years_since/3.0</sup> • Backtested across 20 methods,
                268 groups, 6 holdout years • MAE: 0.3069 (−3.5% vs baseline) •
                {" "}{analytics.total} micro-topics analyzed across {Object.keys(analytics.bySubject).length} subjects
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <Card className="border-t-4 border-t-purple-500">
          <CardContent className="pt-5 pb-4">
            <div className="flex items-center gap-3">
              <Microscope className="h-5 w-5 text-purple-500" />
              <div>
                <p className="text-2xl font-bold font-mono">{analytics.total}</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">Micro-Topics</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-t-4 border-t-green-500">
          <CardContent className="pt-5 pb-4">
            <div className="flex items-center gap-3">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-2xl font-bold font-mono">{analytics.byTrend.Rising || 0}</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">Rising</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-t-4 border-t-blue-500">
          <CardContent className="pt-5 pb-4">
            <div className="flex items-center gap-3">
              <Zap className="h-5 w-5 text-blue-500" />
              <div>
                <p className="text-2xl font-bold font-mono">{analytics.highConf}</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">High Confidence</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-t-4 border-t-amber-500">
          <CardContent className="pt-5 pb-4">
            <div className="flex items-center gap-3">
              <Clock className="h-5 w-5 text-amber-500" />
              <div>
                <p className="text-2xl font-bold font-mono">{analytics.recentlySeen}</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">Seen in 2025+</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-t-4 border-t-orange-500">
          <CardContent className="pt-5 pb-4">
            <div className="flex items-center gap-3">
              <TrendingDown className="h-5 w-5 text-orange-500" />
              <div>
                <p className="text-2xl font-bold font-mono">{analytics.byTrend.Declining || 0}</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-bold">Declining</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top predictions by subject (horizontal scroll cards) */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center gap-2">
            <Flame className="h-4 w-4 text-orange-500" />
            Hottest Micro-Topics by Subject
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {subjects.map((subj) => {
              const tops = analytics.topBySubject[subj] || [];
              if (tops.length === 0) return null;
              return (
                <div key={subj} className="border rounded-lg p-3 bg-card hover:shadow-sm transition-shadow">
                  <div className="flex items-center gap-2 mb-2.5">
                    <span className="text-base">{subjectIcons[subj]}</span>
                    <span className="text-xs font-bold truncate">{subj.replace("Engineering ", "").replace("Computer ", "")}</span>
                  </div>
                  <div className="space-y-1.5">
                    {tops.map((m, i) => (
                      <div key={i} className="flex items-center justify-between gap-2">
                        <span className="text-[11px] text-muted-foreground truncate flex-1" title={m.micro_topic}>
                          {m.micro_topic.length > 30 ? m.micro_topic.substring(0, 30) + "…" : m.micro_topic}
                        </span>
                        <div className="flex items-center gap-1.5 flex-shrink-0">
                          {getTrendIcon(m.trend)}
                          <span className={cn("text-[11px] font-mono font-bold", getConfidenceColor(m.confidence))}>
                            {m.confidence.toFixed(0)}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center gap-2">
            <Filter className="h-4 w-4" />
            Filters & Search
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <div className="flex-1 min-w-[200px]">
              <label className="text-xs text-muted-foreground mb-1.5 block">Search</label>
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search micro-topics, topics, subjects..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 h-9"
                />
              </div>
            </div>
            <div className="w-44">
              <label className="text-xs text-muted-foreground mb-1.5 block">Subject</label>
              <Select
                value={selectedSubject || "all"}
                onValueChange={(v) => setSelectedSubject(v === "all" ? undefined : v)}
              >
                <SelectTrigger className="h-9">
                  <SelectValue placeholder="All Subjects" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Subjects</SelectItem>
                  {subjects.map((subject) => (
                    <SelectItem key={subject} value={subject}>
                      {subjectIcons[subject]} {subject.replace("Engineering ", "").replace("Computer ", "")}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="w-32">
              <label className="text-xs text-muted-foreground mb-1.5 block">Trend</label>
              <Select
                value={selectedTrend || "all"}
                onValueChange={(v) => setSelectedTrend(v === "all" ? undefined : v)}
              >
                <SelectTrigger className="h-9">
                  <SelectValue placeholder="All" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Trends</SelectItem>
                  <SelectItem value="Rising">📈 Rising</SelectItem>
                  <SelectItem value="Stable">➡️ Stable</SelectItem>
                  <SelectItem value="Declining">📉 Declining</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="w-36">
              <label className="text-xs text-muted-foreground mb-1.5 block">Confidence</label>
              <Select
                value={confidenceFilter}
                onValueChange={(v) => setConfidenceFilter(v as any)}
              >
                <SelectTrigger className="h-9">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Levels</SelectItem>
                  <SelectItem value="high">🟢 High (70%+)</SelectItem>
                  <SelectItem value="medium">🔵 Medium (40-70%)</SelectItem>
                  <SelectItem value="low">🟡 Low (&lt;40%)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-end">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const sorts: Array<typeof sortBy> = ["confidence", "predicted", "recency", "appearances"];
                  const idx = sorts.indexOf(sortBy);
                  setSortBy(sorts[(idx + 1) % sorts.length]);
                }}
                className="gap-1.5 h-9"
              >
                <ArrowUpDown className="h-3.5 w-3.5" />
                {sortBy === "confidence" && "Confidence"}
                {sortBy === "predicted" && "Predicted"}
                {sortBy === "recency" && "Recency"}
                {sortBy === "appearances" && "Appearances"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          Showing <span className="font-bold text-foreground">{filteredPredictions.length}</span> of {analytics.total} micro-topics
        </p>
        {(selectedSubject || selectedTrend || searchQuery || confidenceFilter !== "all") && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setSelectedSubject(undefined);
              setSelectedTrend(undefined);
              setSearchQuery("");
              setConfidenceFilter("all");
            }}
            className="text-xs text-muted-foreground"
          >
            Clear all filters
          </Button>
        )}
      </div>

      {/* Main content */}
      {viewMode === "table" ? (
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/30">
                    <TableHead className="w-[280px]">Micro-Topic</TableHead>
                    <TableHead className="w-[160px]">Parent Topic</TableHead>
                    <TableHead className="w-[120px]">Subject</TableHead>
                    <TableHead className="text-center w-[130px]">Confidence</TableHead>
                    <TableHead className="text-center w-[80px]">Predicted</TableHead>
                    <TableHead className="text-center w-[80px]">Trend</TableHead>
                    <TableHead className="text-center w-[70px]">Last Seen</TableHead>
                    <TableHead className="text-center w-[50px]">Freq</TableHead>
                    <TableHead className="text-right w-[80px]">Action</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPredictions.map((micro, index) => {
                    const rowKey = `${micro.subject}::${micro.topic}::${micro.micro_topic}`;
                    const isExpanded = expandedRows.has(rowKey);
                    const relatedQuestions = isExpanded
                      ? getQuestionsByMicroTopic(micro.subject, micro.topic, micro.micro_topic)
                      : [];

                    return (
                      <>
                        <TableRow
                          key={rowKey}
                          className={cn(
                            "cursor-pointer hover:bg-muted/50 transition-colors",
                            micro.confidence >= 70 && "bg-green-50/30",
                            micro.trend === "Rising" && "border-l-2 border-l-green-400"
                          )}
                          onClick={() => toggleExpand(rowKey)}
                        >
                          <TableCell>
                            <div className="flex items-center gap-2">
                              {isExpanded ? (
                                <ChevronDown className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                              ) : (
                                <ChevronRight className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                              )}
                              <span className="text-sm font-medium truncate max-w-[240px]" title={micro.micro_topic}>
                                {micro.micro_topic}
                              </span>
                            </div>
                          </TableCell>
                          <TableCell>
                            <span className="text-xs text-muted-foreground truncate max-w-[140px] inline-block" title={micro.topic}>
                              {micro.topic}
                            </span>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="text-[10px] whitespace-nowrap">
                              {subjectIcons[micro.subject]} {micro.subject.replace("Engineering ", "").replace("Computer ", "").substring(0, 12)}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2 justify-center">
                              <Progress
                                value={micro.confidence}
                                className={cn("h-2 w-14", getConfidenceBarColor(micro.confidence))}
                              />
                              <span className={cn("text-xs font-bold font-mono w-10", getConfidenceColor(micro.confidence))}>
                                {micro.confidence.toFixed(1)}%
                              </span>
                            </div>
                          </TableCell>
                          <TableCell className="text-center">
                            <span className="text-xs font-mono font-bold">
                              {micro.predicted_count.toFixed(2)}q
                            </span>
                          </TableCell>
                          <TableCell className="text-center">
                            <Badge variant="outline" className={cn("gap-1 text-[10px]", getTrendColor(micro.trend))}>
                              {getTrendIcon(micro.trend)}
                              {micro.trend}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-center text-xs text-muted-foreground font-mono">
                            {micro.last_seen}
                          </TableCell>
                          <TableCell className="text-center">
                            <span className="text-xs font-mono">{micro.appearances}×</span>
                          </TableCell>
                          <TableCell className="text-right">
                            <Link
                              to={`/practice?subject=${encodeURIComponent(micro.subject)}`}
                              onClick={(e) => e.stopPropagation()}
                            >
                              <Button variant="ghost" size="sm" className="h-7 text-xs">
                                Practice
                              </Button>
                            </Link>
                          </TableCell>
                        </TableRow>

                        {/* Expanded detail row */}
                        {isExpanded && (
                          <TableRow className="bg-muted/20">
                            <TableCell colSpan={9} className="p-4">
                              <div className="grid md:grid-cols-3 gap-4">
                                {/* Stats */}
                                <div className="space-y-2">
                                  <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Statistics</h4>
                                  <div className="grid grid-cols-2 gap-2 text-xs">
                                    <div className="bg-card p-2 rounded border">
                                      <span className="text-muted-foreground">Historical Avg</span>
                                      <p className="font-bold font-mono">{micro.historical_avg.toFixed(2)} q/year</p>
                                    </div>
                                    <div className="bg-card p-2 rounded border">
                                      <span className="text-muted-foreground">Recent Avg</span>
                                      <p className="font-bold font-mono">{micro.recent_avg.toFixed(2)} q/year</p>
                                    </div>
                                    <div className="bg-card p-2 rounded border">
                                      <span className="text-muted-foreground">Appearances</span>
                                      <p className="font-bold font-mono">{micro.appearances} years</p>
                                    </div>
                                    <div className="bg-card p-2 rounded border">
                                      <span className="text-muted-foreground">Last Seen</span>
                                      <p className="font-bold font-mono">{micro.last_seen}</p>
                                    </div>
                                  </div>
                                </div>

                                {/* Prediction breakdown */}
                                <div className="space-y-2">
                                  <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Prediction</h4>
                                  <div className="bg-card p-3 rounded border space-y-2">
                                    <div className="flex justify-between text-xs">
                                      <span className="text-muted-foreground">Predicted 2027</span>
                                      <span className="font-bold text-purple-600 font-mono">{micro.predicted_count.toFixed(3)} questions</span>
                                    </div>
                                    <div className="flex justify-between text-xs">
                                      <span className="text-muted-foreground">Confidence</span>
                                      <span className={cn("font-bold font-mono", getConfidenceColor(micro.confidence))}>{micro.confidence.toFixed(1)}%</span>
                                    </div>
                                    <div className="flex justify-between text-xs">
                                      <span className="text-muted-foreground">Trend</span>
                                      <Badge variant="outline" className={cn("text-[10px]", getTrendColor(micro.trend))}>
                                        {getTrendIcon(micro.trend)} {micro.trend}
                                      </Badge>
                                    </div>
                                    <div className="flex justify-between text-xs">
                                      <span className="text-muted-foreground">Change vs Avg</span>
                                      <span className={cn("font-bold font-mono", 
                                        micro.recent_avg > micro.historical_avg ? "text-green-600" : 
                                        micro.recent_avg < micro.historical_avg ? "text-orange-600" : "text-gray-500"
                                      )}>
                                        {micro.historical_avg > 0
                                          ? `${(((micro.recent_avg - micro.historical_avg) / micro.historical_avg) * 100).toFixed(0)}%`
                                          : "N/A"}
                                      </span>
                                    </div>
                                  </div>
                                </div>

                                {/* Related questions */}
                                <div className="space-y-2">
                                  <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                                    Related PYQs ({relatedQuestions.length})
                                  </h4>
                                  {relatedQuestions.length > 0 ? (
                                    <div className="space-y-1 max-h-[120px] overflow-y-auto">
                                      {relatedQuestions.slice(0, 5).map((q, i) => (
                                        <div key={i} className="bg-card p-2 rounded border text-xs">
                                          <div className="flex items-center justify-between gap-2">
                                            <Badge variant="outline" className="text-[10px]">
                                              {q.year}
                                            </Badge>
                                            <span className="text-muted-foreground">{q.marks}M • {q.question_type}</span>
                                          </div>
                                          <p className="text-muted-foreground mt-1 line-clamp-1">
                                            {q.question_text.substring(0, 80)}{q.question_text.length > 80 ? "…" : ""}
                                          </p>
                                        </div>
                                      ))}
                                      {relatedQuestions.length > 5 && (
                                        <p className="text-[10px] text-muted-foreground text-center">
                                          +{relatedQuestions.length - 5} more questions
                                        </p>
                                      )}
                                    </div>
                                  ) : (
                                    <div className="bg-card p-3 rounded border text-xs text-muted-foreground text-center">
                                      <AlertTriangle className="h-4 w-4 mx-auto mb-1 text-yellow-500" />
                                      No exact PYQ matches found
                                    </div>
                                  )}
                                </div>
                              </div>
                            </TableCell>
                          </TableRow>
                        )}
                      </>
                    );
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      ) : (
        /* Card view */
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {filteredPredictions.slice(0, 60).map((micro, index) => (
            <Card
              key={`${micro.subject}::${micro.topic}::${micro.micro_topic}-${index}`}
              className={cn(
                "hover:shadow-md transition-all duration-200 group",
                micro.confidence >= 70 && "border-l-4 border-l-green-400",
                micro.trend === "Rising" && micro.confidence < 70 && "border-l-4 border-l-blue-400"
              )}
            >
              <CardContent className="pt-4 pb-3">
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div className="min-w-0 flex-1">
                    <h3 className="text-sm font-bold truncate" title={micro.micro_topic}>
                      {micro.micro_topic}
                    </h3>
                    <p className="text-[11px] text-muted-foreground truncate mt-0.5">
                      {subjectIcons[micro.subject]} {micro.topic}
                    </p>
                  </div>
                  <Badge variant="outline" className={cn("text-[10px] flex-shrink-0", getTrendColor(micro.trend))}>
                    {getTrendIcon(micro.trend)} {micro.trend}
                  </Badge>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Confidence</span>
                    <span className={cn("font-bold font-mono", getConfidenceColor(micro.confidence))}>
                      {micro.confidence.toFixed(1)}%
                    </span>
                  </div>
                  <Progress
                    value={micro.confidence}
                    className={cn("h-1.5", getConfidenceBarColor(micro.confidence))}
                  />

                  <div className="grid grid-cols-3 gap-2 pt-1">
                    <div className="text-center">
                      <p className="text-[10px] text-muted-foreground">Predicted</p>
                      <p className="text-xs font-bold font-mono">{micro.predicted_count.toFixed(2)}q</p>
                    </div>
                    <div className="text-center">
                      <p className="text-[10px] text-muted-foreground">Recent</p>
                      <p className="text-xs font-bold font-mono">{micro.recent_avg.toFixed(1)}/yr</p>
                    </div>
                    <div className="text-center">
                      <p className="text-[10px] text-muted-foreground">Last</p>
                      <p className="text-xs font-bold font-mono">{micro.last_seen}</p>
                    </div>
                  </div>
                </div>

                <div className="mt-3 pt-2 border-t flex justify-between items-center">
                  <span className="text-[10px] text-muted-foreground">
                    {micro.appearances}× in {micro.appearances} years
                  </span>
                  <Link
                    to={`/practice?subject=${encodeURIComponent(micro.subject)}`}
                  >
                    <Button variant="ghost" size="sm" className="h-6 text-[10px] group-hover:text-primary">
                      Practice →
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
          {filteredPredictions.length > 60 && (
            <Card className="flex items-center justify-center bg-muted/30 border-dashed">
              <CardContent className="text-center py-6">
                <p className="text-sm text-muted-foreground">
                  +{filteredPredictions.length - 60} more micro-topics
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  Use table view to see all
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {filteredPredictions.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <Microscope className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
            <p className="text-muted-foreground">No micro-topics match your current filters.</p>
            <Button
              variant="outline"
              className="mt-3"
              onClick={() => {
                setSelectedSubject(undefined);
                setSelectedTrend(undefined);
                setSearchQuery("");
                setConfidenceFilter("all");
              }}
            >
              Clear Filters
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default MicroTopics;
