import { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from "recharts";
import { GATE_DATA, getAllSubjects, subjectIcons, subjectColors, getSubjectStats } from "@/data/gateData";
import { TrendingUp, BarChart3, PieChartIcon } from "lucide-react";

/**
 * Trend Analysis page with data visualizations
 * Research: Tufte's data-ink ratio and Cleveland & McGill position encoding
 * Color-blind friendly Okabe-Ito palette
 */
const Trends = () => {
  const [selectedSubject, setSelectedSubject] = useState<string>("Engineering Mathematics");
  const subjects = getAllSubjects();
  const subjectStats = getSubjectStats();

  // Get trends data for selected subject
  const trendData = useMemo(() => {
    const subjectTrends = GATE_DATA.trends[selectedSubject];
    if (!subjectTrends) return [];

    const years = GATE_DATA.meta.years_covered;
    const topics = Object.keys(subjectTrends);

    // Aggregate by year
    return years.map(year => {
      const yearData: { year: number; total: number; [key: string]: number } = { 
        year, 
        total: 0 
      };
      
      topics.forEach(topic => {
        const count = subjectTrends[topic][year.toString()] || 0;
        yearData[topic] = count;
        yearData.total += count;
      });
      
      return yearData;
    });
  }, [selectedSubject]);

  // Subject distribution for pie chart
  const subjectDistributionData = useMemo(() => {
    return subjects.map(subject => ({
      name: subject.replace("Engineering ", "").replace("Computer ", ""),
      fullName: subject,
      value: subjectStats[subject]?.total || 0,
      color: subjectColors[subject] || "hsl(0, 0%, 50%)",
    }));
  }, [subjects, subjectStats]);

  // Top topics for selected subject
  const topTopics = useMemo(() => {
    const subjectTrends = GATE_DATA.trends[selectedSubject];
    if (!subjectTrends) return [];

    return Object.entries(subjectTrends)
      .map(([topic, yearData]) => ({
        topic,
        total: Object.values(yearData).reduce((sum: number, val) => sum + (val as number), 0),
        recent: (yearData["2023"] || 0) + (yearData["2024"] || 0) + (yearData["2025"] || 0),
      }))
      .sort((a, b) => b.total - a.total)
      .slice(0, 10);
  }, [selectedSubject]);

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-popover border border-border rounded-lg p-3 shadow-lg">
          <p className="font-medium mb-1">GATE {label}</p>
          <p className="text-sm text-muted-foreground">
            Total: {payload[0]?.payload.total} questions
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <TrendingUp className="h-6 w-6 text-primary" />
          Trend Analysis
        </h1>
        <p className="text-muted-foreground text-sm mt-1">
          15-year topic frequency analysis (2011-2025)
        </p>
      </div>

      {/* Subject selector */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium">Select Subject:</label>
            <Select value={selectedSubject} onValueChange={setSelectedSubject}>
              <SelectTrigger className="w-64">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {subjects.map((subject) => (
                  <SelectItem key={subject} value={subject}>
                    {subjectIcons[subject]} {subject}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Main trend chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-primary" />
            Question Frequency Over Time - {selectedSubject}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid 
                  strokeDasharray="3 3" 
                  stroke="hsl(var(--border))"
                  opacity={0.5}
                />
                <XAxis 
                  dataKey="year" 
                  tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                  axisLine={{ stroke: 'hsl(var(--border))' }}
                />
                <YAxis 
                  tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                  axisLine={{ stroke: 'hsl(var(--border))' }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="total"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, fill: 'hsl(var(--primary))' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Top topics bar chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Top Topics - {selectedSubject}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart 
                  data={topTopics} 
                  layout="vertical"
                  margin={{ left: 100 }}
                >
                  <CartesianGrid 
                    strokeDasharray="3 3" 
                    stroke="hsl(var(--border))"
                    opacity={0.5}
                  />
                  <XAxis 
                    type="number"
                    tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }}
                  />
                  <YAxis 
                    type="category" 
                    dataKey="topic" 
                    tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }}
                    width={90}
                  />
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-popover border border-border rounded-lg p-3 shadow-lg">
                            <p className="font-medium">{data.topic}</p>
                            <p className="text-sm text-muted-foreground">
                              Total: {data.total} questions
                            </p>
                            <p className="text-sm text-muted-foreground">
                              Recent (2023-25): {data.recent}
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Bar 
                    dataKey="total" 
                    fill="hsl(var(--primary))"
                    radius={[0, 4, 4, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Subject distribution pie chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <PieChartIcon className="h-5 w-5" />
              Questions by Subject
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={subjectDistributionData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={({ name, percent }) => 
                      `${name} (${(percent * 100).toFixed(0)}%)`
                    }
                    labelLine={false}
                  >
                    {subjectDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload;
                        return (
                          <div className="bg-popover border border-border rounded-lg p-3 shadow-lg">
                            <p className="font-medium">{data.fullName}</p>
                            <p className="text-sm text-muted-foreground">
                              {data.value} questions
                            </p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent topics highlight */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            Recent High-Frequency Topics (2023-2025)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {topTopics
              .filter(t => t.recent > 0)
              .sort((a, b) => b.recent - a.recent)
              .map((topic, index) => (
                <Badge 
                  key={index} 
                  variant={topic.recent >= 3 ? "default" : "secondary"}
                  className="text-xs"
                >
                  {topic.topic} ({topic.recent})
                </Badge>
              ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Trends;
