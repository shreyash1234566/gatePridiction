import React, { useState, useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
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
import { usePredictions } from "@/hooks/usePredictions";
import { subjectIcons, getAllSubjects, Prediction, getMicroTopicPredictions } from "@/data/gateData";
import { 
  Target, 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  Star,
  Filter,
  ArrowUpDown,
  Info,
  ChevronDown,
  ChevronRight
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";

/**
 * 2026 Predictions page with confidence-based topic recommendations
 * Research: Tufte's data-ink ratio - maximum data with minimal decoration
 */
const Predictions = () => {
  const [selectedSubject, setSelectedSubject] = useState<string | undefined>();
  const [selectedTrend, setSelectedTrend] = useState<"Rising" | "Stable" | "Declining" | undefined>();
  const [showCoreOnly, setShowCoreOnly] = useState(false);
  const [sortBy, setSortBy] = useState<"confidence" | "topic">("confidence");
  const [expandedTopics, setExpandedTopics] = useState<Set<string>>(new Set());

  const toggleExpand = (key: string) => {
    setExpandedTopics(prev => {
      const next = new Set(prev);
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.add(key);
      }
      return next;
    });
  };

  const subjects = getAllSubjects();

  const { 
    predictions, 
    subjectDistribution, 
    modelMetrics,
    corePredictions,
    risingTopics,
    highConfidenceTopics 
  } = usePredictions({
    subject: selectedSubject,
    trend: selectedTrend,
    onlyCore: showCoreOnly,
  });

  // Sort predictions
  const sortedPredictions = useMemo(() => {
    const sorted = [...predictions];
    if (sortBy === "confidence") {
      return sorted.sort((a, b) => b.confidence - a.confidence);
    }
    return sorted.sort((a, b) => a.topic.localeCompare(b.topic));
  }, [predictions, sortBy]);

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "Rising":
        return <TrendingUp className="h-4 w-4 text-success" />;
      case "Declining":
        return <TrendingDown className="h-4 w-4 text-warning" />;
      default:
        return <Minus className="h-4 w-4 text-muted-foreground" />;
    }
  };

  const getTrendBadgeClass = (trend: string) => {
    switch (trend) {
      case "Rising":
        return "trend-rising";
      case "Declining":
        return "trend-declining";
      default:
        return "trend-stable";
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Target className="h-6 w-6 text-primary" />
          GATE 2027 Predictions
        </h1>
        <p className="text-muted-foreground text-sm mt-1">
          AI-powered topic predictions based on 15 years of GATE analysis
        </p>
      </div>

      {/* Model accuracy info */}
      <Card className="bg-primary/5 border-primary/20">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 text-primary mt-0.5" />
            <div>
              <p className="text-sm font-medium">Prediction Model Accuracy</p>
              <p className="text-xs text-muted-foreground mt-1">
                R² Score: {(modelMetrics.R2 * 100).toFixed(1)}% • 
                Mean Absolute Error: {modelMetrics.MAE.toFixed(3)} • 
                Based on {highConfidenceTopics.length} high-confidence predictions
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Star className="h-5 w-5 text-primary" />
              <div>
                <p className="text-2xl font-bold">{corePredictions.length}</p>
                <p className="text-xs text-muted-foreground">Core Topics</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <TrendingUp className="h-5 w-5 text-success" />
              <div>
                <p className="text-2xl font-bold">{risingTopics.length}</p>
                <p className="text-xs text-muted-foreground">Rising Topics</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Target className="h-5 w-5 text-chart-2" />
              <div>
                <p className="text-2xl font-bold">{highConfidenceTopics.length}</p>
                <p className="text-xs text-muted-foreground">High Confidence</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <ArrowUpDown className="h-5 w-5 text-muted-foreground" />
              <div>
                <p className="text-2xl font-bold">{predictions.length}</p>
                <p className="text-xs text-muted-foreground">Total Predictions</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm flex items-center gap-2">
            <Filter className="h-4 w-4" />
            Filters
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <div className="w-48">
              <label className="text-xs text-muted-foreground mb-1.5 block">
                Subject
              </label>
              <Select
                value={selectedSubject || "all"}
                onValueChange={(v) => setSelectedSubject(v === "all" ? undefined : v)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Subjects" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Subjects</SelectItem>
                  {subjects.map((subject) => (
                    <SelectItem key={subject} value={subject}>
                      {subjectIcons[subject]} {subject}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="w-40">
              <label className="text-xs text-muted-foreground mb-1.5 block">
                Trend
              </label>
              <Select
                value={selectedTrend || "all"}
                onValueChange={(v) => setSelectedTrend(v === "all" ? undefined : v as any)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Trends" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Trends</SelectItem>
                  <SelectItem value="Rising">📈 Rising</SelectItem>
                  <SelectItem value="Stable">➡️ Stable</SelectItem>
                  <SelectItem value="Declining">📉 Declining</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-end gap-2">
              <Button
                variant={showCoreOnly ? "default" : "outline"}
                size="sm"
                onClick={() => setShowCoreOnly(!showCoreOnly)}
                className="gap-1"
              >
                <Star className="h-3 w-3" />
                Core Topics Only
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => setSortBy(sortBy === "confidence" ? "topic" : "confidence")}
                className="gap-1"
              >
                <ArrowUpDown className="h-3 w-3" />
                Sort by {sortBy === "confidence" ? "Topic" : "Confidence"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Predictions table */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            Topic Predictions ({sortedPredictions.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[200px]">Topic</TableHead>
                  <TableHead>Subject</TableHead>
                  <TableHead className="text-center">Confidence</TableHead>
                  <TableHead className="text-center">Trend</TableHead>
                  <TableHead className="text-center">Last Seen</TableHead>
                  <TableHead className="text-center">Appearances</TableHead>
                  <TableHead className="text-right">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sortedPredictions.map((prediction, index) => {
                  const expandKey = `${prediction.subject}::${prediction.topic}`;
                  const isExpanded = expandedTopics.has(expandKey);
                  const microPreds = isExpanded ? getMicroTopicPredictions(prediction.subject, prediction.topic) : [];
                  
                  return (
                    <React.Fragment key={`${prediction.subject}-${prediction.topic}-${index}`}>
                      <TableRow 
                        className="cursor-pointer hover:bg-muted/50"
                        onClick={() => toggleExpand(expandKey)}
                      >
                        <TableCell className="font-medium">
                          <div className="flex items-center gap-2">
                            {microPreds.length > 0 || !isExpanded ? (
                              isExpanded ? 
                                <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" /> : 
                                <ChevronRight className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                            ) : (
                              <ChevronRight className="h-4 w-4 text-muted-foreground flex-shrink-0 opacity-30" />
                            )}
                            {prediction.is_core === "✓" && (
                              <Star className="h-4 w-4 text-primary flex-shrink-0" />
                            )}
                            <span className="truncate max-w-[180px]">
                              {prediction.topic}
                            </span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="text-xs whitespace-nowrap">
                            {subjectIcons[prediction.subject]} {prediction.subject.replace("Engineering ", "").replace("Computer ", "")}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <Progress 
                              value={prediction.confidence} 
                              className="h-2 w-16"
                            />
                            <span className="text-xs font-medium w-10">
                              {prediction.confidence.toFixed(1)}%
                            </span>
                          </div>
                        </TableCell>
                        <TableCell className="text-center">
                          <Badge 
                            variant="outline" 
                            className={cn("gap-1", getTrendBadgeClass(prediction.trend))}
                          >
                            {getTrendIcon(prediction.trend)}
                            {prediction.trend}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-center text-sm">
                          {prediction.last_seen}
                        </TableCell>
                        <TableCell className="text-center text-sm">
                          {prediction.appearances}x
                        </TableCell>
                        <TableCell className="text-right">
                          <Link
                            to={`/practice?subject=${encodeURIComponent(prediction.subject)}`}
                            onClick={(e) => e.stopPropagation()}
                          >
                            <Button variant="ghost" size="sm">
                              Practice
                            </Button>
                          </Link>
                        </TableCell>
                      </TableRow>
                      
                      {/* Micro-topic sub-rows */}
                      {isExpanded && microPreds.map((micro, mIdx) => (
                        <TableRow 
                          key={`micro-${prediction.subject}-${prediction.topic}-${micro.micro_topic}-${mIdx}`}
                          className="bg-muted/30 border-l-2 border-l-primary/20"
                        >
                          <TableCell className="pl-12 text-sm text-muted-foreground">
                            <span className="truncate max-w-[160px] inline-block">
                              🔬 {micro.micro_topic}
                            </span>
                          </TableCell>
                          <TableCell>
                            <span className="text-xs text-muted-foreground">
                              {micro.predicted_count.toFixed(2)}q
                            </span>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              <Progress 
                                value={micro.confidence} 
                                className="h-1.5 w-12"
                              />
                              <span className="text-xs text-muted-foreground w-10">
                                {micro.confidence.toFixed(0)}%
                              </span>
                            </div>
                          </TableCell>
                          <TableCell className="text-center">
                            <span className="text-xs">
                              {getTrendIcon(micro.trend)}
                            </span>
                          </TableCell>
                          <TableCell className="text-center text-xs text-muted-foreground">
                            {micro.last_seen}
                          </TableCell>
                          <TableCell className="text-center text-xs text-muted-foreground">
                            {micro.appearances}x
                          </TableCell>
                          <TableCell />
                        </TableRow>
                      ))}
                      
                      {isExpanded && microPreds.length === 0 && (
                        <TableRow className="bg-muted/20">
                          <TableCell colSpan={7} className="pl-12 text-xs text-muted-foreground italic">
                            No micro-topic predictions available for this topic
                          </TableCell>
                        </TableRow>
                      )}
                    </React.Fragment>
                  );
                })}
              </TableBody>
            </Table>
          </div>
          
          {sortedPredictions.length === 0 && (
            <p className="text-center text-muted-foreground py-8">
              No predictions match your filters.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Predictions;
