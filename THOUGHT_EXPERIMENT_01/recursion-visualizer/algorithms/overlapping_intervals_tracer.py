"""
Instrumented Overlapping Intervals Algorithm with Trace Capture
================================================================

This module provides a tracer version of the overlapping intervals algorithm
that captures execution steps for visualization purposes.
"""

from typing import List, Tuple, Dict, Any


class OverlappingIntervalsTracer:
    """
    Traces execution of the overlapping intervals removal algorithm.
    
    Captures each step of the recursive algorithm for later visualization.
    """
    
    def __init__(self):
        self.trace: List[Dict[str, Any]] = []
        self.step_counter = 0
        
    def run(self, intervals: List[Tuple[int, int]]) -> Dict[str, Any]:
        """
        Execute algorithm and capture trace.
        
        Args:
            intervals: List of (start, end) tuples
            
        Returns:
            Dict containing:
                - 'result': Final list of non-covered intervals
                - 'trace': List of execution steps
                - 'metadata': Summary statistics
        """
        self.trace = []
        self.step_counter = 0
        
        # Capture initial state
        self._add_step(
            phase="initialization",
            action="Algorithm started",
            explanation=f"Input: {len(intervals)} intervals to process",
            intervals_state=self._create_intervals_state(intervals, "pending"),
            variables={
                "input_intervals": intervals,
                "total_count": len(intervals)
            }
        )
        
        # Sort intervals
        sorted_intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))
        
        self._add_step(
            phase="sorting",
            action="Sorted intervals",
            explanation=(
                "Sorted by start time (ascending), then end time (descending). "
                "This ensures longer intervals come first when starts are equal."
            ),
            intervals_state=self._create_intervals_state(sorted_intervals, "sorted"),
            variables={
                "sorted_intervals": sorted_intervals,
                "sort_key": "(start ↑, end ↓)"
            },
            code_line=8  # Corresponds to line in original algorithm
        )
        
        # Run recursive filtering
        result = self._filter_covered(sorted_intervals, float('-inf'), depth=0)
        
        # Capture final state
        self._add_step(
            phase="completion",
            action="Algorithm completed",
            explanation=(
                f"Removed {len(intervals) - len(result)} covered interval(s). "
                f"Result contains {len(result)} interval(s)."
            ),
            intervals_state=self._create_final_state(sorted_intervals, result),
            variables={
                "final_result": result,
                "removed_count": len(intervals) - len(result)
            },
            result=result
        )
        
        # Calculate metadata
        max_depth = max((step.get('depth', 0) for step in self.trace), default=0)
        total_calls = sum(1 for step in self.trace if step.get('phase') == 'recursive_call')
        
        return {
            'result': result,
            'trace': self.trace,
            'metadata': {
                'total_steps': len(self.trace),
                'total_intervals': len(intervals),
                'result_intervals': len(result),
                'removed_intervals': len(intervals) - len(result),
                'max_recursion_depth': max_depth,
                'total_recursive_calls': total_calls
            }
        }
    
    def _filter_covered(
        self, 
        remaining: List[Tuple[int, int]], 
        max_end_so_far: float,
        depth: int,
        call_stack: List[str] = None
    ) -> List[Tuple[int, int]]:
        """
        Recursively filter covered intervals (instrumented version).
        
        Args:
            remaining: Intervals left to process
            max_end_so_far: Maximum end time seen so far
            depth: Current recursion depth
            call_stack: Stack trace for visualization
            
        Returns:
            List of non-covered intervals
        """
        if call_stack is None:
            call_stack = []
        
        # Add current call to stack
        current_call = f"filter_covered({len(remaining)} intervals, max_end={max_end_so_far})"
        call_stack = call_stack + [current_call]
        
        # Capture recursive call entry
        self._add_step(
            phase="recursive_call",
            action=f"Enter recursive call (depth {depth})",
            explanation=(
                f"Processing {len(remaining)} remaining interval(s) "
                f"with max_end_so_far = {max_end_so_far}"
            ),
            intervals_state=self._create_intervals_state(remaining, "examining"),
            variables={
                "remaining": remaining,
                "max_end_so_far": max_end_so_far,
                "depth": depth
            },
            depth=depth,
            call_stack=call_stack.copy(),
            code_line=12  # Corresponds to function definition
        )
        
        # BASE CASE: Empty list
        if not remaining:
            self._add_step(
                phase="base_case",
                action="Base case reached",
                explanation="No more intervals to process. Return empty list.",
                intervals_state=[],
                variables={
                    "remaining": [],
                    "result": []
                },
                depth=depth,
                call_stack=call_stack.copy(),
                result=[],
                code_line=15
            )
            return []
        
        # Process first interval
        current = remaining[0]
        rest = remaining[1:]
        
        self._add_step(
            phase="examination",
            action=f"Examining interval {current}",
            explanation=f"Current interval: {current}. Checking if covered by max_end_so_far ({max_end_so_far}).",
            intervals_state=self._mark_current(remaining, current),
            variables={
                "current": current,
                "rest": rest,
                "max_end_so_far": max_end_so_far
            },
            depth=depth,
            call_stack=call_stack.copy(),
            code_line=18
        )
        
        # DECISION POINT: Covered or not?
        if current[1] <= max_end_so_far:
            # COVERED
            self._add_step(
                phase="decision_covered",
                action=f"Interval {current} is COVERED",
                explanation=(
                    f"Since {current[1]} ≤ {max_end_so_far}, this interval ends before or at "
                    f"the current maximum end time. It is completely covered by a previous interval. "
                    f"Skip this interval and continue with the rest."
                ),
                intervals_state=self._mark_covered(remaining, current),
                variables={
                    "current": current,
                    "current_end": current[1],
                    "max_end_so_far": max_end_so_far,
                    "decision": "COVERED"
                },
                depth=depth,
                call_stack=call_stack.copy(),
                code_line=22
            )
            
            result = self._filter_covered(rest, max_end_so_far, depth + 1, call_stack)
            
        else:
            # NOT COVERED
            new_max_end = max(max_end_so_far, current[1])
            
            self._add_step(
                phase="decision_keep",
                action=f"Interval {current} is NOT COVERED",
                explanation=(
                    f"Since {current[1]} > {max_end_so_far}, this interval extends beyond "
                    f"the current maximum end time. Keep this interval in the result. "
                    f"Update max_end_so_far from {max_end_so_far} to {new_max_end}."
                ),
                intervals_state=self._mark_kept(remaining, current),
                variables={
                    "current": current,
                    "current_end": current[1],
                    "max_end_so_far": max_end_so_far,
                    "new_max_end": new_max_end,
                    "decision": "KEEP"
                },
                depth=depth,
                call_stack=call_stack.copy(),
                code_line=25
            )
            
            result = [current] + self._filter_covered(rest, new_max_end, depth + 1, call_stack)
        
        # Capture return
        self._add_step(
            phase="return",
            action=f"Return from depth {depth}",
            explanation=f"Returning {len(result)} interval(s) to caller.",
            intervals_state=self._create_intervals_state(result, "result"),
            variables={
                "result": result,
                "result_length": len(result)
            },
            depth=depth,
            call_stack=call_stack.copy(),
            result=result,
            code_line=28
        )
        
        return result
    
    def _add_step(self, **kwargs):
        """Add a step to the trace."""
        step = {
            'step': self.step_counter,
            **kwargs
        }
        self.trace.append(step)
        self.step_counter += 1
    
    def _create_intervals_state(
        self, 
        intervals: List[Tuple[int, int]], 
        status: str
    ) -> List[Dict[str, Any]]:
        """Create visualization state for intervals."""
        return [
            {
                'interval': interval,
                'status': status,
                'opacity': 1.0 if status in ['examining', 'kept'] else 0.6
            }
            for interval in intervals
        ]
    
    def _mark_current(
        self, 
        intervals: List[Tuple[int, int]], 
        current: Tuple[int, int]
    ) -> List[Dict[str, Any]]:
        """Mark current interval being examined."""
        return [
            {
                'interval': interval,
                'status': 'examining' if interval == current else 'pending',
                'opacity': 1.0 if interval == current else 0.5
            }
            for interval in intervals
        ]
    
    def _mark_covered(
        self, 
        intervals: List[Tuple[int, int]], 
        covered: Tuple[int, int]
    ) -> List[Dict[str, Any]]:
        """Mark interval as covered (will be removed)."""
        return [
            {
                'interval': interval,
                'status': 'covered' if interval == covered else 'pending',
                'opacity': 0.3 if interval == covered else 0.5
            }
            for interval in intervals
        ]
    
    def _mark_kept(
        self, 
        intervals: List[Tuple[int, int]], 
        kept: Tuple[int, int]
    ) -> List[Dict[str, Any]]:
        """Mark interval as kept in result."""
        return [
            {
                'interval': interval,
                'status': 'kept' if interval == kept else 'pending',
                'opacity': 1.0 if interval == kept else 0.5
            }
            for interval in intervals
        ]
    
    def _create_final_state(
        self, 
        all_intervals: List[Tuple[int, int]], 
        result: List[Tuple[int, int]]
    ) -> List[Dict[str, Any]]:
        """Create final visualization state showing kept vs removed."""
        result_set = set(result)
        return [
            {
                'interval': interval,
                'status': 'kept' if interval in result_set else 'removed',
                'opacity': 1.0 if interval in result_set else 0.2
            }
            for interval in all_intervals
        ]


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TRACER TEST: Overlapping Intervals")
    print("=" * 70)
    
    # Test with original example
    test_intervals = [(540, 660), (600, 720), (540, 720), (900, 960)]
    
    print(f"\n📥 Input: {test_intervals}")
    
    tracer = OverlappingIntervalsTracer()
    output = tracer.run(test_intervals)
    
    print(f"\n📤 Result: {output['result']}")
    print(f"\n📊 Metadata:")
    for key, value in output['metadata'].items():
        print(f"   • {key}: {value}")
    
    print(f"\n🔍 Trace captured {len(output['trace'])} steps:")
    print("\nStep-by-step summary:")
    print("-" * 70)
    
    for step in output['trace']:
        phase_emoji = {
            'initialization': '🎬',
            'sorting': '📊',
            'recursive_call': '📞',
            'base_case': '🛑',
            'examination': '🔍',
            'decision_covered': '❌',
            'decision_keep': '✅',
            'return': '⬅️',
            'completion': '🏁'
        }.get(step['phase'], '•')
        
        depth_indent = "  " * step.get('depth', 0)
        print(f"{step['step']:2d}. {phase_emoji} {depth_indent}{step['action']}")
    
    print("\n" + "=" * 70)
    print("✓ Tracer test completed successfully!")
    print("=" * 70 + "\n")