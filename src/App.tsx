import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { MainLayout } from "@/components/layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import Practice from "./pages/Practice";
import Predictions from "./pages/Predictions";
import Trends from "./pages/Trends";
import Bookmarks from "./pages/Bookmarks";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

/**
 * GATE 2026 Study Application
 * Research-driven design for optimal learning efficiency
 * 
 * Research Citations:
 * - Mehta & Zhu (2009): Blue color scheme for cognitive focus
 * - Sweller (1988): Cognitive Load Theory - Single-task interface
 * - Dyson & Haselgrove (2001): Serif fonts for reading comprehension
 * - Nielsen Norman Group: F-pattern layout optimization
 */
const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <MainLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/practice" element={<Practice />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/trends" element={<Trends />} />
            <Route path="/bookmarks" element={<Bookmarks />} />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </MainLayout>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
