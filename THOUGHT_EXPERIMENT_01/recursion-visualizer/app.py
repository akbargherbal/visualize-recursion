"""
Recursion Visualizer - Flask Application
=========================================

Web-based tool for visualizing recursive algorithm execution.
"""

from flask import Flask, render_template, session, redirect, url_for, jsonify
from pathlib import Path
import sys

# Add algorithms directory to path
sys.path.insert(0, str(Path(__file__).parent / 'algorithms'))

from overlapping_intervals_tracer import OverlappingIntervalsTracer

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'  # Change this in production!

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False


@app.route('/')
def index():
    """Landing page with algorithm list."""
    algorithms = [
        {
            'id': 'overlapping-intervals',
            'name': 'Remove Covered Intervals',
            'description': 'Remove intervals completely covered by other intervals',
            'difficulty': 'Medium',
            'category': 'Array Processing'
        }
        # More algorithms will be added here
    ]
    return render_template('index.html', algorithms=algorithms)


@app.route('/problem/<algorithm_id>')
def problem(algorithm_id):
    """
    Initialize algorithm and display first step.
    
    This route:
    1. Runs the algorithm with instrumentation
    2. Captures the full execution trace
    3. Stores trace in session
    4. Renders the visualization page at step 0
    """
    if algorithm_id != 'overlapping-intervals':
        return "Algorithm not found", 404
    
    # Initialize with default test case
    test_intervals = [(540, 660), (600, 720), (540, 720), (900, 960)]
    
    # Run tracer
    tracer = OverlappingIntervalsTracer()
    output = tracer.run(test_intervals)
    
    # Store in session
    session['trace'] = output['trace']
    session['metadata'] = output['metadata']
    session['algorithm'] = algorithm_id
    session['input_data'] = test_intervals
    session['current_step'] = 0
    
    # Get first step data
    step_data = output['trace'][0]
    total_steps = len(output['trace'])
    
    return render_template(
        'problem.html',
        algorithm_id=algorithm_id,
        algorithm_name='Remove Covered Intervals',
        step_data=step_data,
        current_step=0,
        total_steps=total_steps,
        metadata=output['metadata'],
        source_code=get_source_code()
    )


@app.route('/problem/<algorithm_id>/step/<int:step_num>')
def get_step(algorithm_id, step_num):
    """
    HTMX endpoint: Return HTML partial for a specific step.
    
    This is called when user clicks Next/Prev buttons.
    Returns only the updated portions of the page.
    """
    # Validate session data exists
    if 'trace' not in session:
        return "Session expired. Please reload.", 400
    
    trace = session['trace']
    
    # Validate step number
    if step_num < 0 or step_num >= len(trace):
        return "Invalid step", 400
    
    # Update current step
    session['current_step'] = step_num
    
    # Get step data
    step_data = trace[step_num]
    
    return render_template(
        'partials/step.html',
        step_data=step_data,
        current_step=step_num,
        total_steps=len(trace),
        source_code=get_source_code()
    )


@app.route('/problem/<algorithm_id>/reset')
def reset(algorithm_id):
    """Reset to step 0."""
    return redirect(url_for('get_step', algorithm_id=algorithm_id, step_num=0))


@app.route('/problem/<algorithm_id>/jump/<int:step_num>')
def jump_to_step(algorithm_id, step_num):
    """Jump to specific step."""
    return redirect(url_for('get_step', algorithm_id=algorithm_id, step_num=step_num))


def get_source_code():
    """
    Return the algorithm source code for display.
    
    In a more complete version, this would be dynamically loaded
    per algorithm. For MVP, we hardcode the overlapping intervals algorithm.
    """
    return '''def filter_covered(remaining, max_end_so_far, depth=0):
    """Recursively filter out covered intervals."""
    
    # BASE CASE: No more intervals to process
    if not remaining:
        return []
    
    # Process first interval
    current = remaining[0]
    rest = remaining[1:]
    
    # DECISION POINT: Is this interval covered?
    if current[1] <= max_end_so_far:
        # Covered: skip this interval
        return filter_covered(rest, max_end_so_far, depth + 1)
    else:
        # Not covered: keep it and update max_end
        new_max_end = max(max_end_so_far, current[1])
        return [current] + filter_covered(rest, new_max_end, depth + 1)'''


# Development-only route for debugging
@app.route('/debug/trace')
def debug_trace():
    """Debug route to inspect current trace in session."""
    if 'trace' not in session:
        return jsonify({'error': 'No trace in session'})
    
    return jsonify({
        'total_steps': len(session['trace']),
        'current_step': session.get('current_step', 0),
        'metadata': session.get('metadata', {}),
        'sample_steps': session['trace'][:3]  # Show first 3 steps
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)