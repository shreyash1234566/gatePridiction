import React, { useState, useEffect } from "react";
import { Map, Clock, CalendarDays, TrendingUp, AlertTriangle, Target, BookOpen, RefreshCw, CheckCircle2, Brain, Zap, CheckCircle } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { useAdaptiveSchedule } from "@/hooks/useAdaptiveSchedule";

// Constants — Data-driven roadmap from elite prediction outputs and trend analysis.
// Focus: subject ROI, high-confidence micro-topics, and 620-safe / 700-push score tracks.
const subjects = [
  { name: 'General Aptitude', qs: 11, conf: 63.6, tier: 1, color: 'bg-emerald-500', tc: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20', time: 'Daily 15min + Phase build', topics: 'Verbal Ability (75.5% ↓), Quantitative Aptitude, Logical Reasoning · Target: 13–14/15 marks', phase: 'All phases' },
  { name: 'Engineering Mathematics', qs: 9, conf: 66.7, tier: 1, color: 'bg-emerald-500', tc: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20', time: 'Phase 1 main focus', topics: 'Linear Algebra ↑(80.3%), Probability ↑(78%), Calculus (76.8%), Graphs (80.4%) · Target: 11–12/~15', phase: 'Mar–May' },
  { name: 'Data Structures', qs: 7, conf: 71.5, tier: 1, color: 'bg-emerald-500', tc: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20', time: 'Phase 1–2', topics: 'BSTs (79.5%), Heaps (80.6%), Trees (78.3%), Hashing (76.4%), Linked Lists (78.6%) · Target: 7–8/~14', phase: 'May–Jul' },
  { name: 'Operating Systems', qs: 6, conf: 67.0, tier: 2, color: 'bg-blue-500', tc: 'text-blue-500 bg-blue-500/10 border-blue-500/20', time: 'Phase 3', topics: 'CPU Sched (82.8%), Proc Sync (81.6%), Deadlock (79.4%), Mem Mgmt (76.1%) · Target: 9–10/~12', phase: 'Aug–Sep' },
  { name: 'Computer Organization', qs: 6, conf: 65.8, tier: 2, color: 'bg-blue-500', tc: 'text-blue-500 bg-blue-500/10 border-blue-500/20', time: 'Phase 3', topics: 'Cache Memory (80.2%), Pipelining (79.5%), I/O · Predicted perfectly in 2026 · Target: 7–8/~12', phase: 'Aug–Sep' },
  { name: 'Theory of Computation', qs: 5, conf: 63.6, tier: 3, color: 'bg-purple-500', tc: 'text-purple-500 bg-purple-500/10 border-purple-500/20', time: 'Phase 4', topics: 'Finite Automata (81.8%), Regular Languages (79.2%), CFG · Selective: skip advanced Turing', phase: 'Oct' },
  { name: 'Computer Networks', qs: 5, conf: 62.3, tier: 3, color: 'bg-purple-500', tc: 'text-purple-500 bg-purple-500/10 border-purple-500/20', time: 'Phase 4 (selective)', topics: 'TCP/IP, Routing, Subnetting — NAT questions only (+EV, no neg marking)', phase: 'Nov' },
  { name: 'Algorithms', qs: 4, conf: 70.2, tier: 2, color: 'bg-blue-500', tc: 'text-blue-500 bg-blue-500/10 border-blue-500/20', time: 'Phase 2', topics: 'Asymptotic (83.8% #1), MST ↑(81.1%), Sorting (75.3% ↓), Graph Algos · Target: 5–6/~7', phase: 'Jun–Jul' },
  { name: 'Databases', qs: 4, conf: 66.6, tier: 3, color: 'bg-purple-500', tc: 'text-purple-500 bg-purple-500/10 border-purple-500/20', time: 'Phase 4', topics: 'Normalization ↑(81.7%), Concurrency (79.6%), RA (77.1%), SQL (76.7%), Indexing (77.9%)', phase: 'Oct–Nov' },
  { name: 'Digital Logic', qs: 3, conf: 66.6, tier: 4, color: 'bg-amber-500', tc: 'text-amber-500 bg-amber-500/10 border-amber-500/20', time: 'Phase 4 light', topics: 'Boolean Algebra ↑(79.4%), K-maps, Combinational circuits · Light coverage only', phase: 'Nov' },
  { name: 'Compiler Design', qs: 3, conf: 63.3, tier: 4, color: 'bg-amber-500', tc: 'text-amber-500 bg-amber-500/10 border-amber-500/20', time: 'Phase 4 light', topics: 'Parsing (82.2%), SDT ↑(78.1%) — focus ONLY these 2 high-conf topics', phase: 'Nov' },
  { name: 'Programming', qs: 2, conf: 69.8, tier: 4, color: 'bg-rose-500', tc: 'text-rose-500 bg-rose-500/10 border-rose-500/20', time: 'Phase 2 light', topics: 'Recursion (76.2%) only. NAT questions only — zero neg marking. Skip MCQs.', phase: 'Jul' },
];

const months = [
  { name: 'MAR', phase: 'P1', subj: 'Engg Math\nLinear Algebra', color: 'text-emerald-500', bg: 'bg-emerald-500/10 border-emerald-500' },
  { name: 'APR', phase: 'P1', subj: 'Probability\nCalculus', color: 'text-emerald-500', bg: 'bg-emerald-500/5 text-emerald-500 border-emerald-500/50' },
  { name: 'MAY', phase: 'P1', subj: 'DS Basics\nTrees + Lists', color: 'text-emerald-500', bg: 'bg-emerald-500/5 text-emerald-500 border-emerald-500/50' },
  { name: 'JUN', phase: 'P2', subj: 'Algorithms\nMST + Sorting', color: 'text-blue-500', bg: 'bg-blue-500/10 text-blue-500 border-blue-500' },
  { name: 'JUL', phase: 'P2', subj: 'BSTs, Heaps\nHashing', color: 'text-blue-500', bg: 'bg-blue-500/5 text-blue-500 border-blue-500/50' },
  { name: 'AUG', phase: 'P3', subj: 'OS: Scheduling\nSync + Deadlock', color: 'text-amber-500', bg: 'bg-amber-500/10 text-amber-500 border-amber-500' },
  { name: 'SEP', phase: 'P3', subj: 'CO: Cache\nPipelining', color: 'text-amber-500', bg: 'bg-amber-500/5 text-amber-500 border-amber-500/50' },
  { name: 'OCT', phase: 'P4', subj: 'ToC + DBs\nNormalization', color: 'text-purple-500', bg: 'bg-purple-500/10 text-purple-500 border-purple-500' },
  { name: 'NOV', phase: 'P4', subj: 'CD + DL\nNetworks', color: 'text-purple-500', bg: 'bg-purple-500/5 text-purple-500 border-purple-500/50' },
  { name: 'DEC', phase: 'P5', subj: 'Full Revision\nMock Tests', color: 'text-rose-500', bg: 'bg-rose-500/10 text-rose-500 border-rose-500' },
  { name: 'JAN', phase: 'P5', subj: 'PYQ Solve\nWeak Topics', color: 'text-rose-500', bg: 'bg-rose-500/5 text-rose-500 border-rose-500/50' },
  { name: 'FEB', phase: 'P6', subj: '🎯 EXAM\nSprint', color: 'text-amber-400', bg: 'bg-amber-400/20 text-amber-400 border-amber-400' },
];

const monthDetails = [
  'MAR — Linear Algebra (Rising ↑ 80.3%, recent avg 2.88→4.33 Qs). Eigenvalues, rank, matrix ops, determinants. Highest-ROI single topic — could swing 6–8 marks. GA daily starts now.',
  'APR — Probability (Rising ↑ 78%): Bayes, conditional, distributions, expectation. Calculus (76.8%): limits, differentiation, integration for CS. Graphs (80.4%): coloring, Euler, representations.',
  'MAY — DS Foundation: Trees (78.3%), Linked Lists (78.6%), Stacks, Queues. Build structural intuition before Phase 2 advanced DS. Combined Engg Math + DS mock: target 16+/27.',
  'JUN — Algorithms core: Asymptotic Analysis (83.8% — HIGHEST confidence in entire model). MST (Rising ↑ 81.1%, recent avg 1.77→2.33). Master Theorem, recurrences. PYQ every Friday.',
  'JUL — Advanced DS: BSTs (79.5%), Heaps (80.6%), Hashing (76.4%). Sorting (75.3% Declining). Recursion/Programming (76.2%) — NAT only. First full-paper mock: target 35–40 marks.',
  'AUG — OS: CPU Scheduling (82.8%), Process Sync (81.6%) — these 2 cover most OS questions. Deadlock (79.4%): detection, Banker\'s. Start CO: Cache Memory (80.2%). Target: 9–10 marks from OS.',
  'SEP — CO: Pipelining (79.5%), I/O. OS: Memory Mgmt (76.1%): paging, segmentation, TLB. Model predicted OS & CO with ~0 error in 2026. OS+CO mock: target 17+/22.',
  'OCT — ToC: Finite Automata (81.8%), Regular Languages (79.2%) — focus these 2, skip Turing. DB: Normalization (Rising ↑ 81.7%), Concurrency (79.6%), SQL (76.7%), RA (77.1%), Indexing (77.9%).',
  'NOV — CD: Parsing (82.2%), SDT (Rising ↑ 78.1%) — only these 2 topics. DL: Boolean Algebra (Rising ↑ 79.4%), K-maps. CN: TCP/IP, routing selective. NAT-only strategy for CN.',
  'DEC — Full revision: Tier 1 (Engg Math + DS) → Tier 2 (OS + CO + Algo). 3 mock tests/week × 4 weeks = 12 mocks. Error analysis every mock. Target ladder: 52→56→60 (620-safe entry).',
  'JAN — PYQ blitz by subject (10+ years). Weak topic sprint. GA master: must score 13+/15 consistently. Rising topics polish. Full mocks averaging 60+ (620-safe) and best mocks 63+ (700-push). NAT strategy locked.',
  '🎯 FEB EXAM MONTH. NO new topics. Formula sheets only. 1 mock/week max. Sleep 8+ hours. Strategy: GA first (13+/15) → NATs (all, +EV) → 2-mark MCQs (eliminate 2 options) → 1-mark MCQs. Execute 620-safe baseline, push to 700 only on high-confidence questions.',
];

const milestonesData = [
  { id: 'm1', date: 'Mar 1, 2026', title: 'LAUNCH DAY — Phase 1 Begins', desc: 'Set up your study log, formula book, and error diary. First session: Linear Algebra Chapter 1.', items: ['Formula book ready','Study log created','Daily GA habit starts'], type: 'active', badge: '🚀 START', btc: 'text-emerald-500 border-emerald-500 bg-emerald-500/10' },
  { id: 'm2', date: 'Mar 31, 2026', title: 'Linear Algebra Mastery Check', desc: 'Complete all Linear Algebra PYQs from 2010–2026. Score at least 70%. This is the highest-ROI single topic in 2027.', items: ['Eigenvalues ✓','Matrix rank ✓','Systems of eq ✓','PYQ score >70%'], badge: '📐 MATH', btc: 'text-emerald-500 border-emerald-500 bg-emerald-500/10' },
  { id: 'm3', date: 'Apr 30, 2026', title: 'Engg Math Complete', desc: 'Probability + Calculus + Graphs done. All Engg Math PYQs solved. Target: 9+/15 on Engg Math section mocks.', items: ['Probability (Rising) done','Calculus done','Section mock: 9+/15'], badge: '✓ PHASE 1A', btc: 'text-emerald-500 border-emerald-500 bg-emerald-500/10' },
  { id: 'm4', date: 'May 31, 2026', title: 'Data Structures Foundation Done', desc: 'DS basics complete. Move to Phase 2. Run a combined Engg Math + DS mock: target 16/27 marks.', items: ['Trees & Heaps done','Linked Lists done','Combined mock: 16+/27'], badge: '✓ PHASE 1', btc: 'text-emerald-500 border-emerald-500 bg-emerald-500/10' },
  { id: 'm5', date: 'Jun 30, 2026', title: 'Algorithms Core Complete', desc: 'Asymptotic Analysis (83.8% conf) fully mastered. MST Rising trend prepared. All sorting algorithms with analysis.', items: ['Asymptotic Analysis mastered','MST: Kruskal + Prim','Sorting: complete'], badge: '✓ ALGO', btc: 'text-blue-500 border-blue-500 bg-blue-500/10' },
  { id: 'm6', date: 'Jul 31, 2026', title: 'Phase 2 Complete — First Full Section Mock', desc: 'Run first full-paper mock test. Target: 35–40 marks (benchmark). Identify top 3 weak subjects. Log everything.', items: ['BSTs + Heaps + Hashing done','First full mock: 35–40 marks','Top 3 weak subjects identified'], badge: '📊 MOCK 1', btc: 'text-blue-500 border-blue-500 bg-blue-500/10' },
  { id: 'm7', date: 'Sep 1, 2026', title: 'OS + CO Phase Complete', desc: 'OS and CO are the two subjects the model predicted perfectly in 2026. They should be locked in. Target: 17+/22 on OS+CO mock.', items: ['CPU Scheduling mastered','Cache Memory mastered','OS+CO mock: 17+/22'], badge: '✓ SYSTEMS', btc: 'text-amber-500 border-amber-500 bg-amber-500/10' },
  { id: 'm8', date: 'Nov 30, 2026', title: 'Full Syllabus Complete — Phase 4 End', desc: 'All 12 subjects covered. Breadth phase done. Full paper mock target: 48–52 marks. Shift to revision mode now.', items: ['ToC + DBs done','CD + DL done','Full mock: 48–52 marks','GA: 12+/15 in mocks'], badge: '✓ ALL SUBJECTS', btc: 'text-purple-500 border-purple-500 bg-purple-500/10' },
  { id: 'm9', date: 'Dec 31, 2026', title: 'Revision Phase 1 Complete', desc: 'P1 + P2 subjects fully revised. Mock test scores improving. Target: 52–56 marks on full mocks by end of December.', items: ['Engg Math revised','DS + Algo revised','Mock target: 52–56 marks'], badge: '📈 IMPROVING', btc: 'text-rose-500 border-rose-500 bg-rose-500/10' },
  { id: 'm10', date: 'Jan 31, 2027', title: '620 SAFE LOCKED', desc: '3 full-paper mocks averaging 60+ marks. GA consistently scoring 13+/15. NAT discipline and error log locked for the final phase.', items: ['Mock avg: 60+ marks','GA: 13+/15 consistent','Error rate: falling each week','NAT strategy: locked'], badge: '✅ 620 SAFE', btc: 'text-rose-500 border-rose-500 bg-rose-500/10' },
  { id: 'm11', date: 'Feb 2027', title: '700 PUSH WINDOW', desc: 'GA first → NAT questions → 2-mark MCQs → 1-mark MCQs. Stretch goal for top attempts: 63–68 raw marks with disciplined risk control.', items: ['GA strategy: 13+/15','NAT: attempt all','2-mark focus: OS, Algo, Math','Target raw: 63–68 (700 push)'], badge: '🎓 EXAM', btc: 'text-amber-400 border-amber-400 bg-amber-400/20' },
];

const days = ['MON', 'TUE', 'WED', 'THU', 'FRI'];

// Weekly Timetable — Topics assigned by ML confidence ranking (Section 6) and Tier priority (Section 7)
// Color Key: c-green=Rising/Review, c-blue=Core study, c-amber=Secondary/GA, c-red=PYQ, c-purple=Mock, c-gray=Analysis
const ttData: Record<string, string[][][]> = {
  // ═══════════════════════════════════════════════════════════════════════════════
  // PHASE 1: FOUNDATION (Mar–May) — Tier 1: Engg Math (9Qs, ~15m) + DS Basics (7Qs, ~14m)
  // Target from this phase: Engg Math 11–12 marks + DS foundation for Phase 2
  // ═══════════════════════════════════════════════════════════════════════════════
  "1": [
    [['Warm-up','Linear Algebra recall','c-green','mins-green'],['Warm-up','Probability recall','c-green','mins-green'],['Warm-up','Calculus formulas','c-green','mins-green'],['Warm-up','Graph Theory recall','c-green','mins-green'],['Warm-up','Full week recall test','c-green','mins-green']],
    [['Linear Algebra ↑(80.3%)','Eigenvalues, rank, matrix ops','c-green','mins-green'],['Probability ↑(78.0%)','Conditional, Bayes, distributions','c-green','mins-green'],['Calculus (76.8%)','Limits, derivatives, integration','c-blue','mins-blue'],['Graphs (80.4%)','Coloring, Euler, representations','c-blue','mins-blue'],['Section Mock','Engg Math timed; target 9+/15','c-purple','mins-gray']],
    [['GA: Verbal (75.5%)','Reading comprehension, vocab','c-amber','mins-amber'],['GA: Quantitative','Arithmetic, algebra, geometry','c-amber','mins-amber'],['GA: Verbal + Quant','Mixed practice set','c-amber','mins-amber'],['GA: Logical','Arrangements, puzzles','c-amber','mins-amber'],['GA: Timed Test','Exam-condition 15min GA','c-amber','mins-amber']],
    [['PYQ: Linear Algebra','Eigenvalue & rank problems','c-red','mins-gray'],['PYQ: Probability','Bayes & distribution Qs','c-red','mins-gray'],['PYQ: Calculus','Integration & limits Qs','c-red','mins-gray'],['PYQ: Graphs','Graph theory Qs','c-red','mins-gray'],['Plan Next Week','Linked Lists (78.6%) prep','c-gray','mins-gray']],
    // Row 5: TOPIC BLOCK
    [['Linked Lists (78.6%)','Singly/doubly/circular, reversal, cycle','c-blue','mins-blue'],['LA Advanced (80.3%↑)','Cayley-Hamilton, vector spaces, rank apps','c-green','mins-green'],['Probability Adv (78%↑)','Random variables, distributions, Bayes apps','c-green','mins-green'],['Trees Adv (78.3%)','Balanced trees, B-trees, tree properties','c-blue','mins-blue'],['Calculus Adv (76.8%)','Differential equations, series convergence','c-blue','mins-blue']],
  ],
  // ═══════════════════════════════════════════════════════════════════════════════
  // PHASE 2: ALGORITHMS & ADV DS (Jun–Jul) — Tier 1+2: Algo (4Qs, ~7m) + DS Advanced + Programming
  // ═══════════════════════════════════════════════════════════════════════════════
  "2": [
    [['Warm-up','Asymptotic notation','c-green','mins-green'],['Warm-up','MST properties recall','c-green','mins-green'],['Warm-up','BST operations','c-green','mins-green'],['Warm-up','Heap properties','c-green','mins-green'],['Warm-up','DS+Algo full recall','c-green','mins-green']],
    [['Asymptotic (83.8% #1)','Big-O, Θ, Master Thm, recurrences','c-blue','mins-blue'],['MST (Rising ↑ 81.1%)','Kruskal, Prim, cut property','c-green','mins-green'],['BSTs (79.5%)','Insert, delete, AVL balancing','c-blue','mins-blue'],['Heaps (80.6%)','Heapify, priority queue, heap sort','c-blue','mins-blue'],['Algo+DS Mock','Timed section; target 12–14 marks','c-purple','mins-gray']],
    [['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA: Timed Test','Exam-condition GA','c-amber','mins-amber']],
    [['PYQ: Asymptotic','Recurrence & Big-O Qs','c-red','mins-gray'],['PYQ: MST','Kruskal/Prim 2-mark Qs','c-red','mins-gray'],['PYQ: BST','Tree operation Qs','c-red','mins-gray'],['PYQ: Heaps','Heap build & sort Qs','c-red','mins-gray'],['Plan Next Week','Track DS completion','c-gray','mins-gray']],
    // Row 5: TOPIC BLOCK 
    [['Recursion (76.2%)','Tail recursion, tree recursion, stack frames','c-blue','mins-blue'],['Graph Algorithms','BFS, DFS, Dijkstra, Bellman-Ford','c-blue','mins-blue'],['Dynamic Programming','LCS, knapsack, matrix chain','c-blue','mins-blue'],['Divide & Conquer','Merge sort analysis, Akra-Bazzi','c-blue','mins-blue'],['Programming NAT Drill','Output prediction, pointer tracing','c-red','mins-gray']],
  ],
  // ═══════════════════════════════════════════════════════════════════════════════
  // PHASE 3: SYSTEMS (Aug–Sep) — Tier 2: OS (6Qs, ~12m) + CO (6Qs, ~12m)
  // ═══════════════════════════════════════════════════════════════════════════════
  "3": [
    [['Warm-up','OS scheduling concepts','c-green','mins-green'],['Warm-up','Sync primitives recall','c-green','mins-green'],['Warm-up','Cache mapping review','c-green','mins-green'],['Warm-up','Pipeline stages recall','c-green','mins-green'],['Warm-up','Full systems recall','c-green','mins-green']],
    [['CPU Scheduling (82.8%)','FCFS, SJF, RR, Priority, MLFQ','c-blue','mins-blue'],['Process Sync (81.6%)','Semaphores, monitors, crit section','c-blue','mins-blue'],['Cache Memory (80.2%)','Direct/assoc/set-assoc, LRU, FIFO','c-blue','mins-blue'],['Pipelining (79.5%)','Data/ctrl hazards, forwarding, stall','c-blue','mins-blue'],['OS+CO Mock','Timed section; target 17+/22','c-purple','mins-gray']],
    [['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA: Timed Test','Exam-condition GA','c-amber','mins-amber']],
    [['PYQ: Scheduling','FCFS/SJF/RR 2-mark Qs','c-red','mins-gray'],['PYQ: Sync','Semaphore & monitor Qs','c-red','mins-gray'],['PYQ: Cache','Hit rate & mapping Qs','c-red','mins-gray'],['PYQ: Pipelining','Hazard & CPI Qs','c-red','mins-gray'],['Plan Next Week','Memory topics prep','c-gray','mins-gray']],
    // Row 5: TOPIC BLOCK 
    [['CPU Sched Adv (82.8%)','MLFQ, real-time sched, Gantt chart drills','c-blue','mins-blue'],['Sync Advanced (81.6%)','Dining philosophers, readers-writers','c-blue','mins-blue'],['Cache Calc (80.2%)','AMAT, multi-level cache, write policies','c-blue','mins-blue'],['Deadlock (79.4%)','Detection, avoidance, Banker\'s algo','c-blue','mins-blue'],['Mem Mgmt (76.1%)','Paging, segmentation, TLB','c-blue','mins-blue']],
  ],
  // ═══════════════════════════════════════════════════════════════════════════════
  // PHASE 4: BREADTH (Oct–Nov) — Tier 3+4: ToC(5), DB(4), CD(3), DL(3), CN(5)
  // ═══════════════════════════════════════════════════════════════════════════════
  "4": [
    [['Warm-up','Finite automata recall','c-green','mins-green'],['Warm-up','Normalization rules','c-green','mins-green'],['Warm-up','Parsing tables recall','c-green','mins-green'],['Warm-up','Boolean algebra rules','c-green','mins-green'],['Warm-up','Mixed P4 recall','c-green','mins-green']],
    [['Finite Automata (81.8%)','DFA, NFA, minimization, conversion','c-blue','mins-blue'],['Normalization ↑(81.7%)','FDs, 1NF–BCNF, lossless join','c-green','mins-green'],['Parsing (82.2%)','LL(1), LR(0), SLR, LALR, first/follow','c-blue','mins-blue'],['Boolean Algebra ↑(79.4%)','K-maps, SOP/POS, comb. circuits','c-green','mins-green'],['Breadth Mock','All P4 subjects; target 48–52 total','c-purple','mins-gray']],
    [['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['GA: Timed Test','Target 12+/15 by now','c-amber','mins-amber']],
    [['PYQ: ToC','Automata & regex Qs','c-red','mins-gray'],['PYQ: DB','Normalization + RA (77.1%) Qs','c-red','mins-gray'],['PYQ: CD','Parsing + SDT Qs','c-red','mins-gray'],['PYQ: DL','Boolean + K-map Qs','c-red','mins-gray'],['Plan Next Week','Track P4 completion %','c-gray','mins-gray']],
    // Row 5: TOPIC BLOCK 
    [['Concurrency (79.6%)','2PL, timestamp ordering, serializability','c-blue','mins-blue'],['Indexing (77.9%)','B+ trees, hash indexes, dense vs sparse','c-blue','mins-blue'],['CN Selective (62.3%)','TCP/IP, subnetting, routing (NAT only)','c-amber','mins-amber'],['SQL Advanced (76.7%)','Nested queries, GROUP BY, HAVING','c-blue','mins-blue'],['SDT (78.1%↑)','S-attributed, L-attributed, annotated trees','c-green','mins-green']],
  ],
  // ═══════════════════════════════════════════════════════════════════════════════
  // PHASE 5: REVISION + MOCKS (Dec–Jan) — Full syllabus, 3 mocks/week
  // ═══════════════════════════════════════════════════════════════════════════════
  "5": [
    [['Warm-up','Tier 1 formula recall','c-green','mins-green'],['Warm-up','Mock 1 weak topics','c-green','mins-green'],['Warm-up','Tier 2 key concepts','c-green','mins-green'],['Warm-up','Lowest-scoring recall','c-green','mins-green'],['Warm-up','Rising topics drill','c-green','mins-green']],
    [['Tier 1 Revision','Engg Math + DS PYQ solve','c-blue','mins-blue'],['Full Mock (65Q)','Timed 3hr, exam conditions','c-purple','mins-gray'],['Tier 2 Revision','OS + CO + Algo all topics','c-blue','mins-blue'],['Tier 3+4 Revision','ToC + DB + CD + DL selective','c-blue','mins-blue'],['Rising Topics Polish','LA↑, MST↑, Norm↑, Bool↑, Prob↑, SDT↑','c-green','mins-green']],
    [['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['Mock 1 Analysis','Error log by subject + type','c-gray','mins-gray'],['GA Practice','Daily verbal + quant','c-amber','mins-amber'],['Mock 2 Analysis','Error log: 1-mark vs 2-mark','c-gray','mins-gray'],['GA Master','Timed 15-mark; target 13+/15','c-amber','mins-amber']],
    [['Rising PYQ Blitz','LA + MST + Norm 2-mark Qs','c-green','mins-green'],['Error Patterns','Categorise: concept vs calc vs silly','c-gray','mins-gray'],['NAT Practice','All subjects NAT Qs (+EV drill)','c-blue','mins-blue'],['PYQ Blitz','10 random mixed past Qs','c-red','mins-gray'],['Plan Next Week','Spaced rep schedule check','c-gray','mins-gray']],
    // Row 5: TOPIC BLOCK 
    [['Top 10 Conf Drill','Asymptotic•CPU•Parsing•FA•Norm•Sync•MST','c-blue','mins-blue'],['Rising ↑ Topics','LA↑,Prob↑,MST↑,Norm↑,Bool↑ 2-mark drill','c-green','mins-green'],['Top 11-20 Drill','Cache•Conc•Pipeline•BST•Bool•Deadlock','c-blue','mins-blue'],['30-Topic Speed Drill','1 problem per topic, timed 60min','c-purple','mins-gray'],['All 30 Error Review','Fix mistakes across entire topic set','c-gray','mins-gray']],
  ],
  // ═══════════════════════════════════════════════════════════════════════════════
  // PHASE 6: FINAL SPRINT (Feb ~3 weeks) — NO new topics. Light revision only.
  // ═══════════════════════════════════════════════════════════════════════════════
  "6": [
    [['Formula Sheet','LA + Prob + Calc formulas','c-green','mins-green'],['Formula Sheet','DS + Algo key theorems','c-green','mins-green'],['Formula Sheet','OS + CO key rules','c-green','mins-green'],['Formula Sheet','ToC + DB + CD rules','c-green','mins-green'],['Exam Day','Strategy review + calm','c-amber','mins-amber']],
    [['Light: Rising Topics','LA↑, Prob↑, MST↑, Norm↑, Bool↑','c-green','mins-green'],['Light: Tier 1','Engg Math + DS key concepts','c-blue','mins-blue'],['Light: Tier 2','OS scheduling + CO cache only','c-blue','mins-blue'],['Light: Tier 3','ToC automata + DB norm only','c-blue','mins-blue'],['🎯 GATE EXAM','GA→NAT→2mk MCQ→1mk MCQ','c-green','mins-green']],
    [['GA Practice','15min easy confidence set','c-amber','mins-amber'],['GA Practice','10min light set','c-amber','mins-amber'],['GA Practice','10min light set','c-amber','mins-amber'],['Mock Analysis','Final error review','c-gray','mins-gray'],['Exam Strategy','GA 1st, NATs 2nd, 2mk 3rd','c-green','mins-green']],
    [['Positive Recall','Review things you know well','c-green','mins-green'],['NAT Strategy','Which subjects → NAT Qs (+EV)','c-blue','mins-blue'],['Light Reading','Formula sheet only, 20min max','c-gray','mins-gray'],['Mental Prep','Visualise exam: 65Q, 3hrs','c-gray','mins-gray'],['🏆 Perform!','Trust your 339 days of prep','c-green','mins-green']],
    // Row 5: TOPIC BLOCK 
    [['Rising Quick Review','LA↑,MST↑,Norm↑,Bool↑ formulas','c-green','mins-green'],['T1 Key Formulas','Math+DS: 13 topics recall','c-blue','mins-blue'],['T2 Key Formulas','OS+CO+Algo: 10 key topic formulas','c-blue','mins-blue'],['30-Topic Final Check','1 formula + 1 concept per topic','c-purple','mins-gray'],['🎯 All 30 Mastered','Execute: GA→NAT→2mk MCQ','c-green','mins-green']],
  ],
};

export default function Roadmap() {
  const schedule = useAdaptiveSchedule(6, 5);

  const [warmupMins, setWarmupMins] = useState(10);
  const [deepworkMins, setDeepworkMins] = useState(45);
  const [gaMins, setGaMins] = useState(15);
  const [pyqMins, setPyqMins] = useState(20);
  const [topicMins, setTopicMins] = useState(30);
  const [ttPhase, setTtPhase] = useState(schedule.currentPhase);
  const [checkedMilestones, setCheckedMilestones] = useState<Record<string, Record<number, boolean>>>({});
  const [dailyProgress, setDailyProgress] = useState<Record<string, Record<number, boolean>>>({});
  
  const totalMins = schedule.lowEnergyMode ? 10 : warmupMins + deepworkMins + gaMins + pyqMins + topicMins;
  const dailyHours = totalMins / 60;

  const todayDateStr = schedule.todayStr;
  const todayDayIndex = schedule.currentDayIndex;
  const todaysDayName = schedule.lowEnergyMode ? "REST DAY (Low Energy)" : `DAY ${todayDayIndex + 1} OF PHASE ${schedule.currentPhase}`;

  useEffect(() => {
    const savedM = localStorage.getItem('gate2027_milestones');
    if (savedM) setCheckedMilestones(JSON.parse(savedM));

    const savedD = localStorage.getItem('gate2027_daily');
    if (savedD) setDailyProgress(JSON.parse(savedD));
  }, []);

  const toggleCheck = (mId: string, iIndex: number) => {
    const newChecked = { ...checkedMilestones };
    if (!newChecked[mId]) newChecked[mId] = {};
    newChecked[mId][iIndex] = !newChecked[mId][iIndex];
    setCheckedMilestones(newChecked);
    localStorage.setItem('gate2027_milestones', JSON.stringify(newChecked));
  };

  const toggleDailyTask = (dateStr: string, taskIdx: number) => {
    const newDp = { ...dailyProgress };
    if (!newDp[dateStr]) newDp[dateStr] = {};
    newDp[dateStr][taskIdx] = !newDp[dateStr][taskIdx];
    setDailyProgress(newDp);
    localStorage.setItem('gate2027_daily', JSON.stringify(newDp));
  };

  const currentTabStyles = "data-[state=active]:bg-sidebar data-[state=active]:border-border border-transparent";
  
  const examDate = new Date('2027-02-01');
  const [daysLeft, setDaysLeft] = useState(339);

  useEffect(() => {
    const now = new Date();
    const diff = examDate.getTime() - now.getTime();
    setDaysLeft(Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24))));
  }, [examDate]);

  const totalCalculatedHours = Math.round(daysLeft * dailyHours);

  return (
    <div className="space-y-8 max-w-7xl mx-auto p-4 md:p-8 animate-fade-in pb-20">
      <div className="flex flex-col gap-4 mb-4">
        <Badge variant="outline" className="w-fit mb-2 text-emerald-500 border-emerald-500/30 tracking-widest uppercase font-mono text-[10px] bg-emerald-500/5">
          // GATE CSE 2027 — IIT Mandi Target
        </Badge>
        <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-foreground flex items-center gap-3">
          1-Year Study <span className="text-primary">Roadmap</span>
        </h1>
        <p className="text-base md:text-xl text-muted-foreground max-w-3xl">
          Data-driven preparation plan built on ML model predictions (R² = 76.67%) with a dual score path. <br/>
          {totalMins} minutes daily. Every session counts.
        </p>

        <div className="flex flex-wrap gap-6 mt-4">
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-orange-500 flex items-center gap-1">
              <Zap className="w-5 h-5 fill-orange-500 shrink-0" />
              {schedule.streak}
            </span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Day Streak</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-primary">{totalCalculatedHours}</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Total Hours</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-primary">{dailyHours.toFixed(1)}h</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Daily Session</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-primary">6</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Phases</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-primary">62-68</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Target Marks Band</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-primary">620-700</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Score Path</span>
          </div>
        </div>
      </div>

      <Tabs defaultValue="phases" className="w-full">
        <TabsList className="flex flex-wrap justify-start h-auto bg-transparent mb-6 border-b border-border rounded-none p-0 overflow-x-auto w-full gap-1 snap-x">
          <TabsTrigger value="phases" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>PHASES</TabsTrigger>
          <TabsTrigger value="year" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>YEAR VIEW</TabsTrigger>
          <TabsTrigger value="timetable" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>WEEKLY TABLE</TabsTrigger>
          <TabsTrigger value="daily" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>DAILY SESSION</TabsTrigger>
          <TabsTrigger value="subjects" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>SUBJECT MAP</TabsTrigger>
          <TabsTrigger value="milestones" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>MILESTONES</TabsTrigger>
          <TabsTrigger value="strategy" className={`font-mono text-xs px-4 py-3 rounded-t-lg border-x border-t ${currentTabStyles}`}>STRATEGY</TabsTrigger>
        </TabsList>

        <TabsContent value="phases" className="space-y-6">
          <div className="mb-8">
            <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Study Phases</h2>
            <p className="text-sm text-muted-foreground mt-2">6 progressive phases from foundation to exam day. Each phase has a clear focus and target outcome.</p>
          </div>

          <div className="bg-sidebar border border-border rounded-xl p-4 md:p-6 flex flex-wrap items-center gap-6 mb-8">
            <div>
              <div className="text-xs font-mono text-muted-foreground">EXAM DATE</div>
              <div className="text-3xl font-mono font-bold text-primary">FEB 2027</div>
            </div>
            <div className="text-border hidden md:block text-2xl">·</div>
            <div>
              <div className="text-xs font-mono text-muted-foreground">DAYS LEFT</div>
              <div className="text-3xl font-mono font-bold text-primary">{daysLeft}</div>
            </div>
            <div className="text-border hidden md:block text-2xl">·</div>
            <div>
              <div className="text-xs font-mono text-muted-foreground">WEEKS</div>
              <div className="text-3xl font-mono font-bold text-primary">{Math.floor(daysLeft/7)}</div>
            </div>
            <div className="text-border hidden md:block text-2xl">·</div>
            <div className="flex-1 text-right text-sm text-muted-foreground hidden md:block">
              Start today. Every session matters.<br/>
              <strong className="text-primary">{daysLeft} days = {Math.round(daysLeft * dailyHours)} hours of study remaining.</strong>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { num: '01', name: 'FOUNDATION', period: 'Mar 2026 – May 2026', badge: 'TIER 1', duration: 90, 
                focus: 'Build the mathematical and structural foundation. Engg Math (9 predicted Qs, 66.7% avg conf) is the highest-weighted technical subject. Linear Algebra recent avg jumped 2.88→4.33 Qs — highest ROI single topic. Target: 11–12/~15 marks from Engg Math alone.', 
                tags: [{t:'Linear Algebra ↑80.3%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Probability ↑78%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Calculus 76.8%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Graphs 80.4%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Trees 78.3%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Linked Lists 78.6%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'GA Daily 15min', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}],
                color: 'text-emerald-500', bg: 'bg-emerald-500/5', border: 'border-emerald-500/20'
              },
              { num: '02', name: 'ALGORITHMS & DS', period: 'Jun 2026 – Jul 2026', badge: 'TIER 1+2', duration: 61, 
                focus: 'Asymptotic Analysis = 83.8% conf — HIGHEST in entire model. MST Rising 81.1% (recent avg 1.77→2.33). Advanced DS: Heaps 80.6%, BSTs 79.5%. Programming: Recursion 76.2% NAT-only. Target: 12–14 marks from Algo+DS combined. First full mock by Jul end: 35–40.', 
                tags: [{t:'Asymptotic 83.8% #1', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'MST ↑81.1%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Heaps 80.6%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'BSTs 79.5%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Hashing 76.4%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Sorting 75.3% ↓', c:'border-rose-500/20 text-rose-400', dot:'bg-rose-400'}, {t:'Recursion 76.2%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}],
                color: 'text-blue-500', bg: 'bg-blue-500/5', border: 'border-blue-500/20'
              },
              { num: '03', name: 'SYSTEMS', period: 'Aug 2026 – Sep 2026', badge: 'TIER 2', duration: 61, 
                focus: 'OS + CO — the two subjects the model predicted with ~0 error in 2026 (most predictable section). 4 OS topics >76% conf, 2 CO topics >79%. CPU Scheduling 82.8% and Process Sync 81.6% cover most OS marks. Target: OS 9–10/~12 + CO 7–8/~12 = 16–18 total.', 
                tags: [{t:'CPU Sched 82.8%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Proc Sync 81.6%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Cache 80.2%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Pipeline 79.5%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Deadlock 79.4%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Mem Mgmt 76.1%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}],
                color: 'text-amber-500', bg: 'bg-amber-500/5', border: 'border-amber-500/20'
              },
              { num: '04', name: 'BREADTH', period: 'Oct 2026 – Nov 2026', badge: 'TIER 3+4', duration: 61, 
                focus: 'Remaining 5 subjects — focus on HIGH-CONFIDENCE topics ONLY (Section 7.3/7.4). 10 topics >76% conf across ToC/DB/CD/DL/CN. Skip low-conf areas. CN: NAT questions only (+EV, zero neg). Target: 9–11 marks from ToC+Algo+DBs combined. Full mock: 48–52.', 
                tags: [{t:'Parsing 82.2%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'FA 81.8%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Norm ↑81.7%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Bool ↑79.4%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'SDT ↑78.1%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Concurrency 79.6%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'SQL 76.7%, RA 77.1%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'CN: NAT only', c:'border-rose-500/20 text-rose-400', dot:'bg-rose-400'}],
                color: 'text-purple-400', bg: 'bg-purple-500/5', border: 'border-purple-500/20'
              },
              { num: '05', name: 'REVISION + MOCKS', period: 'Dec 2026 – Jan 2027', badge: 'CRITICAL', duration: 61, 
                focus: 'Full syllabus revision using spaced repetition: T1 every 2wk, T2 every 3wk, T3 every 4wk. Mock tests 3×/week — error-log every mock. PYQ blitz by subject (10+ years). Rising topics polish: LA↑, MST↑, Norm↑, Bool↑, Prob↑, SDT↑. GA must score 13+/15 consistently. Mock target ladder: 52→56→60 (620-safe) → 63+ (700-push).', 
                tags: [{t:'3 Mocks/Week', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Rising Topic Polish', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'PYQ Blitz 10yr', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'GA 13+/15', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'NAT Strategy Lock', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Weak Topic Sprint', c:'border-rose-500/20 text-rose-400', dot:'bg-rose-400'}, {t:'Spaced Repetition', c:'border-purple-500/20 text-purple-400', dot:'bg-purple-400'}],
                color: 'text-rose-500', bg: 'bg-rose-500/5', border: 'border-rose-500/20'
              },
              { num: '06', name: 'FINAL SPRINT', period: 'Feb 2027 · ~3 weeks', badge: 'EXAM', duration: 21, 
                focus: 'NO new topics. Light revision only. 1 mock/week max. Formula sheets, quick-recall drills. Sleep 8+ hours mandatory. Exam order: GA first (13+/15) → NAT Qs (all, +EV, 0 neg) → 2-mark MCQs (eliminate 2 then pick) → 1-mark MCQs. Target raw bands: 60–63 (620-safe) and 63–68 (700-push).', 
                tags: [{t:'Formula Sheets Only', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'1 Mock Max', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Sleep 8+ Hours', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'GA→NAT→2mk→1mk', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Mental + Physical Rest', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}],
                color: 'text-amber-400', bg: 'bg-amber-400/5', border: 'border-amber-400/20'
              }
            ].map((p, i) => (
              <Card key={i} className={`hover:shadow-lg transition-transform hover:-translate-y-1 bg-card border-border overflow-hidden flex flex-col`}>
                <div className={`p-4 flex items-center gap-4 ${p.bg} border-b ${p.border}`}>
                  <div className={`text-4xl font-mono font-bold opacity-30 ${p.color}`}>{p.num}</div>
                  <div className="flex-1">
                    <div className={`text-sm font-mono font-bold tracking-wide ${p.color}`}>{p.name}</div>
                    <div className="text-xs text-muted-foreground mt-1">{p.period}</div>
                  </div>
                  <Badge variant="outline" className={`font-mono text-[10px] ${p.color} border-current bg-background/50`}>{p.badge}</Badge>
                </div>
                <CardContent className="p-5 flex-1 flex flex-col">
                  <p className="text-xs text-muted-foreground leading-relaxed mb-4">{p.focus}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {p.tags.map((t, j) => (
                      <span key={j} className={`text-[10px] px-2 py-1 rounded-full border bg-background/50 flex items-center gap-1.5 ${t.c}`}>
                        <span className={`w-1 h-1 rounded-full ${t.dot}`}></span>
                        {t.t}
                      </span>
                    ))}
                  </div>
                  <div className="pt-3 mt-auto border-t border-border flex justify-between items-center text-xs font-mono">
                    <span className="text-muted-foreground">~{p.num==='06' ? '32' : Math.round(p.duration * dailyHours)} hrs total</span>
                    <span className="font-bold text-foreground">{p.num==='06' ? 'Light sessions only' : `${dailyHours.toFixed(1)}h/day × ${p.duration} days`}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="year" className="space-y-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">12-Month Overview</h2>
            <p className="text-sm text-muted-foreground mt-2">Each block represents 1 month. Click to see the primary focus for that month.</p>
          </div>
          
          <div className="overflow-x-auto pb-4">
            <div className="grid grid-cols-6 md:grid-cols-12 gap-1.5 min-w-[700px]">
              {months.map((m, i) => (
                <div key={i} className="flex flex-col gap-1 group">
                  <div className={`text-center font-mono text-[10px] tracking-wide ${m.color}`}>{m.name}</div>
                  <div 
                    className={`rounded-md p-2 flex flex-col items-center justify-center gap-1 min-h-[80px] border border-transparent transition-all group-hover:scale-105 group-hover:shadow-md cursor-pointer relative ${m.bg}`} 
                  >
                    <div className="font-mono text-[9px] opacity-70">{m.phase}</div>
                    <div className="text-[10px] font-semibold text-center leading-tight text-foreground whitespace-pre-line">{m.subj}</div>
                    <div className="font-mono text-[9px] mt-auto opacity-60">~{Math.round(30 * dailyHours)}h</div>

                    {/* Tooltip on hover */}
                    <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-48 p-2 bg-popover border border-border rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 pointer-events-none text-xs text-popover-foreground leading-relaxed">
                      {monthDetails[i]}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="timetable" className="space-y-6">
          <div className="mb-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Weekly Timetable</h2>
              <p className="text-sm text-muted-foreground mt-2">Each day = {totalMins} minutes. Dynamically updates by phase with checkpoints for 620-safe and 700-push attempts.</p>
            </div>
            <Select value={ttPhase} onValueChange={setTtPhase}>
              <SelectTrigger className="w-full md:w-[300px]">
                <SelectValue placeholder="Select Phase" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">Phase 1: Foundation (Mar–May)</SelectItem>
                <SelectItem value="2">Phase 2: Algorithms & DS (Jun–Jul)</SelectItem>
                <SelectItem value="3">Phase 3: Systems (Aug–Sep)</SelectItem>
                <SelectItem value="4">Phase 4: Breadth (Oct–Nov)</SelectItem>
                <SelectItem value="5">Phase 5: Revision (Dec–Jan)</SelectItem>
                <SelectItem value="6">Phase 6: Final Sprint (Feb)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="rounded-xl border border-border bg-card overflow-x-auto">
            <div className="min-w-[800px] grid grid-cols-[120px_repeat(7,1fr)]">
              <div className="p-3 border-r border-b border-border bg-sidebar font-mono text-[10px] text-muted-foreground text-center flex items-center justify-center uppercase tracking-wider">Session</div>
              {days.map(d => (
                <div key={d} className="p-3 border-r border-b border-border bg-sidebar font-mono text-[11px] text-foreground text-center font-bold">{d}</div>
              ))}
              
              {['WARM-UP', 'DEEP WORK', 'GA PRACTICE', 'PYQ SPRINT', 'TOPIC BLOCK'].map((slotName, rowIdx) => {
                const rowData = ttData[ttPhase][rowIdx];
                const customMins = [warmupMins, deepworkMins, gaMins, pyqMins, topicMins][rowIdx];
                
                return (
                  <React.Fragment key={slotName}>
                    <div className="p-2 border-r border-b border-border bg-sidebar/50 flex flex-col items-center justify-center text-center">
                      <span className="font-mono text-[10px] text-muted-foreground leading-tight">{slotName}</span>
                      <span className="font-mono text-[10px] text-primary">{customMins} min</span>
                    </div>
                    {rowData.map((cell, colIdx) => {
                      const [label, detail, clsMain, _] = cell;
                      const isGreen = clsMain === 'c-green';
                      const isBlue = clsMain === 'c-blue';
                      const isAmber = clsMain === 'c-amber';
                      const isRed = clsMain === 'c-red';
                      const isPurple = clsMain === 'c-purple';
                      
                      const bgClass = isGreen ? 'bg-emerald-500/5 border-l-2 border-emerald-500' :
                                      isBlue ? 'bg-blue-500/5 border-l-2 border-blue-500' :
                                      isAmber ? 'bg-amber-500/5 border-l-2 border-amber-500' :
                                      isRed ? 'bg-rose-500/5 border-l-2 border-rose-500' :
                                      isPurple ? 'bg-purple-500/5 border-l-2 border-purple-500' :
                                      'bg-slate-500/5 border-l-2 border-slate-500';
                                      
                      const pillClass = isGreen ? 'bg-emerald-500/20 text-emerald-500' :
                                        isBlue ? 'bg-blue-500/20 text-sky-400' :
                                        isAmber ? 'bg-amber-500/20 text-amber-400' :
                                        'bg-slate-500/20 text-muted-foreground';

                      return (
                        <div key={colIdx} className={`p-2 border-r border-b border-border flex flex-col gap-1 ${bgClass}`}>
                          <div className="font-semibold text-[11px] leading-tight text-foreground">{label}</div>
                          <div className="text-[10px] text-muted-foreground leading-tight">{detail}</div>
                          <div className={`mt-auto w-fit font-mono text-[9px] px-1.5 py-0.5 rounded-sm ${pillClass}`}>
                            {customMins}m
                          </div>
                        </div>
                      )
                    })}
                  </React.Fragment>
                )
              })}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="daily" className="space-y-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Daily Session Customizer</h2>
            <p className="text-sm text-muted-foreground mt-2">Adjust your daily study distribution. Total time scales automatically across the roadmap and supports both 620-safe and 700-push tracks.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="bg-card">
              <CardHeader>
                <CardTitle className="text-lg flex justify-between items-center">
                  <span>Allocate Minutes</span>
                  <span className="text-primary font-mono text-xl">{totalMins} min ({dailyHours.toFixed(1)}h)</span>
                </CardTitle>
                <CardDescription>Drag sliders to customize your 4-phase daily workflow.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-emerald-500 font-medium">Warm-Up / Recall</span>
                    <span className="font-mono text-muted-foreground">{warmupMins} min</span>
                  </div>
                  <Slider value={[warmupMins]} onValueChange={v => setWarmupMins(v[0])} max={30} step={5} className="[&_[role=slider]]:border-emerald-500" />
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-blue-500 font-medium">Deep Work Block</span>
                    <span className="font-mono text-muted-foreground">{deepworkMins} min</span>
                  </div>
                  <Slider value={[deepworkMins]} onValueChange={v => setDeepworkMins(v[0])} max={180} step={15} className="[&_[role=slider]]:border-blue-500" />
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-amber-500 font-medium">GA Practice</span>
                    <span className="font-mono text-muted-foreground">{gaMins} min</span>
                  </div>
                  <Slider value={[gaMins]} onValueChange={v => setGaMins(v[0])} max={45} step={5} className="[&_[role=slider]]:border-amber-500" />
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-rose-500 font-medium">PYQ Sprint</span>
                    <span className="font-mono text-muted-foreground">{pyqMins} min</span>
                  </div>
                  <Slider value={[pyqMins]} onValueChange={v => setPyqMins(v[0])} max={90} step={10} className="[&_[role=slider]]:border-rose-500" />
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-purple-500 font-medium">Topic Deep Dive</span>
                    <span className="font-mono text-muted-foreground">{topicMins} min</span>
                  </div>
                  <Slider value={[topicMins]} onValueChange={v => setTopicMins(v[0])} max={90} step={10} className="[&_[role=slider]]:border-purple-500" />
                </div>

                <div className="pt-6 border-t border-border">
                  <div className="flex w-full h-8 rounded-md overflow-hidden bg-sidebar-border border border-border">
                    <div style={{ width: `${(warmupMins/totalMins)*100}%` }} className="bg-emerald-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{warmupMins}m</div>
                    <div style={{ width: `${(deepworkMins/totalMins)*100}%` }} className="bg-blue-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{deepworkMins}m</div>
                    <div style={{ width: `${(gaMins/totalMins)*100}%` }} className="bg-amber-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{gaMins}m</div>
                    <div style={{ width: `${(pyqMins/totalMins)*100}%` }} className="bg-rose-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{pyqMins}m</div>
                    <div style={{ width: `${(topicMins/totalMins)*100}%` }} className="bg-purple-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{topicMins}m</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="space-y-4">
              <Card className="bg-card relative overflow-hidden">
                <CardHeader className="py-4 border-b border-border/50 mb-2">
                  <CardTitle className="text-sm font-mono text-muted-foreground uppercase tracking-widest flex items-center justify-between">
                    <span>Today's Itinerary</span>
                    <Badge variant="outline" className={`${schedule.lowEnergyMode ? 'bg-orange-500/10 text-orange-500 border-orange-500/20' : 'bg-primary/10 text-primary border-primary/20'}`}>
                      {todaysDayName}
                    </Badge>
                  </CardTitle>
                  <div className="flex items-center justify-between mt-3 pt-2">
                    <div className="flex flex-col">
                      <span className="text-xs font-bold text-foreground">Low Energy Mode</span>
                      <span className="text-[10px] text-muted-foreground">Keep your habit alive (10m)</span>
                    </div>
                    <Switch checked={schedule.lowEnergyMode} onCheckedChange={schedule.toggleLowEnergyMode} />
                  </div>
                </CardHeader>
                <CardContent className="space-y-1 pb-6">
                  {schedule.lowEnergyMode ? (
                    <div className="flex items-start gap-3 py-4 border-b border-border/50 bg-orange-500/5 -mx-6 px-6 relative">
                      <div className="mt-0.5">
                        <Checkbox 
                          id="daily-micro"
                          checked={!!dailyProgress[todayDateStr]?.['micro']}
                          onCheckedChange={() => toggleDailyTask(todayDateStr, 'micro' as any)}
                          className="data-[state=checked]:bg-orange-500 data-[state=checked]:border-orange-500"
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <label htmlFor="daily-micro" className="cursor-pointer text-sm font-bold text-orange-500 hover:opacity-80 transition-opacity">
                          Minimum Viable Routine (10m)
                        </label>
                        <div className="mt-1.5 bg-background/50 border border-orange-500/20 p-2 rounded-md text-xs border-l-2 border-l-orange-500">
                          <span className="font-semibold text-foreground block">Light GA Practice & Formula Recap</span>
                          <span className="text-muted-foreground block mt-0.5">No deep work today. Just show up and keep the streak alive.</span>
                        </div>
                      </div>
                    </div>
                  ) : (
                  [
                    { id: 0, title: 'Warm-Up', mins: warmupMins, tColor: 'text-emerald-500', bColor: 'border-emerald-500', cbClass: 'data-[state=checked]:bg-emerald-500 data-[state=checked]:border-emerald-500', tt: ttData[schedule.currentPhase][0][todayDayIndex], desc: "Revise yesterday's notes. 2–3 key concepts." },
                    { id: 1, title: 'Deep Work Block', mins: deepworkMins, tColor: 'text-blue-500', bColor: 'border-blue-500', cbClass: 'data-[state=checked]:bg-blue-500 data-[state=checked]:border-blue-500', tt: ttData[schedule.currentPhase][1][todayDayIndex], desc: "New concept or problem-set for today's topic." },
                    { id: 2, title: 'GA Practice', mins: gaMins, tColor: 'text-amber-500', bColor: 'border-amber-500', cbClass: 'data-[state=checked]:bg-amber-500 data-[state=checked]:border-amber-500', tt: ttData[schedule.currentPhase][2][todayDayIndex], desc: "Daily GA regardless of phase." },
                    { id: 3, title: 'PYQ Sprint', mins: pyqMins, tColor: 'text-rose-500', bColor: 'border-rose-500', cbClass: 'data-[state=checked]:bg-rose-500 data-[state=checked]:border-rose-500', tt: ttData[schedule.currentPhase][3][todayDayIndex], desc: "Solve previous year questions. Mark doubts." },
                    { id: 4, title: 'Topic Deep Dive', mins: topicMins, tColor: 'text-purple-500', bColor: 'border-purple-500', cbClass: 'data-[state=checked]:bg-purple-500 data-[state=checked]:border-purple-500', tt: ttData[schedule.currentPhase][4][todayDayIndex], desc: "Dedicated deep dive into a specific topic." },
                  ].map((task) => {
                    const isChecked = !!dailyProgress[todayDateStr]?.[task.id];
                    return (
                      <div key={task.id} className={`flex items-start gap-3 py-3 ${task.id !== 4 ? 'border-b border-border/50' : ''}`}>
                        <div className="mt-0.5">
                          <Checkbox 
                            id={`daily-${task.id}`}
                            checked={isChecked}
                            onCheckedChange={() => toggleDailyTask(todayDateStr, task.id)}
                            className={task.cbClass}
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <label 
                            htmlFor={`daily-${task.id}`}
                            className={`cursor-pointer text-sm font-bold select-none ${task.tColor} ${isChecked ? 'line-through opacity-50' : 'hover:opacity-80 transition-opacity'}`}
                          >
                            <span>{task.title} ({task.mins}m)</span>
                          </label>
                          <div className={`mt-1.5 bg-background border border-border p-2 rounded-md text-xs border-l-2 ${task.bColor} transition-opacity ${isChecked ? 'opacity-50' : ''}`}>
                            <span className="font-semibold text-foreground block md:inline">{task.tt[0]}</span>
                            <span className="text-muted-foreground md:ml-1 block md:inline">{task.tt[1]}</span>
                          </div>
                          <div className={`text-[10px] text-muted-foreground mt-1.5 leading-tight transition-opacity ${isChecked ? 'opacity-40' : ''}`}>
                            {task.desc}
                          </div>
                        </div>
                      </div>
                    );
                  })
                  )}

                  <div className="pt-6 mt-2">
                    <Button 
                      className={`w-full h-12 font-bold tracking-wide transition-all ${schedule.lastStudyDate === todayDateStr ? 'bg-zinc-800 text-zinc-400 hover:bg-zinc-800' : 'bg-primary hover:bg-primary/90 text-primary-foreground shadow-[0_0_15px_rgba(var(--primary),0.3)]'}`}
                      onClick={() => schedule.completeDay()}
                      disabled={schedule.lastStudyDate === todayDateStr}
                    >
                      {schedule.lastStudyDate === todayDateStr ? (
                        <>
                          <CheckCircle className="w-4 h-4 mr-2" /> Day Complete! Sequence saved.
                        </>
                      ) : (
                        schedule.lowEnergyMode ? "Mark Rest Day Complete (+1 Streak)" : "Mark Day Complete & Advance Queue"
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-amber-500/10 border-amber-500/20">
                <CardContent className="p-4 flex gap-4 items-start">
                  <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                  <div>
                    <div className="text-sm font-bold text-amber-500">Key Rule</div>
                    <div className="text-xs text-muted-foreground mt-1">Never skip the GA block. Even on hard subject days. GA is the base lock for both 620-safe and 700-push outcomes.</div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="subjects" className="space-y-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Subject Priority Map</h2>
            <p className="text-sm text-muted-foreground mt-2">Ordered by predicted 2027 weightage × confidence score. Use this map to secure 620-safe first, then push 700 via high-confidence 2-mark topics.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {subjects.map((s, i) => (
              <Card key={i} className="bg-card">
                <CardContent className="p-4 flex gap-4">
                  <div className="font-mono text-2xl font-bold opacity-10 pt-1 shrink-0">
                    {String(i+1).padStart(2,'0')}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-sm text-foreground truncate" title={s.name}>{s.name}</div>
                    <div className="flex flex-wrap gap-1.5 mt-2 mb-3">
                      <Badge variant="outline" className={`font-mono text-[9px] ${s.tc}`}>
                        {['','🔴 T1 Must','🟠 T2 High','🟡 T3 Select','🟢 T4 Light'][s.tier]}
                      </Badge>
                      <Badge variant="outline" className="font-mono text-[9px] text-amber-400 border-amber-400/30 bg-amber-400/10">
                        {s.qs} Qs
                      </Badge>
                      <Badge variant="outline" className="font-mono text-[9px] text-muted-foreground border-border bg-sidebar">
                        {s.phase}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2 mb-3">
                      <Progress value={(s.qs / 11) * 100} className="h-1.5 bg-border/50" />
                      <span className={`font-mono text-[10px] w-8 text-right text-${s.color.replace('bg-','')}`}>{s.qs}Q</span>
                    </div>
                    <div className="text-[11px] text-muted-foreground leading-relaxed line-clamp-2" title={s.topics}>
                      {s.topics}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="milestones" className="space-y-6">
          <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Milestone Timeline</h2>
              <p className="text-sm text-muted-foreground mt-2">Check off achievements as you go. Progress is saved locally in your browser across both 620-safe and 700-push milestones.</p>
            </div>
            <div className="bg-sidebar px-4 py-2 rounded-lg border border-border flex items-center gap-3">
              <span className="text-sm font-medium text-foreground">Overall Goal</span>
              <span className="text-sm font-bold text-primary">
                {Object.values(checkedMilestones).reduce((acc, curr) => acc + Object.values(curr).filter(Boolean).length, 0)} / {milestonesData.reduce((acc, curr) => acc + curr.items.length, 0)}
              </span>
            </div>
          </div>

          <div className="relative pl-4 md:pl-8 border-l-2 border-border space-y-8 pb-8">
            {milestonesData.map((m) => {
              const checkedCount = m.items.filter((_, i) => checkedMilestones[m.id]?.[i]).length;
              const isFullyDone = checkedCount === m.items.length;
              
              return (
                <div key={m.id} className={`relative bg-card border ${isFullyDone ? 'border-primary/50' : 'border-border'} rounded-xl p-5 hover:border-primary/50 transition-colors`}>
                  <div className={`absolute -left-[23px] md:-left-[39px] top-6 w-3 h-3 rounded-full border-2 ${isFullyDone ? 'bg-primary border-primary shadow-[0_0_8px_rgba(var(--primary),0.8)]' : m.type === 'active' ? 'bg-amber-500 border-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]' : 'bg-background border-border'}`}></div>
                  
                  <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 mb-3">
                    <div>
                      <div className="font-mono text-[11px] text-muted-foreground mb-1 flex items-center gap-2">
                        <CalendarDays className="w-3 h-3" /> {m.date}
                      </div>
                      <h3 className="font-bold text-sm text-foreground">{m.title}</h3>
                    </div>
                    <Badge variant="outline" className={`font-mono text-[10px] ${m.btc}`}>{m.badge}</Badge>
                  </div>
                  
                  <p className="text-xs text-muted-foreground mb-4">{m.desc}</p>
                  
                  <div className="flex flex-col gap-3">
                    {m.items.map((item, iIndex) => {
                      const isChecked = !!checkedMilestones[m.id]?.[iIndex];
                      return (
                        <div key={iIndex} className="flex items-start gap-3 group">
                          <Checkbox 
                            id={`${m.id}-${iIndex}`} 
                            checked={isChecked}
                            onCheckedChange={() => toggleCheck(m.id, iIndex)}
                            className="data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                          />
                          <label 
                            htmlFor={`${m.id}-${iIndex}`} 
                            className={`text-xs cursor-pointer select-none leading-tight transition-colors ${isChecked ? 'text-muted-foreground line-through opacity-70' : 'text-foreground group-hover:text-primary'}`}
                          >
                            {item}
                          </label>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </TabsContent>

        <TabsContent value="strategy" className="space-y-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Exam Strategy & Tips</h2>
            <p className="text-sm text-muted-foreground mt-2">Based on model predictions, calibration analysis, and GATE exam patterns.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { icon: Target, title: 'DUAL ROADMAP: 620 SAFE / 700 PUSH', text: '620-safe track: 60–63 raw marks with strong GA + NAT discipline. 700-push track: 63–68 raw marks with higher 2-mark conversion in OS/Algo/Math. Treat 60 as floor, 68 as stretch.', color: 'text-primary', bg: 'bg-primary/10' },
              { icon: TrendingUp, title: 'Linear Algebra is Your Secret Weapon', text: 'Recent average jumped 2.88→4.33 Qs (Rising↑ 80.3%). Predicted 1.01 Qs at 80.3% conf. This single topic could swing 6–8 marks. Priority #1 in Phase 1.', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
              { icon: Target, title: 'NAT-First Exam Strategy', text: 'Exam order: GA first (15 marks locked) → ALL NATs (0 negative marking, pure +EV) → 2-mark MCQs (eliminate 2 options: -2/3 → +2 gamble) → 1-mark MCQs last (-1/3 penalty).', color: 'text-blue-500', bg: 'bg-blue-500/10' },
              { icon: AlertTriangle, title: 'Calibration Inversion Insight', text: 'Section 4: Topics in 65–80% confidence band have HIGHER real accuracy (80–87%) vs 80%+ band. The 30 high-conf topics (>75%) are calibration sweet spot — trust them more than raw %.', color: 'text-amber-500', bg: 'bg-amber-500/10' },
              { icon: TrendingUp, title: '6 Rising Trend Topics', text: 'Linear Algebra↑, Probability↑, MST↑, Normalization↑, Boolean Algebra↑, SDT↑. These 6 show increasing question counts. Prepare as 2-mark sources. Combined potential: 8–12 marks.', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
              { icon: TrendingUp, title: '2 Declining Trend Topics', text: 'Sorting (75.3% ↓) and Verbal Ability (75.5% ↓). Don\'t skip — still >75% conf and in top 30. But invest less time. Sorting: 1 day/phase. Verbal: daily 5min only.', color: 'text-rose-500', bg: 'bg-rose-500/10' },
              { icon: CheckCircle2, title: 'GA = 13+/15. Non-Negotiable.', text: 'Model predicted 11 Qs vs 10 actual (Sec 5). 15 mins daily × 339 days = ~85 hours invested. GA = 15 marks at easiest difficulty. Best marks-per-hour in entire paper.', color: 'text-primary', bg: 'bg-primary/10' },
              { icon: BookOpen, title: 'Asymptotic Analysis: 83.8% #1', text: 'HIGHEST confidence topic in entire 1606-question model. Predicted 0.43 Qs (stable). Master Theorem, recurrences, Akra-Bazzi. Section 6 rank #1. Guaranteed marks.', color: 'text-blue-500', bg: 'bg-blue-500/10' },
              { icon: RefreshCw, title: 'Spaced Repetition Schedule', text: 'Tier 1 (Engg Math, DS): every 2 weeks. Tier 2 (OS, CO, Algo): every 3 weeks. Tier 3 (ToC, CN, DBs): every 4 weeks. Tier 4 (DL, CD, Prog): as needed. Blocks forgetting decay.', color: 'text-purple-500', bg: 'bg-purple-500/10' },
              { icon: Brain, title: 'Phase 5: Where Ranks Are Made', text: 'Dec–Jan: 3 mocks/week × 8 weeks = 24 mocks. Error analysis after EVERY mock. Categorise errors: concept vs calculation vs silly. Target trajectory: 52→56→60→63+ marks.', color: 'text-rose-500', bg: 'bg-rose-500/10' },
              { icon: AlertTriangle, title: 'DS Volatility Warning', text: 'Section 3: DS has highest prediction error (most volatile). 7 predicted Qs at 71.5% avg conf. Don\'t over-rely on count — focus on conceptual mastery. BSTs (79.5%) is anchor topic.', color: 'text-amber-500', bg: 'bg-amber-500/10' },
              { icon: Target, title: 'Negative Marking Rules', text: 'MCQ (1-mark): −1/3 per wrong. MCQ (2-mark): −2/3 per wrong. NAT: 0 penalty ever. Strategy: attempt ALL NATs always. MCQs: only attempt if you can eliminate ≥2 options.', color: 'text-blue-500', bg: 'bg-blue-500/10' },
            ].map((tip, i) => (
              <Card key={i} className="bg-card">
                <CardHeader className="pb-2">
                  <div className={`p-2 w-fit rounded-lg ${tip.bg} mb-3`}>
                    <tip.icon className={`w-5 h-5 ${tip.color}`} />
                  </div>
                  <CardTitle className="text-sm font-bold leading-snug">
                    {tip.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {tip.text}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

      </Tabs>
    </div>
  );
}
