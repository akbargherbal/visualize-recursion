# CONTEXT.md - Interactive Recursion Visualizer Project

## 🎯 Project Vision

**Goal**: Build a web-based tool that visualizes recursive algorithm execution step-by-step, with problem-specific visualizations that make recursion intuitive.

**Inspiration**: Python Tutor (pythontutor.com) but **domain-specific** rather than universal
- Python Tutor shows generic stack frames → abstract
- Our tool shows problem-specific visualizations → concrete and intuitive

**Target User**: Self-learning developers working through recursion algorithms (like the user working through a recursion course, currently on Chapter 4)

---

## 📋 Project Status

**Current State**: Ideation & Architecture Planning (Session 1)

**Decisions Made**:
- ✅ Tech stack: Flask + HTMX + Alpine.js + Tailwind CSS
- ✅ Execution model: Pre-computation (run algorithm once, capture trace, replay)
- ✅ State storage: Flask session (with server-side storage for larger traces)
- ✅ First algorithm: Overlapping Intervals (from `overlapping_intervals.py`)

**Decisions Pending**:
- ⏳ Code highlighting approach (Pygments vs. manual CSS)
- ⏳ Input customization (fixed test cases vs. user input form)
- ⏳ Routing architecture (hardcoded vs. dynamic registration)
- ⏳ Timeline visualization library (SVG, Canvas, or HTML+CSS)

---

## 🏗️ Architecture Overview

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User navigates to /problem/overlapping-intervals         │
│    └─> Flask runs algorithm ONCE with instrumentation       │
│    └─> Captures execution trace (list of step dicts)        │
│    └─> Stores trace in Flask session                        │
│    └─> Renders initial page with step 0                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. User clicks "Next" button                                 │
│    └─> HTMX sends GET /step/<n>                             │
│    └─> Flask retrieves trace[n] from session                │
│    └─> Returns HTML partial (just the updated sections)     │
│    └─> HTMX swaps content in place                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Visualization updates                                     │
│    └─> Timeline redraws with new highlighted interval       │
│    └─> Code view highlights current line                    │
│    └─> Variables panel shows updated state                  │
│    └─> Call stack shows current depth                       │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack Rationale

| Technology | Why Chosen | User's Experience Level |
|------------|-----------|------------------------|
| **Flask** | Familiar, simple routing, good for server-heavy pattern | B-level (Intermediate) |
| **HTMX** | Minimal JS, server-driven updates, aligns with user preference | B-level |
| **Alpine.js** | Lightweight interactivity (e.g., keyboard shortcuts) | B-level |
| **Tailwind CSS** | Rapid prototyping, utility-first | C-level (Basic) |

**Key Principle**: Keep complexity on the server (Python), minimize frontend logic (user's comfort zone)

---

## 📊 Data Structures

### Trace Step Format

Each step in the execution trace is a dictionary:

```python
{
    "step": 3,                          # Step number (0-indexed)
    "depth": 1,                         # Recursion depth
    "function": "filter_covered",       # Function name
    "args": {                           # Current function arguments
        "remaining": [(600, 720), (900, 960)],
        "max_end_so_far": 720
    },
    "current_line": 45,                 # Line number in source code
    "action": "Examining (600, 720)",   # Human-readable action
    "decision": "COVERED because 720 ≤ 720",  # Explanation
    "result": None,                     # Return value (None if not returning yet)
    
    # Algorithm-specific visualization data
    "intervals_state": [
        {
            "interval": (540, 720),
            "status": "kept",           # kept | examining | pending | removed
            "opacity": 1.0
        },
        {
            "interval": (600, 720),
            "status": "examining",
            "opacity": 0.6
        },
        {
            "interval": (900, 960),
            "status": "pending",
            "opacity": 0.3
        }
    ],
    
    # Visualization rendering hints
    "visualization_data": {
        "timeline_start": 500,          # Timeline axis start
        "timeline_end": 1000,           # Timeline axis end
        "highlight_y": 1                # Which row to highlight
    },
    
    # Call stack snapshot
    "call_stack": [
        {"function": "filter_covered", "depth": 0, "args": "..."},
        {"function": "filter_covered", "depth": 1, "args": "..."}
    ]
}
```

### Session Storage

```python
session = {
    'trace': [step0, step1, step2, ...],  # Full execution trace
    'current_step': 3,                     # Currently displayed step
    'algorithm': 'overlapping-intervals',  # Algorithm identifier
    'input_data': [(540, 660), ...],       # Original input
    'metadata': {
        'total_steps': 12,
        'total_calls': 5,
        'max_depth': 3
    }
}
```

---

## 🎨 UI Layout Design

### Four-Pane Layout

```
┌───────────────────────────────────────────────────────────────┐
│  Header: Problem Title + Controls                             │
│  [◀ Prev] [▶ Next] [⟲ Reset] [⏭ Jump to End]  Step 3/12     │
├────────────────────────┬──────────────────────────────────────┤
│                        │                                      │
│  Code View             │  Timeline Visualization              │
│  (Syntax highlighted)  │  (Problem-specific)                  │
│  Current line marked   │                                      │
│  with → or highlight   │  For intervals: Timeline bars        │
│                        │  For trees: Tree structure           │
│  def filter_covered:   │  For backtracking: Board state       │
│ >  current = rem[0]    │                                      │
│    if current[1] <= .. │  [====interval====]                  │
│                        │     [====interval====]               │
│                        │  [========interval========]          │
│                        │  Current: (600, 720) - COVERED       │
├────────────────────────┼──────────────────────────────────────┤
│  Variables Panel       │  Call Stack                          │
│  remaining: [(600...)] │  1. filter([4 intervals], -∞)        │
│  max_end_so_far: 720   │  2. filter([2 intervals], 720) ← YOU │
│  current: (600, 720)   │                                      │
├────────────────────────┴──────────────────────────────────────┤
│  Explanation Box                                               │
│  "Examining interval (600, 720). Since end=720 is not greater │
│   than max_end_so_far=720, this interval is COVERED. It will  │
│   be skipped and not included in the result."                 │
└───────────────────────────────────────────────────────────────┘
```

### Responsive Considerations

- Desktop (>=1024px): Four-pane layout as shown
- Tablet (768-1023px): Stack top two panes, bottom two panes
- Mobile (<768px): Tabs to switch between Code/Visualization/Stack

---

## 🔧 Implementation Phases

### Phase 1: MVP - Single Algorithm (3-4 hours)

**Scope**: Overlapping Intervals only, hardcoded test case

**Deliverables**:
1. Flask app with routes:
   - `GET /` → Landing page with algorithm list
   - `GET /problem/overlapping-intervals` → Initialize trace, render step 0
   - `GET /problem/overlapping-intervals/step/<n>` → Return step partial

2. Tracer class:
   ```python
   class OverlappingIntervalsTracer:
       def run(self, intervals):
           # Instrumented version of algorithm
           # Captures step dicts during execution
           return trace  # List[dict]
   ```

3. Basic UI:
   - Next/Prev buttons working
   - Code view with current line highlight
   - Timeline visualization (simple HTML bars)
   - Variables panel

**Success Criteria**:
- Can navigate through all steps
- Timeline updates correctly
- Code highlight moves
- No session issues

### Phase 2: Refinement (2-3 hours)

**Enhancements**:
- Keyboard navigation (arrow keys, spacebar)
- Jump to specific step
- Better timeline visualization (SVG or Canvas)
- Syntax highlighting for code
- Improved explanation text

**Success Criteria**:
- UX feels smooth
- Visualizations are clear and helpful
- Explanations are educational

### Phase 3: Second Algorithm (3-4 hours)

**Scope**: Add another algorithm (e.g., Tree Traversal or Merge Sort)

**Work**:
- Refactor to `AlgorithmTracer` base class
- Dynamic routing system
- Algorithm registry
- New visualization type (tree or split/merge diagram)

**Success Criteria**:
- Two algorithms working
- Easy to add third algorithm
- Code is DRY and maintainable

### Phase 4: User Input & Polish (2-3 hours)

**Features**:
- Form to input custom test cases
- Save/share trace URLs
- Dark mode toggle
- Performance optimization

---

## ⚠️ Known Challenges & Pitfalls

### 1. Session Storage Limits

**Problem**: Flask default session uses cookies (4KB limit)

**Solution**: Use `flask-session` with filesystem or Redis backend
```python
from flask_session import Session

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_sessions'
Session(app)
```

**Estimate**: 50 steps × 2KB = 100KB per trace (too big for cookies)

### 2. Trace Capture Complexity

**Problem**: How to instrument existing algorithm to capture steps?

**Options**:

**A. Decorator-based tracing** (automatic but less control)
```python
@trace_recursion
def filter_covered(remaining, max_end):
    # Original code unchanged
    pass
```

**B. Manual instrumentation** (more work but precise)
```python
def filter_covered(remaining, max_end, trace=[]):
    trace.append(capture_state())
    # ... algorithm logic with trace.append() at key points
```

**Recommendation**: Start with B (manual) for precision, refactor to A if pattern emerges

### 3. Code Highlight Synchronization

**Problem**: Mapping execution steps to source code line numbers

**Challenge**: 
- Tracer captures step at runtime
- Need to know which line of source code corresponds to that step
- Python's `inspect` module can help but adds complexity

**Options**:
- Store line numbers manually in instrumented code
- Use `sys.settrace()` to capture line numbers automatically (heavy)
- Use frame inspection: `inspect.currentframe().f_lineno`

**Recommendation**: Manual line number tracking in trace step dict for MVP

### 4. Visualization Complexity

**Problem**: Each algorithm needs different visualization

**Timeline for Intervals**:
```html
<svg width="600" height="200">
  <rect x="54" y="20" width="66" height="20" fill="green" opacity="1.0"/>
  <rect x="60" y="50" width="72" height="20" fill="red" opacity="0.6"/>
  <!-- etc -->
</svg>
```

**Tree for Tree Traversal**:
```html
<div class="tree-node" style="--depth: 0">
  <div class="node-value">5</div>
  <div class="children">
    <div class="tree-node" style="--depth: 1">...</div>
  </div>
</div>
```

**Strategy**: Create template partials per algorithm
```
templates/
  visualizations/
    overlapping_intervals.html
    tree_traversal.html
    merge_sort.html
```

### 5. Performance with Large Traces

**Problem**: 100+ steps could make session heavy

**Solutions**:
- Limit trace length (truncate very deep recursion)
- Lazy loading (only load steps as needed)
- Compression (gzip trace before storing in session)

**For MVP**: Limit to algorithms with <50 steps, defer optimization

### 6. Browser Back Button

**Problem**: HTMX updates without changing URL → back button doesn't work as expected

**Solutions**:
- Use `hx-push-url="true"` to update URL with step number
- Or: Explicitly handle with Alpine.js state management

**Recommendation**: Add `hx-push-url="/problem/overlapping-intervals/step/{step}"` to Next/Prev buttons

---

## 🎯 Success Metrics

### MVP Success Criteria

- [ ] Can load algorithm and see step 0
- [ ] Next/Prev buttons navigate through trace
- [ ] Code highlight follows execution
- [ ] Visualization updates correctly
- [ ] Variables panel shows current state
- [ ] Call stack shows recursion depth
- [ ] No session errors or data loss
- [ ] Smooth UX (no flicker, no lag)

### Educational Value Metrics

**How to measure if this actually helps learning**:

1. **Clarity Test**: Can user predict next step after watching 5 steps?
2. **Insight Test**: Does visualization reveal "aha moments" (e.g., "oh, that's why it's covered!")?
3. **Retention Test**: After using tool, can user explain algorithm without it?

**User Feedback Questions**:
- Is this clearer than print statements?
- Is this clearer than Python Tutor?
- What's still confusing?
- What would you add/change?

---

## 🗺️ Roadmap

### Immediate Next Session (Session 2)

**Goal**: Build working MVP with Overlapping Intervals

**Tasks**:
1. Set up Flask project structure
2. Implement `OverlappingIntervalsTracer` class
3. Create base template with four-pane layout
4. Wire up Next/Prev with HTMX
5. Basic timeline visualization (HTML bars)
6. Test with sample input

**Time Estimate**: 3-4 hours

**Deliverable**: Working prototype where you can step through execution

### Future Sessions

**Session 3**: Refinement & Polish
- Better visualizations
- Keyboard shortcuts
- Improved explanations

**Session 4**: Second Algorithm
- Choose algorithm (Tree Traversal or Merge Sort)
- Refactor to base class
- New visualization type

**Session 5**: User Input & Sharing
- Custom input form
- URL-based trace sharing
- Dark mode

---

## 📁 Proposed File Structure

```
recursion-visualizer/
├── app.py                          # Flask application
├── requirements.txt                # Dependencies
├── config.py                       # Configuration
│
├── algorithms/                     # Algorithm implementations
│   ├── __init__.py
│   ├── base.py                     # AlgorithmTracer base class
│   └── overlapping_intervals.py   # First algorithm
│
├── templates/
│   ├── base.html                   # Base template with layout
│   ├── index.html                  # Landing page
│   ├── problem.html                # Main problem page (4-pane layout)
│   ├── partials/
│   │   ├── step.html               # HTMX partial for step updates
│   │   ├── code_view.html          # Code pane
│   │   ├── variables.html          # Variables pane
│   │   └── call_stack.html         # Call stack pane
│   └── visualizations/
│       └── overlapping_intervals.html  # Timeline visualization
│
├── static/
│   ├── css/
│   │   └── styles.css              # Custom styles (beyond Tailwind)
│   └── js/
│       └── app.js                  # Alpine.js components
│
└── tests/                          # Unit tests for tracers
    └── test_overlapping_intervals.py
```

---

## 🔑 Key Design Principles

### 1. Server-Heavy Architecture
- Python does the heavy lifting (user's strength)
- HTMX handles navigation (minimal JS)
- Alpine.js for small interactions only (keyboard shortcuts, toggles)

### 2. Educational Focus
- Every step has clear explanation
- Visualizations are problem-specific, not generic
- Highlight "decision points" where recursion logic is key

### 3. Incremental Complexity
- MVP: One algorithm, hardcoded input
- Phase 2: Polish UX
- Phase 3: More algorithms
- Phase 4: User input

### 4. Maintainability
- DRY: Base classes, template partials
- Each algorithm is self-contained
- Easy to add new algorithms

---

## 🤔 Open Questions

### For Next Session

1. **Timeline Library**: Should we use raw SVG, D3.js, or HTML+CSS for visualizations?
   - **Consideration**: User has D3 available in their stack profile but limited experience

2. **Code Syntax Highlighting**: Pygments (Python library) or Prism.js (frontend)?
   - **Pygments**: Server-side, no JS, but requires preprocessing
   - **Prism.js**: Client-side, lightweight, but adds JS dependency

3. **Input Validation**: How to handle invalid inputs from users (Phase 4)?
   - Maximum interval count? Maximum value size?

4. **Algorithm Selection**: Which algorithm should be second?
   - **Tree Traversal**: Different visualization type (good for diversity)
   - **Merge Sort**: Same divide-conquer pattern (validates abstraction)

---

## 📚 Reference Materials

### Existing Code
- `overlapping_intervals.py` - First algorithm to visualize (already has educational print statements)
- `MASTER_GUIDE.md` - Parent document that inspired this project

### Similar Tools
- **Python Tutor**: https://pythontutor.com/ (generic approach)
- **VisuAlgo**: https://visualgo.net/ (algorithm visualizations, but not recursion-focused)
- **Recursion Tree Visualizer**: Various open-source projects on GitHub

### Technical Resources
- **HTMX Docs**: https://htmx.org/docs/
- **Flask-Session**: https://flask-session.readthedocs.io/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 🎓 Learning Goals

### For the Developer (User)
- Deeper understanding of recursion through visualization
- See how algorithmic decisions flow through recursive calls
- Build intuition for recursion patterns

### For the Project (Meta-Learning)
- Validate: Can problem-specific visualizations beat generic tools?
- Test: Does HTMX + Flask provide low-friction interactivity?
- Discover: What visualization types are most effective for different recursion patterns?

---

## 💡 Future Enhancements (Out of Scope for MVP)

- **Algorithm Comparison**: Side-by-side view of recursive vs. iterative
- **Performance Metrics**: Call count, max depth, time complexity visualization
- **Export**: Download trace as PDF or animated GIF
- **Collaboration**: Share trace URL with teacher/peer
- **Exercises**: "Predict next step" quiz mode
- **Mobile App**: Native iOS/Android app
- **More Algorithms**: Eventually cover all 8 chapters from the course

---

## 📝 Session Notes

### Session 1 (Current)
- **Date**: [To be filled]
- **Participants**: User + Claude
- **Achievements**: 
  - Defined project vision
  - Chose tech stack
  - Designed data structures
  - Identified challenges
  - Created this context document
- **Decisions Made**:
  - Flask + HTMX + Alpine.js + Tailwind
  - Pre-computation model for execution trace
  - Four-pane UI layout
  - Overlapping Intervals as first algorithm
- **Next Steps**: Build MVP in Session 2

### Session 2
- **Date**: [To be filled]
- **Goals**: 
  - [ ] Working Flask app
  - [ ] Tracer class implemented
  - [ ] Basic UI with HTMX navigation
  - [ ] Timeline visualization
- **Notes**: [To be filled during session]

---

## 🎯 Quick Start for Next Session

**To Resume Work**:

1. Review this document (focus on "Roadmap" and "Open Questions")
2. Reference `overlapping_intervals.py` for algorithm logic
3. Start with file structure setup
4. Implement tracer class first (pure Python, no Flask yet)
5. Add Flask routes once tracer works
6. Build UI incrementally (layout → navigation → visualization)

**Priority Order**:
1. Core functionality (navigation works)
2. Correctness (trace captures right info)
3. Visualization (clear and helpful)
4. Polish (aesthetics, UX refinements)

---

**Document Status**: Living document - update after each session  
**Last Updated**: Session 1  
**Next Review**: Start of Session 2