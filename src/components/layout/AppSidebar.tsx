import { useLocation } from "react-router-dom";
import { 
  BookOpen, 
  TrendingUp, 
  Target, 
  BarChart3, 
  Bookmark,
  Home,
  GraduationCap,
  Map,
  Microscope
} from "lucide-react";
import { NavLink } from "@/components/NavLink";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
  useSidebar,
} from "@/components/ui/sidebar";
import { Progress } from "@/components/ui/progress";
import { useProgress } from "@/hooks/useProgress";
import { subjectIcons, getAllSubjects } from "@/data/gateData";

/**
 * Application sidebar with navigation and subject progress
 * Research: Miller's Law - Chunked into 7±2 navigation items
 */
export const AppSidebar = () => {
  const { state, toggleSidebar } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();
  const { progress, getSubjectProgress } = useProgress();
  const subjects = getAllSubjects();

  const mainNavItems = [
    { title: "Dashboard", url: "/", icon: Home },
    { title: "Practice", url: "/practice", icon: BookOpen },
    { title: "Roadmap", url: "/roadmap", icon: Map },
    { title: "Predictions", url: "/predictions", icon: Target },
    { title: "Micro-Topics", url: "/micro-topics", icon: Microscope },
    { title: "Trends", url: "/trends", icon: TrendingUp },
    { title: "Bookmarks", url: "/bookmarks", icon: Bookmark },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <Sidebar collapsible="offcanvas" className="border-r border-sidebar-border">
      <SidebarHeader className="border-b border-sidebar-border p-4">
        <button 
          onClick={toggleSidebar}
          className="flex items-center gap-3 w-full text-left hover:opacity-80 transition-opacity cursor-pointer"
          title="Click to hide sidebar (Ctrl+B)"
        >
          <GraduationCap className="h-8 w-8 text-primary shrink-0" />
          {!collapsed && (
            <div className="flex flex-col">
              <span className="font-semibold text-sidebar-foreground">GATE 2027</span>
              <span className="text-xs text-muted-foreground">Study Platform</span>
            </div>
          )}
        </button>
      </SidebarHeader>

      <SidebarContent className="px-2">
        {/* Main Navigation */}
        <SidebarGroup>
          <SidebarGroupLabel className="px-2 text-xs text-muted-foreground">
            Navigation
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {mainNavItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                    asChild
                    isActive={isActive(item.url)}
                    tooltip={item.title}
                  >
                    <NavLink 
                      to={item.url} 
                      className="flex items-center gap-3 px-3 py-2 rounded-md transition-colors"
                      activeClassName="bg-sidebar-accent text-sidebar-accent-foreground"
                    >
                      <item.icon className="h-4 w-4 shrink-0 text-sidebar-foreground" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        {/* Subject Progress - Only visible when expanded */}
        {!collapsed && (
          <SidebarGroup className="mt-4">
            <SidebarGroupLabel className="px-2 text-xs text-muted-foreground">
              Subjects Progress
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <div className="space-y-3 px-2">
                {subjects.slice(0, 6).map((subject) => {
                  const subjectProgress = getSubjectProgress(subject);
                  const icon = subjectIcons[subject] || "📚";
                  
                  return (
                    <NavLink
                      key={subject}
                      to={`/practice?subject=${encodeURIComponent(subject)}`}
                      className="block group"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2 text-sm">
                          <span>{icon}</span>
                          <span className="text-sidebar-foreground group-hover:text-primary transition-colors truncate max-w-[120px]">
                            {subject.replace("Engineering ", "").replace("Computer ", "")}
                          </span>
                        </div>
                        <span className="text-xs text-muted-foreground">
                          {subjectProgress.percentage.toFixed(0)}%
                        </span>
                      </div>
                      <Progress 
                        value={subjectProgress.percentage} 
                        className="h-1.5"
                      />
                    </NavLink>
                  );
                })}
                
                {/* View all link */}
                <NavLink
                  to="/practice"
                  className="text-xs text-primary hover:underline flex items-center gap-1 mt-2"
                >
                  View all {subjects.length} subjects →
                </NavLink>
              </div>
            </SidebarGroupContent>
          </SidebarGroup>
        )}
      </SidebarContent>

      <SidebarFooter className="border-t border-sidebar-border p-4">
        {!collapsed && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Overall Progress</span>
              <span className="font-medium">{progress.overall.percentage.toFixed(1)}%</span>
            </div>
            <Progress value={progress.overall.percentage} className="h-2" />
            <p className="text-xs text-muted-foreground">
              {progress.overall.totalAttempted} of {progress.overall.totalQuestions} questions attempted
            </p>
          </div>
        )}
      </SidebarFooter>
    </Sidebar>
  );
};
