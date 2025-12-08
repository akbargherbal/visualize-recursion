import React, { useState } from "react";
import { Play, RotateCcw, ChevronRight, ChevronDown } from "lucide-react";

const IntervalCoverageVisualizer = () => {
  const initialIntervals = [
    { id: 1, start: 540, end: 660, color: "blue" },
    { id: 2, start: 600, end: 720, color: "green" },
    { id: 3, start: 540, end: 720, color: "amber" },
    { id: 4, start: 900, end: 960, color: "purple" },
  ];

  const [phase, setPhase] = useState(0); // 0: initial, 1: sorted, 2: recursion, 3: complete
  const [intervals, setIntervals] = useState([...initialIntervals]);
  const [sortedIntervals, setSortedIntervals] = useState([]);
  const [callStack, setCallStack] = useState([]);
  const [currentCallId, setCurrentCallId] = useState(0);
  const [stepInPhase, setStepInPhase] = useState(0);
  const [result, setResult] = useState([]);
  const [maxEndHistory, setMaxEndHistory] = useState([]);

  const minVal = 500;
  const maxVal = 1000;
  const toPercent = (val) => ((val - minVal) / (maxVal - minVal)) * 100;

  const colorClasses = {
    blue: {
      bg: "bg-blue-500",
      border: "border-blue-400",
      text: "text-blue-400",
      light: "bg-blue-900/30",
    },
    green: {
      bg: "bg-green-500",
      border: "border-green-400",
      text: "text-green-400",
      light: "bg-green-900/30",
    },
    amber: {
      bg: "bg-amber-500",
      border: "border-amber-400",
      text: "text-amber-400",
      light: "bg-amber-900/30",
    },
    purple: {
      bg: "bg-purple-500",
      border: "border-purple-400",
      text: "text-purple-400",
      light: "bg-purple-900/30",
    },
  };

  const sortIntervals = (intervals) => {
    return [...intervals].sort((a, b) => {
      if (a.start !== b.start) return a.start - b.start;
      return b.end - a.end; // Longer intervals first when starts are equal
    });
  };

  const handleNextStep = () => {
    if (phase === 0) {
      // Sort intervals
      const sorted = sortIntervals(intervals);
      setSortedIntervals(sorted);
      setPhase(1);
    } else if (phase === 1) {
      // Initialize recursion
      const initialCall = {
        id: 0,
        depth: 0,
        intervals: sortedIntervals,
        maxEnd: -Infinity,
        current: sortedIntervals[0],
        status: "examining",
        decision: null,
        returnValue: null,
        children: [],
      };
      setCallStack([initialCall]);
      setCurrentCallId(0);
      setPhase(2);
      setStepInPhase(0);
    } else if (phase === 2) {
      processRecursionStep();
    }
  };

  const processRecursionStep = () => {
    const stack = [...callStack];
    const currentCall = findCallById(stack, currentCallId);

    if (!currentCall) return;

    if (currentCall.status === "examining") {
      // Make decision
      const isCovered = currentCall.current.end <= currentCall.maxEnd;
      currentCall.status = "decided";
      currentCall.decision = isCovered ? "covered" : "keep";

      if (!isCovered) {
        const newMaxEnd = Math.max(currentCall.maxEnd, currentCall.current.end);
        setMaxEndHistory([
          ...maxEndHistory,
          {
            depth: currentCall.depth,
            value: newMaxEnd,
            interval: currentCall.current,
          },
        ]);
      }

      setCallStack(stack);
      setStepInPhase(stepInPhase + 1);
    } else if (currentCall.status === "decided") {
      // Check if we've already processed this (prevent duplicate calls)
      if (currentCall.children.length > 0 || currentCall.returnValue !== null) {
        // Already processed, move to returning state
        currentCall.status = "returning";
        setCallStack(stack);
        setStepInPhase(stepInPhase + 1);
        return;
      }

      // Create child call or return
      const remaining = currentCall.intervals.slice(1);

      if (remaining.length > 0) {
        const newMaxEnd =
          currentCall.decision === "keep"
            ? Math.max(currentCall.maxEnd, currentCall.current.end)
            : currentCall.maxEnd;

        const childCall = {
          id: callStack.length,
          depth: currentCall.depth + 1,
          intervals: remaining,
          maxEnd: newMaxEnd,
          current: remaining[0],
          status: "examining",
          decision: null,
          returnValue: null,
          children: [],
        };

        currentCall.children.push(childCall.id);
        stack.push(childCall);
        setCurrentCallId(childCall.id);
        setCallStack(stack);
        setStepInPhase(stepInPhase + 1);
      } else {
        // Base case: no more intervals, start returning
        currentCall.status = "returning";
        // Build return value immediately for this call
        if (currentCall.decision === "keep") {
          currentCall.returnValue = [currentCall.current];
        } else {
          currentCall.returnValue = [];
        }

        setCallStack(stack);
        setStepInPhase(stepInPhase + 1);

        // Check if this is the root call
        const parentId = findParentId(stack, currentCallId);
        if (parentId === null) {
          // Root call, we're done
          setPhase(3);
          setResult(currentCall.returnValue);
        } else {
          setCurrentCallId(parentId);
        }
      }
    } else if (currentCall.status === "returning") {
      // Bubble up return value
      const childReturnValues = currentCall.children
        .map((childId) => findCallById(stack, childId))
        .filter((child) => child && child.returnValue !== null)
        .flatMap((child) => child.returnValue);

      if (currentCall.decision === "keep") {
        currentCall.returnValue = [currentCall.current, ...childReturnValues];
      } else {
        currentCall.returnValue = childReturnValues;
      }

      setCallStack(stack);
      setStepInPhase(stepInPhase + 1);

      const parentId = findParentId(stack, currentCallId);
      if (parentId !== null) {
        setCurrentCallId(parentId);
      } else {
        setPhase(3);
        setResult(currentCall.returnValue);
      }
    }
  };

  const findCallById = (stack, id) => {
    return stack.find((call) => call.id === id);
  };

  const findParentId = (stack, childId) => {
    const parent = stack.find((call) => call.children.includes(childId));
    return parent ? parent.id : null;
  };

  const buildResult = (rootCall) => {
    if (!rootCall || !rootCall.returnValue) return [];
    return rootCall.returnValue;
  };

  const handleReset = () => {
    setPhase(0);
    setIntervals([...initialIntervals]);
    setSortedIntervals([]);
    setCallStack([]);
    setCurrentCallId(0);
    setStepInPhase(0);
    setResult([]);
    setMaxEndHistory([]);
  };

  const renderCallTree = () => {
    return callStack.map((call) => {
      const indent = call.depth * 24;
      const isActive = call.id === currentCallId;
      const colors = colorClasses[call.current?.color || "blue"];

      return (
        <div
          key={call.id}
          style={{ marginLeft: `${indent}px` }}
          className="my-2"
        >
          <div
            className={`p-3 rounded-lg border-2 transition-all ${
              isActive
                ? "border-yellow-400 bg-yellow-900/20 shadow-lg"
                : call.status === "returning"
                ? "border-emerald-400 bg-emerald-900/20"
                : "border-slate-600 bg-slate-800/50"
            }`}
          >
            {/* Call header */}
            <div className="flex items-center gap-2 mb-2">
              <div className="text-slate-400 text-xs font-mono">
                CALL #{call.id}
              </div>
              <ChevronRight size={12} className="text-slate-500" />
              <div className="text-white text-xs font-mono">
                depth={call.depth}, remaining={call.intervals.length}
              </div>
            </div>

            {/* Current interval */}
            <div className="flex items-center gap-2 mb-2">
              <div className="text-slate-400 text-xs">Examining:</div>
              <div
                className={`${colors.bg} text-white px-2 py-1 rounded text-xs font-bold`}
              >
                ({call.current.start}, {call.current.end})
              </div>
            </div>

            {/* Max end */}
            <div className="flex items-center gap-2 mb-2">
              <div className="text-slate-400 text-xs">max_end_so_far:</div>
              <div className="text-cyan-400 text-xs font-mono font-bold">
                {call.maxEnd === -Infinity ? "-∞" : call.maxEnd}
              </div>
            </div>

            {/* Decision */}
            {call.decision && (
              <div
                className={`flex items-center gap-2 p-2 rounded ${
                  call.decision === "keep"
                    ? "bg-emerald-900/30 border border-emerald-500"
                    : "bg-red-900/30 border border-red-500"
                }`}
              >
                <div className="text-xs font-bold">
                  {call.decision === "keep" ? "✅ KEEP" : "❌ COVERED"}
                </div>
                <div className="text-xs text-slate-300">
                  {call.current.end} {call.decision === "keep" ? ">" : "≤"}{" "}
                  {call.maxEnd === -Infinity ? "-∞" : call.maxEnd}
                </div>
              </div>
            )}

            {/* Return value */}
            {call.returnValue !== null && (
              <div className="mt-2 pt-2 border-t border-slate-600">
                <div className="text-slate-400 text-xs mb-1">⬅️ RETURN:</div>
                <div className="flex flex-wrap gap-1">
                  {call.returnValue.length === 0 ? (
                    <div className="text-slate-500 text-xs italic">[]</div>
                  ) : (
                    call.returnValue.map((interval, idx) => {
                      const c = colorClasses[interval.color];
                      return (
                        <div
                          key={idx}
                          className={`${c.bg} text-white px-2 py-1 rounded text-xs`}
                        >
                          ({interval.start},{interval.end})
                        </div>
                      );
                    })
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      );
    });
  };

  const getDisplayIntervals = () => {
    if (phase === 0) return intervals;
    if (phase === 1 || phase === 2) return sortedIntervals;
    return result;
  };

  return (
    <div className="w-full h-screen bg-slate-900 flex items-center justify-center p-4 overflow-hidden">
      {/* Completion Modal */}
      {phase === 3 && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-2xl shadow-2xl border-2 border-emerald-500 max-w-lg w-full p-8 animate-in">
            <div className="text-center mb-6">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-emerald-500 rounded-full mb-4">
                <svg
                  className="w-10 h-10 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={3}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <h2 className="text-3xl font-bold text-white mb-2">
                Algorithm Complete!
              </h2>
              <p className="text-slate-400">
                Successfully removed covered intervals
              </p>
            </div>

            <div className="bg-slate-900/50 rounded-lg p-6 mb-6">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-slate-400 text-sm mb-1">
                    Initial Intervals
                  </div>
                  <div className="text-3xl font-bold text-white">
                    {initialIntervals.length}
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-slate-400 text-sm mb-1">
                    Kept Intervals
                  </div>
                  <div className="text-3xl font-bold text-emerald-400">
                    {result.length}
                  </div>
                </div>
              </div>

              <div className="text-center pt-4 border-t border-slate-700">
                <div className="text-slate-400 text-sm mb-1">Removed</div>
                <div className="text-2xl font-bold text-red-400">
                  {initialIntervals.length - result.length} interval(s)
                </div>
              </div>
            </div>

            <div className="mb-6">
              <div className="text-slate-300 font-semibold mb-2">
                Final Result:
              </div>
              <div className="flex flex-wrap gap-2">
                {result.map((interval, idx) => {
                  const colors = colorClasses[interval.color];
                  return (
                    <div
                      key={idx}
                      className={`${colors.bg} text-white px-3 py-2 rounded-lg text-sm font-bold`}
                    >
                      ({interval.start}, {interval.end})
                    </div>
                  );
                })}
              </div>
            </div>

            <button
              onClick={handleReset}
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              <RotateCcw size={20} />
              Start Over
            </button>
          </div>
        </div>
      )}

      <div className="w-full h-full max-w-7xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-white">
              Remove Covered Intervals
            </h1>
            <p className="text-slate-400 text-sm">
              {phase === 0 && "Initial intervals"}
              {phase === 1 && "Step 1: Sorted by (start ↑, end ↓)"}
              {phase === 2 &&
                `Step 2: Recursive filtering - Processing call #${currentCallId}`}
              {phase === 3 && "Complete! Final result shown"}
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleReset}
              className="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
            >
              <RotateCcw size={20} />
              Reset
            </button>
            <button
              onClick={handleNextStep}
              disabled={phase === 3}
              className="bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-600 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors font-bold"
            >
              {phase === 0 && "Sort Intervals"}
              {phase === 1 && "Start Recursion"}
              {phase === 2 && "Next Step"}
              {phase === 3 && "Complete"}
              <ChevronRight size={20} />
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex gap-4 overflow-hidden">
          {/* Left: Timeline */}
          <div className="flex-1 bg-slate-800 rounded-xl p-6 shadow-2xl flex flex-col">
            <h2 className="text-white font-bold mb-4">
              Timeline Visualization
            </h2>

            <div className="relative flex-1 bg-slate-900/50 rounded-lg p-4">
              {/* Timeline axis */}
              <div className="absolute bottom-6 left-4 right-4 h-0.5 bg-slate-600"></div>

              {/* Scale markers */}
              <div className="absolute bottom-1 left-4 text-slate-400 text-xs">
                {minVal}
              </div>
              <div className="absolute bottom-1 left-1/3 text-slate-400 text-xs">
                700
              </div>
              <div className="absolute bottom-1 left-2/3 text-slate-400 text-xs">
                850
              </div>
              <div className="absolute bottom-1 right-4 text-slate-400 text-xs">
                {maxVal}
              </div>

              {/* Max end line */}
              {phase === 2 &&
                callStack[currentCallId] &&
                callStack[currentCallId].maxEnd !== -Infinity && (
                  <div
                    className="absolute top-4 bottom-6 w-0.5 bg-cyan-400 z-10"
                    style={{
                      left: `${
                        4 + toPercent(callStack[currentCallId].maxEnd) * 0.92
                      }%`,
                    }}
                  >
                    <div className="absolute -top-6 -left-12 bg-cyan-400 text-slate-900 text-xs px-2 py-1 rounded font-bold whitespace-nowrap">
                      max_end: {callStack[currentCallId].maxEnd}
                    </div>
                  </div>
                )}

              {/* Interval bars */}
              {getDisplayIntervals().map((interval, idx) => {
                const colors = colorClasses[interval.color];
                const left = toPercent(interval.start);
                const width =
                  toPercent(interval.end) - toPercent(interval.start);
                const currentCall = callStack[currentCallId];
                const isCurrentlyExamining =
                  phase === 2 && currentCall?.current?.id === interval.id;
                const isCovered =
                  phase === 2 &&
                  callStack.some(
                    (c) =>
                      c.current?.id === interval.id && c.decision === "covered"
                  );
                const isKept =
                  phase === 2 &&
                  callStack.some(
                    (c) =>
                      c.current?.id === interval.id && c.decision === "keep"
                  );

                return (
                  <div
                    key={interval.id}
                    className={`absolute h-10 ${colors.bg} rounded border-2 ${
                      colors.border
                    } flex items-center justify-center text-white text-sm font-bold transition-all duration-300 ${
                      isCurrentlyExamining
                        ? "ring-4 ring-yellow-400 scale-105"
                        : ""
                    } ${isCovered ? "opacity-30 line-through" : ""} ${
                      isKept ? "shadow-lg shadow-emerald-500/50" : ""
                    }`}
                    style={{
                      left: `${4 + left * 0.92}%`,
                      width: `${width * 0.92}%`,
                      top: `${4 + idx * 48}px`,
                    }}
                  >
                    {interval.start}-{interval.end}
                  </div>
                );
              })}
            </div>

            {/* Legend */}
            <div className="mt-4 flex gap-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-8 h-3 bg-cyan-400 rounded"></div>
                <span className="text-slate-400">max_end line</span>
              </div>
              {phase === 2 && (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-3 bg-yellow-400 rounded ring-2 ring-yellow-400"></div>
                    <span className="text-slate-400">examining</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-3 bg-slate-500 opacity-30 rounded line-through"></div>
                    <span className="text-slate-400">covered (skipped)</span>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Right: Call Stack */}
          <div className="w-96 bg-slate-800 rounded-xl p-6 shadow-2xl flex flex-col overflow-hidden">
            <h2 className="text-white font-bold mb-4 flex items-center gap-2">
              Recursive Call Stack
              {phase === 2 && (
                <span className="text-xs bg-emerald-500 text-white px-2 py-1 rounded-full">
                  {callStack.length} calls
                </span>
              )}
            </h2>

            <div className="flex-1 overflow-y-auto">
              {phase < 2 ? (
                <div className="text-slate-500 text-sm italic">
                  {phase === 0 && "Sort intervals first to begin"}
                  {phase === 1 &&
                    "Click 'Start Recursion' to see the call stack"}
                </div>
              ) : (
                <div className="space-y-2">{renderCallTree()}</div>
              )}
            </div>

            {/* Summary */}
            {phase === 3 && (
              <div className="mt-4 p-4 bg-emerald-900/20 border-2 border-emerald-500 rounded-lg">
                <div className="text-emerald-400 font-bold mb-2">
                  ✓ Algorithm Complete!
                </div>
                <div className="text-white text-sm">
                  Kept: {result.length} / {initialIntervals.length} intervals
                </div>
                <div className="text-slate-400 text-xs mt-2">
                  Removed {initialIntervals.length - result.length} covered
                  interval(s)
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default IntervalCoverageVisualizer;
