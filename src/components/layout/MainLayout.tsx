import { ReactNode } from "react";
import { SidebarProvider, SidebarInset, SidebarTrigger, useSidebar } from "@/components/ui/sidebar";
import { AppSidebar } from "./AppSidebar";
import { Menu, PanelLeftClose, PanelLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

interface MainLayoutProps {
  children: ReactNode;
}

/**
 * Desktop toggle button for sidebar - only visible when sidebar is CLOSED
 */
const DesktopSidebarToggle = () => {
  const { open, toggleSidebar } = useSidebar();
  
  // Only show when sidebar is closed
  if (open) return null;
  
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleSidebar}
      className="fixed top-4 left-4 z-50 hidden lg:flex h-10 w-10 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-100 shadow-lg border border-slate-600 transition-all duration-300"
      title="Show Sidebar (Ctrl+B)"
    >
      <PanelLeft className="h-5 w-5" />
    </Button>
  );
};

/**
 * Main application layout with sidebar and content area
 * Research: F-pattern reading optimized layout (Nielsen Norman Group)
 * Maximum content width of 720px for optimal reading (45-75 characters)
 */
export const MainLayout = ({ children }: MainLayoutProps) => {
  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen flex w-full">
        <AppSidebar />
        <SidebarInset className="flex-1">
          {/* Desktop sidebar toggle - Always visible */}
          <DesktopSidebarToggle />
          
          {/* Mobile header with sidebar trigger */}
          <header className="sticky top-0 z-40 flex h-14 items-center gap-4 border-b border-border bg-background/95 backdrop-blur px-4 lg:hidden">
            <SidebarTrigger>
              <Menu className="h-5 w-5" />
            </SidebarTrigger>
            <span className="font-semibold">GATE 2027 Prep</span>
          </header>
          
          {/* Main content area */}
          <main className="flex-1 p-4 md:p-6 lg:p-8">
            {children}
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
};
