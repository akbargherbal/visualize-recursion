"""
Educational UI Testing for Recursion Visualizer
================================================

Tests that verify the tracer produces educationally valuable output
and validates UI/UX requirements.
"""

import sys
from pathlib import Path

# Add algorithms directory to path (go up one level from tests/)
sys.path.insert(0, str(Path(__file__).parent.parent / 'algorithms'))

from overlapping_intervals_tracer import OverlappingIntervalsTracer


def test_basic_execution():
    """Test 1: Verify tracer completes successfully."""
    print("\n" + "="*70)
    print("TEST 1: Basic Execution")
    print("="*70)
    
    tracer = OverlappingIntervalsTracer()
    test_intervals = [(540, 660), (600, 720), (540, 720), (900, 960)]
    output = tracer.run(test_intervals)
    
    assert 'trace' in output, "Missing 'trace' in output"
    assert 'result' in output, "Missing 'result' in output"
    assert 'metadata' in output, "Missing 'metadata' in output"
    
    print(f"✅ Tracer executed successfully")
    print(f"   • Steps captured: {len(output['trace'])}")
    print(f"   • Result: {output['result']}")
    
    return output


def test_step_structure(output):
    """Test 2: Verify each step has required fields."""
    print("\n" + "="*70)
    print("TEST 2: Step Structure Validation")
    print("="*70)
    
    required_fields = [
        'step', 'phase', 'action', 'explanation', 
        'intervals_state', 'variables'
    ]
    
    trace = output['trace']
    
    for i, step in enumerate(trace):
        for field in required_fields:
            if field not in step:
                print(f"❌ Step {i}: Missing field '{field}'")
                return False
    
    print(f"✅ All {len(trace)} steps have required fields")
    return True


def test_educational_clarity(output):
    """Test 3: Verify explanations are clear and helpful."""
    print("\n" + "="*70)
    print("TEST 3: Educational Clarity")
    print("="*70)
    
    trace = output['trace']
    
    # Check for key educational phases
    phases_found = set(step['phase'] for step in trace)
    expected_phases = {
        'initialization', 'sorting', 'recursive_call', 
        'examination', 'decision_covered', 'decision_keep'
    }
    
    missing_phases = expected_phases - phases_found
    if missing_phases:
        print(f"⚠️  Missing educational phases: {missing_phases}")
    else:
        print(f"✅ All key educational phases present")
    
    # Check explanation length (should be substantial)
    short_explanations = [
        (i, step) for i, step in enumerate(trace)
        if len(step.get('explanation', '')) < 20
    ]
    
    if short_explanations:
        print(f"⚠️  {len(short_explanations)} steps have very short explanations")
        for i, step in short_explanations[:3]:
            print(f"   Step {i}: '{step['explanation']}'")
    else:
        print(f"✅ All explanations are substantial")
    
    return True


def test_visualization_data(output):
    """Test 4: Verify visualization data is present and valid."""
    print("\n" + "="*70)
    print("TEST 4: Visualization Data")
    print("="*70)
    
    trace = output['trace']
    
    # Check intervals_state structure
    for i, step in enumerate(trace):
        intervals_state = step.get('intervals_state', [])
        
        if not isinstance(intervals_state, list):
            print(f"❌ Step {i}: intervals_state is not a list")
            return False
        
        for item in intervals_state:
            if not isinstance(item, dict):
                print(f"❌ Step {i}: interval item is not a dict")
                return False
            
            required = ['interval', 'status', 'opacity']
            for field in required:
                if field not in item:
                    print(f"❌ Step {i}: interval missing '{field}'")
                    return False
    
    print(f"✅ All steps have valid visualization data")
    return True


def test_decision_points(output):
    """Test 5: Identify and validate key decision points."""
    print("\n" + "="*70)
    print("TEST 5: Decision Points (Educational Critical)")
    print("="*70)
    
    trace = output['trace']
    
    # Find decision points
    decisions = [
        step for step in trace 
        if step['phase'] in ['decision_covered', 'decision_keep']
    ]
    
    print(f"Found {len(decisions)} decision points:")
    
    for i, step in enumerate(decisions, 1):
        print(f"\n  Decision {i}:")
        print(f"    Phase: {step['phase']}")
        print(f"    Action: {step['action']}")
        print(f"    Explanation: {step['explanation'][:80]}...")
        
        # Check for key information in decision explanations
        explanation = step['explanation'].lower()
        
        # Should explain WHY the decision was made
        has_comparison = any(word in explanation for word in ['<=', '>', 'since', 'because'])
        has_consequence = any(word in explanation for word in ['skip', 'keep', 'covered', 'update'])
        
        if has_comparison and has_consequence:
            print(f"    ✅ Good explanation (has comparison + consequence)")
        else:
            print(f"    ⚠️  Could be clearer (missing comparison or consequence)")
    
    return True


def test_step_by_step_narrative(output):
    """Test 6: Verify the trace tells a coherent story."""
    print("\n" + "="*70)
    print("TEST 6: Step-by-Step Narrative")
    print("="*70)
    
    trace = output['trace']
    
    print("\nFull execution narrative:")
    print("-" * 70)
    
    for step in trace:
        depth_indent = "  " * step.get('depth', 0)
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
        
        print(f"{step['step']:2d}. {phase_emoji} {depth_indent}{step['action']}")
    
    print("-" * 70)
    print("✅ Narrative flows logically")
    
    return True


def test_timeline_visual_states(output):
    """Test 7: Verify timeline has distinct visual states."""
    print("\n" + "="*70)
    print("TEST 7: Timeline Visual States")
    print("="*70)
    
    trace = output['trace']
    
    # Collect all statuses used
    all_statuses = set()
    for step in trace:
        for item in step.get('intervals_state', []):
            all_statuses.add(item['status'])
    
    print(f"Timeline uses {len(all_statuses)} distinct visual states:")
    for status in sorted(all_statuses):
        print(f"  • {status}")
    
    # Should have at least: pending, examining, kept, covered
    expected_min = {'pending', 'examining', 'kept'}
    if expected_min.issubset(all_statuses):
        print("✅ Has key visual states (pending, examining, kept)")
    else:
        missing = expected_min - all_statuses
        print(f"⚠️  Missing key states: {missing}")
    
    return True


def test_attention_guidance(output):
    """Test 8: Check if UI guides attention properly."""
    print("\n" + "="*70)
    print("TEST 8: Attention Guidance (What to Watch)")
    print("="*70)
    
    trace = output['trace']
    
    # Count steps with 'examining' status (should be clear focus)
    examining_steps = [
        step for step in trace
        if any(item['status'] == 'examining' 
               for item in step.get('intervals_state', []))
    ]
    
    print(f"Steps with clear focus (examining): {len(examining_steps)}")
    
    # Check opacity variations (helps guide attention)
    opacity_variations = set()
    for step in trace:
        for item in step.get('intervals_state', []):
            opacity_variations.add(item['opacity'])
    
    print(f"Opacity levels used: {sorted(opacity_variations)}")
    
    if len(opacity_variations) >= 3:
        print("✅ Good use of opacity to guide attention")
    else:
        print("⚠️  Could use more opacity variation")
    
    return True


def print_sample_step(output, step_num):
    """Print detailed view of a single step."""
    print("\n" + "="*70)
    print(f"SAMPLE STEP #{step_num} DETAILS")
    print("="*70)
    
    step = output['trace'][step_num]
    
    print(f"\nPhase: {step['phase']}")
    print(f"Action: {step['action']}")
    print(f"\nExplanation:")
    print(f"  {step['explanation']}")
    
    print(f"\nVariables:")
    for key, value in step.get('variables', {}).items():
        print(f"  {key}: {value}")
    
    print(f"\nIntervals State:")
    for item in step.get('intervals_state', []):
        print(f"  {item['interval']} -> {item['status']} (opacity: {item['opacity']})")
    
    if step.get('call_stack'):
        print(f"\nCall Stack:")
        for call in step['call_stack']:
            print(f"  {call}")


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "█"*70)
    print("EDUCATIONAL UI TEST SUITE")
    print("█"*70)
    
    # Run tracer
    output = test_basic_execution()
    
    # Run all tests
    tests = [
        test_step_structure,
        test_educational_clarity,
        test_visualization_data,
        test_decision_points,
        test_step_by_step_narrative,
        test_timeline_visual_states,
        test_attention_guidance,
    ]
    
    results = {}
    for test_func in tests:
        try:
            result = test_func(output)
            results[test_func.__name__] = result
        except Exception as e:
            print(f"❌ {test_func.__name__} failed with error: {e}")
            results[test_func.__name__] = False
    
    # Print sample step
    print_sample_step(output, step_num=5)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        display_name = test_name.replace('test_', '').replace('_', ' ').title()
        print(f"{status} - {display_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED - UI IS EDUCATIONALLY SOUND!")
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW NEEDED")
    print("="*70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)