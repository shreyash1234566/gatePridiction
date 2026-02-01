import { useMemo } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getAllQuestions, Question, subjectIcons } from "@/data/gateData";
import { Bookmark, BookmarkX, ArrowRight, Trash2 } from "lucide-react";
import { useState, useEffect } from "react";

/**
 * Bookmarks page showing saved questions
 * Uses localStorage for persistence
 */
const Bookmarks = () => {
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<number>>(new Set());
  
  // Load bookmarks from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('gate_bookmarks');
    if (saved) {
      try {
        const bookmarks = JSON.parse(saved);
        setBookmarkedIds(new Set(bookmarks));
      } catch (e) {
        console.error('Failed to load bookmarks:', e);
      }
    }
  }, []);

  // Get bookmarked questions
  const bookmarkedQuestions = useMemo(() => {
    const allQuestions = getAllQuestions();
    return allQuestions.filter(q => bookmarkedIds.has(q.id));
  }, [bookmarkedIds]);

  // Group by subject
  const groupedBySubject = useMemo(() => {
    const groups: { [subject: string]: Question[] } = {};
    bookmarkedQuestions.forEach(q => {
      if (!groups[q.subject]) {
        groups[q.subject] = [];
      }
      groups[q.subject].push(q);
    });
    return groups;
  }, [bookmarkedQuestions]);

  const removeBookmark = (id: number) => {
    setBookmarkedIds(prev => {
      const newSet = new Set(prev);
      newSet.delete(id);
      localStorage.setItem('gate_bookmarks', JSON.stringify([...newSet]));
      return newSet;
    });
  };

  const clearAllBookmarks = () => {
    if (window.confirm('Are you sure you want to clear all bookmarks?')) {
      setBookmarkedIds(new Set());
      localStorage.setItem('gate_bookmarks', '[]');
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Bookmark className="h-6 w-6 text-primary" />
            Bookmarked Questions
          </h1>
          <p className="text-muted-foreground text-sm mt-1">
            {bookmarkedQuestions.length} questions saved for review
          </p>
        </div>
        
        {bookmarkedQuestions.length > 0 && (
          <Button variant="outline" onClick={clearAllBookmarks} className="gap-2">
            <Trash2 className="h-4 w-4" />
            Clear All
          </Button>
        )}
      </div>

      {/* Empty state */}
      {bookmarkedQuestions.length === 0 && (
        <Card className="p-12 text-center">
          <BookmarkX className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="font-medium text-lg mb-2">No Bookmarks Yet</h3>
          <p className="text-muted-foreground mb-6">
            Bookmark questions during practice to review them later.
          </p>
          <Link to="/practice">
            <Button className="gap-2">
              Start Practicing <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </Card>
      )}

      {/* Grouped bookmarks */}
      {Object.entries(groupedBySubject).map(([subject, questions]) => (
        <Card key={subject}>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <span>{subjectIcons[subject] || "📚"}</span>
              {subject}
              <Badge variant="secondary" className="ml-2">
                {questions.length}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {questions.map((question) => (
                <div 
                  key={question.id}
                  className="p-4 rounded-lg bg-muted/50 border border-border"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="outline" className="text-xs">
                          {question.topic}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          GATE {question.year}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          {question.marks} mark{question.marks > 1 ? 's' : ''}
                        </Badge>
                      </div>
                      <p className="text-sm font-serif leading-relaxed line-clamp-3">
                        {question.question_text}
                      </p>
                    </div>
                    
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => removeBookmark(question.id)}
                      className="flex-shrink-0 text-destructive hover:text-destructive hover:bg-destructive/10"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                  
                  <div className="mt-3 flex items-center gap-2">
                    <Link
                      to={`/practice?subject=${encodeURIComponent(question.subject)}`}
                    >
                      <Button variant="outline" size="sm" className="gap-1">
                        Practice Topic <ArrowRight className="h-3 w-3" />
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default Bookmarks;
