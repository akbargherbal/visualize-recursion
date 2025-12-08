"""
Remove Covered Intervals Algorithm
Removes all intervals that are completely covered by other intervals.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from algorithms.base_algorithm import BaseAlgorithm
from algorithms.registry import registry
from core.tracer import TraceGenerator


@registry.register
class IntervalCoverageAlgorithm(BaseAlgorithm):
    """
    Algorithm to remove intervals covered by others.

    An interval [a, b] is covered by [c, d] if c <= a and b <= d.
    Strategy:
    1. Sort by start time (ascending), then end time (descending)
    2. Recursively filter: keep interval if its end extends beyond max_end
    """

    def validate_input(self, input_data):
        """Validate intervals format"""
        if not isinstance(input_data, dict):
            return False

        if 'intervals' not in input_data:
            return False

        intervals = input_data['intervals']
        if not isinstance(intervals, list):
            return False

        # Check each interval has required fields
        for interval in intervals:
            if not isinstance(interval, dict):
                return False
            required_fields = ['start', 'end']
            if not all(k in interval for k in required_fields):
                return False
            if interval['start'] >= interval['end']:
                return False

        return True

    def execute_traced(self, input_data):
        """Execute with full trace capture"""
        intervals = input_data['intervals']
        tracer = TraceGenerator()

        # Set metadata
        tracer.set_metadata({
            'algorithm': self.id,
            'input_size': len(intervals),
            'algorithm_name': self.name
        })

        # Capture initial state
        tracer.capture('INITIAL_STATE', {
            'intervals': intervals,
            'count': len(intervals),
            'description': 'Original unsorted intervals'
        })

        # Sort intervals
        tracer.capture('SORT_BEGIN', {
            'description': 'Sorting by (start ↑, end ↓)'
        })

        sorted_intervals = sorted(
            intervals,
            key=lambda x: (x['start'], -x['end'])
        )

        tracer.capture('SORT_COMPLETE', {
            'sorted_intervals': sorted_intervals,
            'description': 'Intervals sorted - ready for recursion'
        })

        # Recursive processing with detailed trace
        def recurse(remaining, max_end, depth, parent_id):
            """
            Recursive function to filter covered intervals.

            Args:
                remaining: List of intervals still to process
                max_end: Maximum end value seen so far
                depth: Current recursion depth
                parent_id: ID of parent call (for tree structure)

            Returns:
                List of intervals to keep
            """
            call_id = tracer.next_call_id()

            # Capture call start
            tracer.capture('CALL_START', {
                'call_id': call_id,
                'depth': depth,
                'remaining_count': len(remaining),
                'remaining': remaining,
                'max_end': max_end,
                'parent_id': parent_id
            })

            # Base case: no more intervals
            if not remaining:
                tracer.capture('BASE_CASE', {
                    'call_id': call_id,
                    'description': 'No intervals remaining - return empty list'
                })

                tracer.capture('CALL_RETURN', {
                    'call_id': call_id,
                    'return_value': [],
                    'depth': depth
                })
                return []

            # Get current interval
            current = remaining[0]

            tracer.capture('EXAMINING_INTERVAL', {
                'call_id': call_id,
                'interval': current,
                'max_end': max_end,
                'comparison': f"{current['end']} vs {max_end}"
            })

            # Decision: covered or keep?
            # If max_end is None, this is the first interval - keep it
            if max_end is None:
                is_covered = False
            else:
                is_covered = current['end'] <= max_end
            decision = 'covered' if is_covered else 'keep'

            tracer.capture('DECISION_MADE', {
                'call_id': call_id,
                'interval': current,
                'decision': decision,
                'reason': f"end={current['end']} {'<=' if is_covered else '>'} max_end={max_end if max_end is not None else 'None (first)'}",
                'will_keep': not is_covered
            })

            # Update max_end if keeping interval
            new_max_end = max_end
            if decision == 'keep':
                # If max_end is None, just use current end
                if max_end is None:
                    new_max_end = current['end']
                else:
                    new_max_end = max(max_end, current['end'])
                tracer.capture('MAX_END_UPDATE', {
                    'call_id': call_id,
                    'old_max_end': max_end,
                    'new_max_end': new_max_end,
                    'interval': current
                })

            # Recursive call for remaining intervals
            child_result = recurse(
                remaining[1:],
                new_max_end,
                depth + 1,
                call_id
            )

            # Build result
            if decision == 'keep':
                result = [current] + child_result
            else:
                result = child_result

            tracer.capture('CALL_RETURN', {
                'call_id': call_id,
                'return_value': result,
                'depth': depth,
                'kept_count': len(result)
            })

            return result

        # Start recursion with a sentinel value that's JSON-safe
        # Using None or a very small number instead of float('-inf')
        result = recurse(sorted_intervals, None, 0, None)

        # Capture completion
        tracer.capture('ALGORITHM_COMPLETE', {
            'result': result,
            'kept_count': len(result),
            'removed_count': len(intervals) - len(result),
            'efficiency': f"{len(result)}/{len(intervals)} intervals kept"
        })

        return tracer.get_trace(), result

    def get_default_example(self):
        """Return default example input"""
        return {
            'intervals': [
                {'id': 1, 'start': 540, 'end': 660, 'color': 'blue'},
                {'id': 2, 'start': 600, 'end': 720, 'color': 'green'},
                {'id': 3, 'start': 540, 'end': 720, 'color': 'amber'},
                {'id': 4, 'start': 900, 'end': 960, 'color': 'purple'}
            ]
        }