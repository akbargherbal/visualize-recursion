"""
Core tracing infrastructure for algorithm visualization.
Captures execution steps with timestamps and structured data.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json


class TraceGenerator:
    """Captures algorithm execution steps for visualization"""

    def __init__(self):
        self.steps: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
        self._call_counter = 0
        self._start_time = datetime.now()

    def set_metadata(self, metadata: Dict[str, Any]):
        """Set algorithm metadata (name, input size, etc.)"""
        self.metadata.update(metadata)

    def capture(self, event_type: str, data: Dict[str, Any]):
        """
        Capture a single execution step.

        Args:
            event_type: Type of event (e.g., 'CALL_START', 'DECISION_MADE')
            data: Event-specific data to capture
        """
        timestamp = (datetime.now() - self._start_time).total_seconds()

        step = {
            "step_number": len(self.steps),
            "timestamp": timestamp,
            "type": event_type,
            "data": data,
        }

        self.steps.append(step)

    def next_call_id(self) -> int:
        """Generate unique call ID for recursion tracking"""
        call_id = self._call_counter
        self._call_counter += 1
        return call_id

    def get_trace(self) -> Dict[str, Any]:
        """
        Get complete trace data.

        Returns:
            Dictionary with metadata and steps
        """
        return {
            "metadata": self.metadata,
            "steps": self.steps,
            "total_steps": len(self.steps),
            "duration": self.steps[-1]["timestamp"] if self.steps else 0,
        }

    def to_json(self) -> str:
        """Export trace as JSON string"""
        return json.dumps(self.get_trace(), indent=2)
