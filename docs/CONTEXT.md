# 📄 PROJECT CONTEXT DOCUMENT v2.0
## "LLM-Powered Recursion Learning Workflow"

**Purpose:** Quick onboarding for future Claude sessions on this project

**Document Status:** Post-Research Phase - Master Guide Complete  
**Last Updated:** After finalizing Master Guide (all 10 parts)  
**Supersedes:** Context v1.0 (research questions phase)

---

## 🎯 PROJECT OVERVIEW

**What I'm Building:**  
An LLM-augmented learning workflow to master recursion algorithms from an open-source Python book. Instead of passively reading dense algorithmic code, I'm using LLMs to instrument code with educational print statements, then stepping through it with VS Code debugger to observe execution in real-time.

**Core Innovation:**  
Combining three elements: (1) LLM prompt engineering for code instrumentation, (2) VS Code debugger for step-by-step execution, (3) strategic print statements for narrating algorithm logic.

**Current Status:**  
- ✅ Research phase COMPLETE (3 research questions investigated)
- ✅ Master Guide finalized (`recursion_debug_master.md` - 10 parts)
- ✅ Proven workflow on Chapter 4 (Interval Problems - divide-and-conquer)
- 🎯 NOW ENTERING: Application phase - using Master Guide across remaining chapters

---

## 📚 LEARNING CONTEXT

**Book Structure:** 8-module recursion course covering:
1. ✅ Recursion Foundations (linear recursion)
2. ✅ List Recursion Patterns
3. ✅ Divide and Conquer
4. **🎯 Recursive Problem Solving** ← Currently here (Chapter 4)
5. ⏭️ Tree Recursion
6. ⏭️ Advanced Recursion Patterns (memoization, tail recursion)
7. ⏭️ Backtracking
8. ⏭️ Recursion in Practice

**Learning Approach:**  
Using Master Guide as primary reference for:
- Debugging technique selection (Parts 1, 6)
- Instrumentation patterns (Parts 2, 7)
- Visualization tools (Part 3)
- Troubleshooting (Parts 5, 8)
- Progress validation (Parts 4, 9)

---

## 💪 MY STRENGTHS (Self-Assessment)

### Strong Areas (7-10/10):
- **LLM Prompt Engineering (8/10):** Can orchestrate LLMs to solve technical problems
- **Automated Code Transformation (8/10):** Conceptually understand batch processing
- **Educational Content Generation (8/10):** Effective at prompting LLMs for explanations
- **Workflow Repeatability (8/10):** Built reusable Master Guide for future learning
- **VS Code Debugging (5→7/10):** Significantly improved after research - now comfortable with watch expressions, conditional breakpoints, logpoints, call stack navigation

### Weak Areas (Still 2-4/10):
- **Debug Configuration (2→3/10):** Still rely on LLMs for `launch.json`, but understand structure better
- **Managing Multiple Versions (3/10):** Not a priority - focus is understanding, not preservation

### Evolved Understanding:
- **Visualizing Recursion Patterns (5→7/10):** Now have clear framework (Pattern Library in Master Guide Part 2)
- **Translating Debug Insights to Mental Models (6→8/10):** Validation framework in Part 4 provides structure

---

## 🎯 PROJECT GOALS & SUCCESS CRITERIA

**Primary Goal:**  
✅ **ACHIEVED:** Discovered debugging techniques and instrumentation patterns beyond print statements

**New Primary Goal:**  
Apply Master Guide workflow across all 8 book modules to validate universality and refine patterns

**Success Looks Like:**
- ✅ Working workflow for 5-10 examples (DONE - Chapter 4)
- ✅ Reusable prompt templates (DONE - Part 7 of Master Guide)
- ✅ 3+ game-changing debugging techniques (DONE - watch expressions, conditional breakpoints, logpoints, call stack navigation)
- ✅ Pattern library for all recursion types (DONE - Part 2 + Part 6)
- 🎯 NEW: Validate patterns work for Trees (Ch 5), DP (Ch 6), Backtracking (Ch 7)

---

## 📖 MASTER GUIDE REFERENCE

**Primary Document:** `recursion_debug_master.md`

**Quick Navigation by Need:**

| If You Need... | Go To... |
|----------------|----------|
| **Debugging techniques for recursion** | Part 1: VS Code Debugging Arsenal |
| **What to instrument for [recursion type]** | Part 2: Instrumentation Pattern Library |
| **Visual tools to try** | Part 3: Zero-Friction Visualization Tools |
| **Am I actually learning?** | Part 4: Learning Validation Framework |
| **Stuck/confused** | Part 5 & 8: Common Blockers & Troubleshooting |
| **Chapter-specific guidance** | Part 6: Chapter-Specific Quick Reference |
| **Prompt templates for LLMs** | Part 7: Workflow Optimization Strategies |
| **Progress tracking** | Part 9: Success Metrics & Iteration Guide |
| **Quick copy-paste patterns** | Part 10: Reference Resources |

**Core Patterns (Quick Reference):**
- Linear Recursion: Track input parameter, base case, return value
- Divide & Conquer: Track split point, subproblem bounds, merge results
- Tree Recursion: Track node, path, depth, branches
- Backtracking: Track state, choices, constraints, undo points
- DP/Memoization: Track cache hits/misses, subproblem keys, transitions

---

## 🛠️ CURRENT WORKFLOW

**Standard Algorithm Learning Process:**

1. **Prepare** (2 min)
   - Identify recursion type from code structure
   - Check Master Guide Part 2 for pattern
   - Review Part 6 for chapter-specific tips

2. **Instrument** (5 min)
   - Use LLM with prompt template from Part 7
   - Apply instrumentation pattern from Part 10 (copy-paste)
   - Generate/update `.vscode/launch.json` if needed

3. **Debug** (10-15 min)
   - Start with F5 + F11 (basic stepping)
   - Add watch expressions for key variables
   - Set conditional breakpoints on base cases
   - Use logpoints for decision points
   - Navigate call stack to understand depth

4. **Validate** (5 min)
   - Run tests from Part 4: Prediction, Drawing, Explanation, Modification
   - Score progress (green flags vs red flags)
   - Document what worked in personal notes

5. **Iterate**
   - If confused: Check Part 8 troubleshooting
   - If clear: Reduce instrumentation, move to next example
   - Weekly: Review Part 9 iteration strategy

---

## 🔧 TECHNICAL STACK & TOOLS

**Primary Tools:**
- VS Code with Python extension
- Built-in VS Code debugger (watch, breakpoints, logpoints, call stack)
- Python Tutor (pythontutor.com) - zero-setup visualization
- LLMs for code instrumentation and prompt assistance

**Optional Enhancements:**
- Debug Visualizer (VS Code extension) - installed but selective use
- recursion-visualiser (Python library) - available if needed, requires Graphviz

**Tool Selection Criteria:**
- ✅ Free/open-source
- ✅ Low/zero setup friction
- ✅ Complements workflow without replacing core techniques
- ❌ Complex configuration or steep learning curves

---

## ⚡ QUICK START FOR RESUMING WORK

**Essential Context Questions:**

1. **Where am I in the book?**
   - Current chapter/module
   - Specific algorithm being studied

2. **What's my current blocker?**
   - Stuck on understanding
   - Tool friction
   - Pattern unclear

3. **What have I tried?**
   - Which debugging techniques from Part 1
   - Which instrumentation pattern from Part 2
   - Any visualization tools from Part 3

**Immediate Actions:**

```
📖 Open Master Guide → Navigate to relevant part
🔍 If stuck → Check Part 8 troubleshooting first
🎯 If new algorithm → Use Part 6 chapter guide + Part 2 pattern
💬 If prompting LLM → Use templates from Part 7
📊 If checking progress → Review Part 9 metrics
```

---

## 🚫 EXPLICITLY OUT OF SCOPE

**Still Not Worried About:**
1. Comparative debugging (original vs. instrumented code)
2. Persistent learning artifacts (recordings, annotations)
3. Testing/validation layer for LLM output
4. Managing multiple code versions
5. Premature batch processing of all examples

**Why These Remain Out of Scope:**
- Goal is understanding, not code preservation
- Real-time comprehension > archival
- 2% bug rate acceptable for 30% learning acceleration
- Master Guide provides structure without heavy tooling
- Deliberate deep learning before scaling

---

## 📊 RESEARCH OUTCOMES (ARCHIVED)

**Three Research Questions Investigated:**

✅ **Q1: VS Code Debugging Features**  
→ Delivered: Watch expressions, conditional breakpoints, logpoints, call stack navigation  
→ Documented: Master Guide Part 1

✅ **Q2: Instrumentation Patterns by Recursion Type**  
→ Delivered: Pattern library for 5 recursion types with specific state variables, decision points, flow insights  
→ Documented: Master Guide Part 2 + Part 6 (chapter-specific)

✅ **Q3: Zero-Friction Visualization Tools**  
→ Delivered: Python Tutor (1/10 friction), Debug Visualizer (2/10), recursion-visualiser (5/10)  
→ Documented: Master Guide Part 3

**Research Artifacts (Historical Reference Only):**
- `RQ1/`, `RQ2/`, `RQ3/` - LLM research outputs
- `RESEARCH_PLAN.md` - Original research questions
- `LLM_ANSWERS_TO_RQS.txt` - Raw research findings

**Note:** These files are now superseded by Master Guide. Refer to Master Guide for all practical usage.

---

## 🎯 CURRENT PHASE: APPLICATION & VALIDATION

**Phase Status:** Post-Research → Active Application

**Immediate Goals:**
1. Apply Master Guide workflow to next 2-3 algorithms in Chapter 4
2. Begin Chapter 5 (Tree Recursion) using Part 6 preparation guide
3. Validate instrumentation patterns work across different recursion types
4. Refine personal notes section in Master Guide with real usage insights

**Success Criteria for This Phase:**
- ✅ Master Guide patterns work without modification for 80% of cases
- ✅ Debugging time stays under 15 minutes per algorithm
- ✅ Learning validation tests (Part 4) consistently show 3+ green flags
- ⚠️ Identify any gaps in patterns requiring Master Guide updates

**When to Update Master Guide:**
- Found a pattern that doesn't work as documented
- Discovered a new debugging technique not covered
- Hit a blocker not addressed in troubleshooting sections
- Chapter-specific insights that would help future you

---

## 📝 PERSONAL NOTES SECTION

**Usage:** Add your own findings as you work through chapters

**Template:**
```markdown
### [Date] - [Chapter/Algorithm]

**Recursion Type:** [Linear/D&C/Tree/Backtracking/DP]

**Master Guide Sections Used:**
- Part [X]: [What you referenced]

**What Worked:**
- [Specific technique/pattern that helped]

**What Didn't Work:**
- [Where Master Guide fell short]

**Adjustments Made:**
- [How you adapted the pattern]

**Learning Validation Score:** [X/4 green flags]

**Time to Understanding:** [X minutes]

**Notes for Future:**
- [Insight that would help next time]
```

---

## 🔄 ITERATION & UPDATES

**Master Guide Update Triggers:**

1. **Pattern Failure** (High Priority)
   - Documented pattern doesn't work for specific case
   - → Update Part 2 pattern or add caveat

2. **New Technique Discovery** (Medium Priority)
   - Found a debugging feature not in Part 1
   - → Add to techniques section

3. **Workflow Friction** (Medium Priority)
   - Step in workflow consistently takes too long
   - → Update Part 7 optimization strategies

4. **Tool Issues** (Low Priority)
   - Recommended tool causes problems
   - → Update Part 3 with warning/alternative

**Version Control:**
- Keep Master Guide as single source of truth
- Add version notes at top when making significant updates
- Archive old versions if major restructure needed

---

## 🎓 LEARNING PHILOSOPHY

**Core Principles:**
1. **Active over Passive:** Step through code, don't just read it
2. **Visual over Abstract:** Use tools to make recursion concrete
3. **Iterative over Perfect:** Quick instrumentation → test → refine
4. **Guided over Manual:** Let LLMs handle boilerplate, focus on understanding
5. **Validated over Assumed:** Use objective tests (Part 4) to confirm learning

**When Stuck:**
- Simplify the input first
- Check Master Guide troubleshooting (Part 8)
- Try Python Tutor for quick visualization
- Ask: "What's the ONE thing blocking my understanding?"

**When Confident:**
- Reduce instrumentation gradually
- Try predicting execution before running
- Teach the concept (rubber duck or note-taking)
- Move to harder example

---

## 📚 REFERENCE FILES

**Primary Reference:**
- `recursion_debug_master.md` - Complete workflow guide (10 parts)

**Code Examples:**
- `02.py` - Example of LLM-instrumented code
- `02_original.py` - Original recursive algorithm from book
- `.vscode/launch.json` - Debug configuration template

**Historical/Archive:**
- `CONTEXT.md` (v1.0) - Previous context document
- `RESEARCH_PLAN.md` - Original research questions
- `RQ1/`, `RQ2/`, `RQ3/` - Research outputs (superseded by Master Guide)

---

## 🚀 QUICK COMMANDS

**Start Debugging Session:**
```bash
# 1. Open algorithm file in VS Code
# 2. F5 to start debugging
# 3. F11 to step into recursive calls
# 4. Check Master Guide Part 1 for advanced techniques
```

**Instrument New Algorithm:**
```python
# Use LLM prompt from Master Guide Part 7:
"Add instrumentation to this recursive function following the 
[Linear/D&C/Tree/Backtracking/DP] pattern from the Master Guide. 
Focus on [specific aspect]."
```

**Quick Pattern Lookup:**
```markdown
# Master Guide Part 10 has copy-paste patterns for all 5 types
# Part 2 has detailed "what to instrument" for each type
# Part 6 has chapter-specific examples
```

---

**Document Version:** 2.0 (Post-Research)  
**Status:** Active Application Phase  
**Next Review:** After completing Chapter 5 (Tree Recursion) to validate pattern universality

---

## 🎯 TL;DR FOR CLAUDE

**In 3 Sentences:**
I'm mastering recursion using LLM-assisted code instrumentation + VS Code debugging. I've completed research phase and built a comprehensive Master Guide (`recursion_debug_master.md`) with debugging techniques, instrumentation patterns, and troubleshooting. Now applying this workflow across an 8-module recursion course, currently on Chapter 4 (Divide & Conquer), validating patterns work universally.

**What Claude Needs to Know:**
1. **Primary Reference:** Master Guide (10 parts) - check it first for any question
2. **Current Focus:** Applying proven workflow to remaining book chapters
3. **Help Needed:** Troubleshooting when patterns don't work, refining techniques, validating learning

**Don't Waste Time On:**
- Explaining basic recursion concepts (I have the book)
- Suggesting tools not in Master Guide (already researched)
- Recreating what's in Master Guide (just reference it)

**Do Help With:**
- Applying Master Guide to specific algorithms
- Debugging workflow issues
- Validating if I'm actually learning (Part 4 tests)
- Updating Master Guide when patterns fail