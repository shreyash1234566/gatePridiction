import React, { useState, useEffect } from "react";
import { Map, Clock, CalendarDays, TrendingUp, AlertTriangle, Target, BookOpen, RefreshCw, CheckCircle2, Brain } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";

// Constants
const subjects = [
  { name: 'General Aptitude', qs: 11, conf: 63.6, tier: 1, color: 'bg-emerald-500', tc: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20', time: 'Daily 15min + Phase build', topics: 'Verbal Ability, Quantitative Aptitude, Logical Reasoning', phase: 'All phases' },
  { name: 'Engineering Mathematics', qs: 9, conf: 66.7, tier: 1, color: 'bg-emerald-500', tc: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20', time: 'Phase 1 main focus', topics: 'Linear Algebra ↑, Probability ↑, Calculus, Graphs', phase: 'Mar–May' },
  { name: 'Data Structures', qs: 7, conf: 71.5, tier: 1, color: 'bg-emerald-500', tc: 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20', time: 'Phase 1–2', topics: 'BSTs, Heaps, Trees, Hashing, Linked Lists', phase: 'May–Jul' },
  { name: 'Operating Systems', qs: 6, conf: 67.0, tier: 2, color: 'bg-blue-500', tc: 'text-blue-500 bg-blue-500/10 border-blue-500/20', time: 'Phase 3', topics: 'CPU Scheduling, Process Sync, Deadlock, Memory Mgmt', phase: 'Aug–Sep' },
  { name: 'Computer Organization', qs: 6, conf: 65.8, tier: 2, color: 'bg-blue-500', tc: 'text-blue-500 bg-blue-500/10 border-blue-500/20', time: 'Phase 3', topics: 'Cache Memory, Pipelining, I/O', phase: 'Aug–Sep' },
  { name: 'Theory of Computation', qs: 5, conf: 63.6, tier: 3, color: 'bg-purple-500', tc: 'text-purple-500 bg-purple-500/10 border-purple-500/20', time: 'Phase 4', topics: 'Finite Automata, Regular Languages, CFG', phase: 'Oct' },
  { name: 'Computer Networks', qs: 5, conf: 62.3, tier: 3, color: 'bg-purple-500', tc: 'text-purple-500 bg-purple-500/10 border-purple-500/20', time: 'Phase 4 (selective)', topics: 'TCP/IP, Routing, DNS, HTTP — selective only', phase: 'Nov' },
  { name: 'Algorithms', qs: 4, conf: 70.2, tier: 2, color: 'bg-blue-500', tc: 'text-blue-500 bg-blue-500/10 border-blue-500/20', time: 'Phase 2', topics: 'Asymptotic Analysis, MST ↑, Sorting, Graph Algos', phase: 'Jun–Jul' },
  { name: 'Databases', qs: 4, conf: 66.6, tier: 3, color: 'bg-purple-500', tc: 'text-purple-500 bg-purple-500/10 border-purple-500/20', time: 'Phase 4', topics: 'Normalization ↑, SQL, Concurrency, Relational Algebra', phase: 'Oct–Nov' },
  { name: 'Digital Logic', qs: 3, conf: 66.6, tier: 4, color: 'bg-amber-500', tc: 'text-amber-500 bg-amber-500/10 border-amber-500/20', time: 'Phase 4 light', topics: 'Boolean Algebra ↑, K-maps, Combinational circuits', phase: 'Nov' },
  { name: 'Compiler Design', qs: 3, conf: 63.3, tier: 4, color: 'bg-amber-500', tc: 'text-amber-500 bg-amber-500/10 border-amber-500/20', time: 'Phase 4 light', topics: 'Parsing, Syntax Directed Translation — focus only these 2', phase: 'Nov' },
  { name: 'Programming', qs: 2, conf: 69.8, tier: 4, color: 'bg-rose-500', tc: 'text-rose-500 bg-rose-500/10 border-rose-500/20', time: 'Phase 2 light', topics: 'Recursion only. Attempt NAT questions. Skip MCQs.', phase: 'Jul' },
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
  'Focus: Linear Algebra (Rising, 80.3% conf). Eigenvalues, rank, matrix ops. + GA daily. Target: complete Engg Math chapters 1–3.',
  'Focus: Probability (Rising, 78%) + Calculus. Bayesian probability, distributions. Calculus: limits, integration basics for CS applications.',
  'Focus: DS Basics — Linked Lists, Stacks, Queues, Trees. Build intuition before advanced structures. Graph Theory (Engg Math) also this month.',
  'Focus: Algorithms — Asymptotic Analysis (83.8%, highest in model), Sorting algorithms, MST (Rising, 81.1%). PYQ sprint every Friday.',
  'Focus: Advanced DS — BSTs (79.5%), Heaps (80.6%), Hashing (76.4%). Complete DS portion. Full section mock by end of month.',
  'Focus: OS — CPU Scheduling (82.8%), Process Synchronization (81.6%). These two alone cover most OS questions. Deep concept focus.',
  'Focus: OS Deadlock (79.4%) + Memory Management (76.1%). CO: Cache Memory (80.2%) + Pipelining (79.5%). Model predicted these perfectly in 2026.',
  'Focus: Theory of Computation — Finite Automata (81.8%), Regular Languages (79.2%). Databases — Normalization (Rising, 81.7%), SQL, Concurrency.',
  'Focus: Compiler Design — Parsing (82.2%), SDT (78.1%). Digital Logic — Boolean Algebra (Rising, 79.4%). Computer Networks selective topics.',
  'Focus: Full revision cycle — Engg Math → DS → Algorithms → OS → CO. 3 mock tests per week. Error analysis after every mock.',
  'Focus: PYQ solving by subject. Weak topic sprint. GA master practice. Full paper mocks. Aim: consistently scoring 58–62 on mocks.',
  '🎯 EXAM MONTH. Only revision. Formula sheets. 1 mock/week max. Sleep 8h. Exam day: GA first, NATs next, 2-mark MCQs last.',
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
  { id: 'm10', date: 'Jan 31, 2027', title: 'GATE-READY Milestone', desc: '3 full-paper mocks averaging 58+ marks. GA consistently scoring 13+/15. Rising topics fully polished. Exam is 2–4 weeks away.', items: ['Mock avg: 58+ marks','GA: 13+/15 consistent','Rising topics: mastered','NAT strategy: locked'], badge: '🎯 READY', btc: 'text-rose-500 border-rose-500 bg-rose-500/10' },
  { id: 'm11', date: 'Feb 2027', title: '🏆 GATE CSE 2027 — EXAM DAY', desc: 'GA first → NAT questions → 2-mark MCQs → 1-mark MCQs. Target 60+ raw marks. IIT Mandi CSE here we come.', items: ['GA strategy: 13+/15','NAT: attempt all','2-mark focus: OS, Algo, Math','Target raw: 60–65'], badge: '🎓 EXAM', btc: 'text-amber-400 border-amber-400 bg-amber-400/20' },
];

const days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];

const ttData: Record<string, string[][][]> = {
  "1": [
    // Mon Tue Wed Thu Fri Sat Sun
    [['Warm-up','Review last topic','c-green','mins-green'],['Warm-up','Review last topic','c-green','mins-green'],['Warm-up','Engg Math concept','c-green','mins-green'],['Warm-up','Review DS','c-green','mins-green'],['Warm-up','Mixed review','c-green','mins-green'],['Warm-up','Week summary','c-green','mins-green'],['Warm-up','Week recall','c-green','mins-green']],
    [['Linear Algebra','Matrices, rank, eigenvalues','c-blue','mins-blue'],['Linear Algebra','Systems of equations','c-blue','mins-blue'],['Probability','Conditional, Bayes','c-blue','mins-blue'],['Probability','Distributions, expectation','c-blue','mins-blue'],['PYQ Solve','Engg Math past papers','c-green','mins-green'],['Section Mock','Engg Math timed test','c-purple','mins-gray'],['DS: Trees','Binary trees, traversals','c-amber','mins-amber']],
    [['GA Practice','Verbal + Quant','c-amber','mins-amber'],['GA Practice','Verbal + Quant','c-amber','mins-amber'],['GA Practice','Verbal + Quant','c-amber','mins-amber'],['GA Practice','Verbal + Quant','c-amber','mins-amber'],['GA Practice','Verbal + Quant','c-amber','mins-amber'],['GA Practice','Full GA set','c-amber','mins-amber'],['GA Practice','Timed GA set','c-amber','mins-amber']],
    [['PYQ Sprint','2–3 LA questions','c-red','mins-gray'],['PYQ Sprint','2–3 LA questions','c-red','mins-gray'],['PYQ Sprint','2–3 Prob questions','c-red','mins-gray'],['PYQ Sprint','2–3 DS questions','c-red','mins-gray'],['Error Review','Fix mock mistakes','c-gray','mins-gray'],['Error Analysis','Review mock answers','c-gray','mins-gray'],['Plan Next Week','Topic tracker update','c-gray','mins-gray']],
  ],
  "2": [
    [['Warm-up','Algo concept recall','c-green','mins-green'],['Warm-up','Algo review','c-green','mins-green'],['Warm-up','DS advanced recall','c-green','mins-green'],['Warm-up','DS structures','c-green','mins-green'],['Warm-up','Mixed review','c-green','mins-green'],['Warm-up','Week summary','c-green','mins-green'],['Warm-up','Week recall','c-green','mins-green']],
    [['Asymptotic Analysis','Big-O, Theta, recurrences','c-blue','mins-blue'],['Master Theorem','Divide & Conquer','c-blue','mins-blue'],['BSTs','Operations, balancing, AVL','c-blue','mins-blue'],['Heaps','Min/max heap, heapify','c-blue','mins-blue'],['MST (Rising ↑)','Kruskal, Prim, analysis','c-green','mins-green'],['Algo Mock','Timed algorithm test','c-purple','mins-gray'],['Hashing','Hash functions, collision','c-amber','mins-amber']],
    [['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Full set','c-amber','mins-amber'],['GA Practice','Timed set','c-amber','mins-amber']],
    [['PYQ: Asymptotic','2–3 questions','c-red','mins-gray'],['PYQ: Sorting','2–3 sort questions','c-red','mins-gray'],['PYQ: BST','2–3 tree questions','c-red','mins-gray'],['PYQ: Heaps','2–3 heap questions','c-red','mins-gray'],['PYQ: MST','2–3 MST questions','c-red','mins-gray'],['Error Analysis','Review answers','c-gray','mins-gray'],['Plan Next Week','Update tracker','c-gray','mins-gray']],
  ],
  "3": [
    [['Warm-up','OS concept recall','c-green','mins-green'],['Warm-up','Scheduling review','c-green','mins-green'],['Warm-up','CO review','c-green','mins-green'],['Warm-up','Cache concepts','c-green','mins-green'],['Warm-up','Mixed review','c-green','mins-green'],['Warm-up','Week summary','c-green','mins-green'],['Warm-up','Week recall','c-green','mins-green']],
    [['CPU Scheduling (82.8%)','FCFS, SJF, Round Robin','c-blue','mins-blue'],['Process Sync (81.6%)','Semaphores, monitors','c-blue','mins-blue'],['Cache Memory (80.2%)','Mapping, replacement','c-amber','mins-amber'],['Pipelining (79.5%)','Hazards, forwarding','c-amber','mins-amber'],['Deadlock (79.4%)','Detection, avoidance, Banker','c-blue','mins-blue'],['OS+CO Mock','Timed section test','c-purple','mins-gray'],['Memory Mgmt (76.1%)','Paging, segmentation','c-blue','mins-blue']],
    [['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Full set','c-amber','mins-amber'],['GA Practice','Timed set','c-amber','mins-amber']],
    [['PYQ: Scheduling','2–3 sched Qs','c-red','mins-gray'],['PYQ: Sync','2–3 sync Qs','c-red','mins-gray'],['PYQ: Cache','2–3 cache Qs','c-red','mins-gray'],['PYQ: Pipelining','2–3 CO Qs','c-red','mins-gray'],['PYQ: Deadlock','2–3 DL Qs','c-red','mins-gray'],['Error Analysis','Review answers','c-gray','mins-gray'],['Plan Next Week','Update tracker','c-gray','mins-gray']],
  ],
  "4": [
    [['Warm-up','ToC recall','c-green','mins-green'],['Warm-up','DB review','c-green','mins-green'],['Warm-up','CD recall','c-green','mins-green'],['Warm-up','DL review','c-green','mins-green'],['Warm-up','CN review','c-green','mins-green'],['Warm-up','Week summary','c-green','mins-green'],['Warm-up','Week recall','c-green','mins-green']],
    [['Finite Automata (81.8%)','DFA, NFA, minimization','c-blue','mins-blue'],['Normalization (Rising ↑)','1NF–BCNF, FDs','c-green','mins-green'],['Parsing (82.2%)','LL, LR, LALR grammars','c-blue','mins-blue'],['Boolean Algebra (Rising ↑)','K-maps, simplification','c-green','mins-green'],['CN Selective','TCP/IP, routing basics','c-amber','mins-amber'],['Full Breadth Mock','All Phase 4 subjects','c-purple','mins-gray'],['Regular Languages (79.2%)','Regex, pumping lemma','c-blue','mins-blue']],
    [['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Full set','c-amber','mins-amber'],['GA Practice','Timed set','c-amber','mins-amber']],
    [['PYQ: ToC','2–3 automata Qs','c-red','mins-gray'],['PYQ: DBs','2–3 SQL/norm Qs','c-red','mins-gray'],['PYQ: CD','2–3 parsing Qs','c-red','mins-gray'],['PYQ: DL','2–3 boolean Qs','c-red','mins-gray'],['PYQ: CN','2–3 network Qs','c-red','mins-gray'],['Error Analysis','Deep review','c-gray','mins-gray'],['Plan Next Week','Update tracker','c-gray','mins-gray']],
  ],
  "5": [
    [['Warm-up','Engg Math rapid recall','c-green','mins-green'],['Warm-up','Algo recall','c-green','mins-green'],['Warm-up','OS recall','c-green','mins-green'],['Warm-up','Mixed recall','c-green','mins-green'],['Warm-up','Weak topic recap','c-green','mins-green'],['Warm-up','Full syllabus sweep','c-green','mins-green'],['Warm-up','Week recall','c-green','mins-green']],
    [['Revision: P1+P2','Engg Math + DS + Algo PYQs','c-blue','mins-blue'],['Full Mock Test','65Q timed, exam conditions','c-purple','mins-gray'],['Revision: P3','OS + CO, all topics','c-amber','mins-amber'],['Weak Topic Sprint','Your lowest-scoring topics','c-red','mins-gray'],['Revision: P4','ToC + DBs + CD + DL','c-blue','mins-blue'],['Full Mock Test','65Q, strict time limit','c-purple','mins-gray'],['GA Master Set','Full 15-mark GA timed','c-amber','mins-amber']],
    [['GA Practice','Daily set','c-amber','mins-amber'],['Error Analysis','Mock 1 deep review','c-gray','mins-gray'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','Daily set','c-amber','mins-amber'],['Error Analysis','Mock 2 deep review','c-gray','mins-gray'],['Plan + Score Log','Track mock scores','c-gray','mins-gray']],
    [['Rising Topics','Linear + MST + Norm review','c-green','mins-green'],['Error Pattern Log','Categorise mistake types','c-gray','mins-gray'],['NAT Practice','Identify + solve NATs fast','c-blue','mins-blue'],['PYQ Blitz','10 random past questions','c-red','mins-gray'],['Subject Balance','Shore up weak subjects','c-red','mins-gray'],['Score Tracker','Log mock performance','c-gray','mins-gray'],['Plan Next Week','Focus on gaps','c-gray','mins-gray']],
  ],
  "6": [
    [['Formula Sheet','Engg Math quick recall','c-green','mins-green'],['Formula Sheet','DS + Algo recall','c-green','mins-green'],['Formula Sheet','OS + CO recall','c-green','mins-green'],['Formula Sheet','ToC + DB recall','c-green','mins-green'],['Light Review','High-conf topics only','c-green','mins-green'],['Rest Day','Minimum study. Sleep!','c-gray','mins-gray'],['Exam Day ✓','Strategy + calm','c-amber','mins-amber']],
    [['Light Revision','Rising topics only','c-blue','mins-blue'],['Light Revision','High-conf topics','c-blue','mins-blue'],['Light Revision','OS + Algorithms','c-blue','mins-blue'],['Light Revision','Engg Math formulas','c-blue','mins-blue'],['Final Mock (last!)','Partial section only','c-purple','mins-gray'],['Rest completely','Walk, eat, sleep 9h','c-gray','mins-gray'],['🎯 GATE EXAM','GA → NAT → MCQ','c-green','mins-green']],
    [['GA Practice','Daily set','c-amber','mins-amber'],['GA Practice','10min easy set','c-amber','mins-amber'],['GA Practice','10min easy set','c-amber','mins-amber'],['GA Practice','10min easy set','c-amber','mins-amber'],['Error Analysis','Final mock review','c-gray','mins-gray'],['Nothing','Completely off','c-gray','mins-gray'],['Exam is on!','','c-green','mins-green']],
    [['Positive Recall','Things you know well','c-green','mins-green'],['Mental Prep','Visualise exam flow','c-gray','mins-gray'],['NAT Strategy','Review which topics have NATs','c-blue','mins-blue'],['Rest + Sleep','8–9 hours sleep tonight','c-gray','mins-gray'],['Light Reading','Formula sheet only','c-gray','mins-gray'],['Sleep 9 hours','Tomorrow is the exam','c-gray','mins-gray'],['Perform!','You prepared. Trust it','c-green','mins-green']],
  ],
};

export default function Roadmap() {
  const [warmupMins, setWarmupMins] = useState(10);
  const [deepworkMins, setDeepworkMins] = useState(45);
  const [gaMins, setGaMins] = useState(15);
  const [pyqMins, setPyqMins] = useState(20);
  const [ttPhase, setTtPhase] = useState("1");
  const [checkedMilestones, setCheckedMilestones] = useState<Record<string, Record<number, boolean>>>({});
  
  const totalMins = warmupMins + deepworkMins + gaMins + pyqMins;
  const dailyHours = totalMins / 60;

  useEffect(() => {
    const saved = localStorage.getItem('gate2027_milestones');
    if (saved) {
      setCheckedMilestones(JSON.parse(saved));
    }
  }, []);

  const toggleCheck = (mId: string, iIndex: number) => {
    const newChecked = { ...checkedMilestones };
    if (!newChecked[mId]) newChecked[mId] = {};
    newChecked[mId][iIndex] = !newChecked[mId][iIndex];
    setCheckedMilestones(newChecked);
    localStorage.setItem('gate2027_milestones', JSON.stringify(newChecked));
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
          Data-driven preparation plan built on ML model predictions (R² = 76.67%). <br/>
          {totalMins} minutes daily. Every session counts.
        </p>

        <div className="flex flex-wrap gap-6 mt-4">
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
            <span className="text-2xl font-mono font-bold text-primary">60+</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">Target Marks</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-mono font-bold text-primary">620+</span>
            <span className="text-xs text-muted-foreground uppercase tracking-wider">GATE Score</span>
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
                focus: 'Build the mathematical and structural foundation. Engg Math and DS basics form the bedrock for every subsequent technical subject. Linear Algebra is a Rising-trend topic.', 
                tags: [{t:'Linear Algebra ↑', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Probability ↑', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Calculus', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Graph Theory', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Linked Lists', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Trees', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Stacks & Queues', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'GA Daily', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}],
                color: 'text-emerald-500', bg: 'bg-emerald-500/5', border: 'border-emerald-500/20'
              },
              { num: '02', name: 'ALGORITHMS & DS', period: 'Jun 2026 – Jul 2026', badge: 'TIER 1', duration: 61, 
                focus: 'Advanced Data Structures and core Algorithms. MST is on a Rising trend — highest confidence among Algorithms topics. Asymptotic Analysis is the single highest-confidence topic.', 
                tags: [{t:'MST (81.1%) ↑', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Asymptotic 83.8%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'BSTs 79.5%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Heaps 80.6%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Hashing', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Sorting', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'DP Intro', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}],
                color: 'text-blue-500', bg: 'bg-blue-500/5', border: 'border-blue-500/20'
              },
              { num: '03', name: 'SYSTEMS', period: 'Aug 2026 – Sep 2026', badge: 'TIER 2', duration: 61, 
                focus: 'Operating Systems and Computer Organization — the two subjects the model predicted perfectly in 2026. Three OS topics have above 79% confidence. CO Cache & Pipelining are reliable.', 
                tags: [{t:'CPU Scheduling 82.8%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Process Sync 81.6%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Deadlock 79.4%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Memory Mgmt 76.1%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Cache Memory 80.2%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Pipelining 79.5%', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}],
                color: 'text-amber-500', bg: 'bg-amber-500/5', border: 'border-amber-500/20'
              },
              { num: '04', name: 'BREADTH', period: 'Oct 2026 – Nov 2026', badge: 'TIER 3', duration: 61, 
                focus: 'Complete remaining subjects: ToC, Databases, Compiler Design, Digital Logic, and Computer Networks. Focus on high-confidence topics only; don\'t go deep into low-confidence areas.', 
                tags: [{t:'Finite Automata 81.8%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Normalization ↑ 81.7%', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Parsing 82.2%', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Boolean Algebra ↑', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'SQL, Concurrency', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'CN: TCP/IP, Routing', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}],
                color: 'text-purple-400', bg: 'bg-purple-500/5', border: 'border-purple-500/20'
              },
              { num: '05', name: 'REVISION + MOCKS', period: 'Dec 2026 – Jan 2027', badge: 'CRITICAL', duration: 61, 
                focus: 'Full syllabus revision with mock tests 3× per week. Focus on PYQs for each topic. Identify weak spots and target them with focused 30-min sessions. GA should score 13+/15 by now.', 
                tags: [{t:'Full PYQ Solve', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Mock Tests 3×/week', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Rising Topics Review', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'GA Master', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Weak Topic Sprint', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'NAT Practice', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}],
                color: 'text-rose-500', bg: 'bg-rose-500/5', border: 'border-rose-500/20'
              },
              { num: '06', name: 'FINAL SPRINT', period: 'Feb 2027 · ~3 weeks', badge: 'EXAM', duration: 21, 
                focus: 'NO new topics. Light revision only. One full mock per week max. Focus on formula sheets, quick-recall drills. Sleep 8 hours. Exam day: GA first, then NATs, then 2-mark MCQs.', 
                tags: [{t:'Formula Sheets Only', c:'border-emerald-500/30 text-emerald-500', dot:'bg-emerald-500'}, {t:'Light Mock ×1/week', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'High-Conf Topics', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}, {t:'Mental Prep', c:'border-amber-500/20 text-amber-400', dot:'bg-amber-400'}, {t:'Sleep + Rest', c:'border-blue-500/30 text-sky-400', dot:'bg-sky-400'}],
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
              <p className="text-sm text-muted-foreground mt-2">Each day = {totalMins} minutes. Dynamically updates based on Phase.</p>
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
              
              {['WARM-UP', 'DEEP WORK', 'GA PRACTICE', 'PYQ SPRINT'].map((slotName, rowIdx) => {
                const rowData = ttData[ttPhase][rowIdx];
                const customMins = [warmupMins, deepworkMins, gaMins, pyqMins][rowIdx];
                
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
            <p className="text-sm text-muted-foreground mt-2">Adjust your daily study distribution. Total time scales automatically across the roadmap.</p>
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

                <div className="pt-6 border-t border-border">
                  <div className="flex w-full h-8 rounded-md overflow-hidden bg-sidebar-border border border-border">
                    <div style={{ width: `${(warmupMins/totalMins)*100}%` }} className="bg-emerald-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{warmupMins}m</div>
                    <div style={{ width: `${(deepworkMins/totalMins)*100}%` }} className="bg-blue-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{deepworkMins}m</div>
                    <div style={{ width: `${(gaMins/totalMins)*100}%` }} className="bg-amber-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{gaMins}m</div>
                    <div style={{ width: `${(pyqMins/totalMins)*100}%` }} className="bg-rose-500/80 flex items-center justify-center font-mono text-[10px] text-zinc-900 font-bold overflow-hidden transition-all">{pyqMins}m</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="space-y-4">
              <Card className="bg-card">
                <CardHeader className="py-4">
                  <CardTitle className="text-sm font-mono text-muted-foreground uppercase tracking-widest">Standard Study Day</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center gap-4 py-2 border-b border-border/50">
                    <div className="w-1.5 h-8 rounded-full bg-emerald-500"></div>
                    <div className="flex-1">
                      <div className="text-sm font-bold text-emerald-500">Warm-Up ({warmupMins}m)</div>
                      <div className="text-xs text-muted-foreground mt-1">Revise yesterday's notes. 2–3 key concepts. Don't open new material.</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 py-2 border-b border-border/50">
                    <div className="w-1.5 h-8 rounded-full bg-blue-500"></div>
                    <div className="flex-1">
                      <div className="text-sm font-bold text-blue-500">Deep Work Block ({deepworkMins}m)</div>
                      <div className="text-xs text-muted-foreground mt-1">New concept or problem-set for today's topic. No distractions.</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 py-2 border-b border-border/50">
                    <div className="w-1.5 h-8 rounded-full bg-amber-500"></div>
                    <div className="flex-1">
                      <div className="text-sm font-bold text-amber-500">GA Practice ({gaMins}m)</div>
                      <div className="text-xs text-muted-foreground mt-1">Daily GA regardless of phase. Verbal + quantitative problems.</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 py-2">
                    <div className="w-1.5 h-8 rounded-full bg-rose-500"></div>
                    <div className="flex-1">
                      <div className="text-sm font-bold text-rose-500">PYQ Sprint ({pyqMins}m)</div>
                      <div className="text-xs text-muted-foreground mt-1">Solve previous year questions on today's topic. Mark doubts.</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-amber-500/10 border-amber-500/20">
                <CardContent className="p-4 flex gap-4 items-start">
                  <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                  <div>
                    <div className="text-sm font-bold text-amber-500">Key Rule</div>
                    <div className="text-xs text-muted-foreground mt-1">Never skip the GA block. Even on hard subject days. GA = guaranteed 13+ marks if practiced daily for a year.</div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="subjects" className="space-y-6">
          <div className="mb-4">
            <h2 className="text-xl font-bold flex items-center gap-3 border-l-4 border-primary pl-3">Subject Priority Map</h2>
            <p className="text-sm text-muted-foreground mt-2">Ordered by predicted 2027 weightage × confidence score. Bar = proportion of total paper.</p>
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
              <p className="text-sm text-muted-foreground mt-2">Check off achievements as you go. Progress is saved locally in your browser.</p>
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
              { icon: TrendingUp, title: 'Linear Algebra is Your Secret Weapon', text: 'Recent average jumped from 2.88 → 4.33 questions, with a Rising trend and 80.3% confidence. This single topic could swing 6–8 marks.', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
              { icon: Target, title: 'NAT-First Exam Strategy', text: 'In the exam hall, identify and attempt ALL NAT questions first. They have zero negative marking. Target under 30 seconds per identification.', color: 'text-blue-500', bg: 'bg-blue-500/10' },
              { icon: AlertTriangle, title: 'The Calibration Inversion Warning', text: 'Topics in the 65–80% confidence band have HIGHER real accuracy (80–87%) than the 80%+ band. Don\'t obsess over top-confidence topics alone.', color: 'text-amber-500', bg: 'bg-amber-500/10' },
              { icon: TrendingUp, title: 'Rising Trend Topics', text: 'Linear Algebra, Probability, MST, Normalization, Boolean Algebra. Prepare them as if they are 2-mark question sources.', color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
              { icon: TrendingUp, title: 'Declining vs Rising', text: 'Sorting (Algo) and Verbal Ability (GA) show Declining trends. Don\'t skip them, but balance your time investment accordingly.', color: 'text-rose-500', bg: 'bg-rose-500/10' },
              { icon: CheckCircle2, title: 'GA = 13+/15. Non-Negotiable.', text: 'Model correctly predicted 11 questions vs 10 actual. 15 mins daily = ~91 hours of GA over the year. Best ROI in the paper.', color: 'text-primary', bg: 'bg-primary/10' },
              { icon: BookOpen, title: 'Asymptotic Analysis: 83.8% Conf', text: 'Single highest-confidence topic. Deep mastery here is guaranteed marks. Cover recurrences, Master Theorem, Akra-Bazzi.', color: 'text-blue-500', bg: 'bg-blue-500/10' },
              { icon: RefreshCw, title: 'Spaced Repetition Schedule', text: 'Tier 1 subjects: revise every 2 weeks. Tier 2: every 3 weeks. Tier 3: every 4 weeks. Blocks forgetting curve decay.', color: 'text-purple-500', bg: 'bg-purple-500/10' },
              { icon: Brain, title: 'Phase 5 is Where Ranks are Made', text: 'Starting revision in December gives a 2-month head start. Do 3 full-length mock tests per week minimum.', color: 'text-rose-500', bg: 'bg-rose-500/10' },
              { icon: AlertTriangle, title: 'Data Structures Volatility', text: 'DS remains the most volatile subject. Don\'t skip it, but don\'t over-rely on its predicted count. Focus on conceptual mastery.', color: 'text-amber-500', bg: 'bg-amber-500/10' },
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
