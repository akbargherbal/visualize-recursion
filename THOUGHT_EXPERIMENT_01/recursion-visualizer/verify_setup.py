"""
Setup Verification Script
==========================

Run this to verify your recursion-visualizer setup is correct.
"""

import sys
from pathlib import Path

def check_file_structure():
    """Verify all required files exist."""
    print("\n" + "="*70)
    print("CHECKING FILE STRUCTURE")
    print("="*70)
    
    required_files = [
        'app.py',
        'requirements.txt',
        'algorithms/__init__.py',
        'algorithms/overlapping_intervals_tracer.py',
        'templates/base.html',
        'templates/index.html',
        'templates/problem.html',
        'templates/partials/step.html',
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(file_path)
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist


def test_tracer_import():
    """Test if tracer can be imported."""
    print("\n" + "="*70)
    print("TESTING TRACER IMPORT")
    print("="*70)
    
    try:
        sys.path.insert(0, str(Path('algorithms')))
        from overlapping_intervals_tracer import OverlappingIntervalsTracer
        print("✅ Tracer imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_tracer_execution():
    """Test if tracer can run."""
    print("\n" + "="*70)
    print("TESTING TRACER EXECUTION")
    print("="*70)
    
    try:
        sys.path.insert(0, str(Path('algorithms')))
        from overlapping_intervals_tracer import OverlappingIntervalsTracer
        
        tracer = OverlappingIntervalsTracer()
        test_intervals = [(540, 660), (600, 720), (540, 720), (900, 960)]
        output = tracer.run(test_intervals)
        
        print(f"✅ Tracer executed successfully")
        print(f"   • Steps captured: {len(output['trace'])}")
        print(f"   • Result: {output['result']}")
        print(f"   • Metadata: {output['metadata']}")
        
        # Verify trace structure
        if len(output['trace']) > 0:
            step0 = output['trace'][0]
            print(f"\n   First step structure:")
            print(f"   • Keys: {list(step0.keys())}")
            print(f"   • Phase: {step0.get('phase')}")
            print(f"   • Action: {step0.get('action')}")
        
        return True
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flask_imports():
    """Test if Flask imports work."""
    print("\n" + "="*70)
    print("TESTING FLASK IMPORTS")
    print("="*70)
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        return True
    except Exception as e:
        print(f"❌ Flask import failed: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def check_templates():
    """Verify template files are valid."""
    print("\n" + "="*70)
    print("CHECKING TEMPLATES")
    print("="*70)
    
    templates = {
        'templates/base.html': [
            ("Has <html> tag", lambda c: "<html" in c.lower()),
            ("Has {% block content %}", lambda c: "{% block content %}" in c),
            ("Has HTMX script", lambda c: "htmx.org" in c),
        ],
        'templates/index.html': [
            ("Extends base", lambda c: "{% extends" in c),
            ("Has content block", lambda c: "{% block content %}" in c),
            ("Has algorithms loop", lambda c: "{% for algo in algorithms %}" in c),
        ],
        'templates/problem.html': [
            ("Extends base", lambda c: "{% extends" in c),
            ("Has HTMX navigation", lambda c: "hx-get" in c),
            ("Has visualization container", lambda c: "visualization-container" in c),
        ],
        'templates/partials/step.html': [
            ("Has step_data", lambda c: "step_data" in c),
            ("Has intervals_state", lambda c: "intervals_state" in c),
            ("Has explanation", lambda c: "explanation" in c),
        ],
    }
    
    all_valid = True
    for template_path, checks in templates.items():
        path = Path(template_path)
        if not path.exists():
            print(f"❌ {template_path} - NOT FOUND")
            all_valid = False
            continue
        
        content = path.read_text()
        
        all_checks_pass = all(check_fn(content) for _, check_fn in checks)
        status = "✅" if all_checks_pass else "❌"
        print(f"{status} {template_path}")
        
        if not all_checks_pass:
            for check_name, check_fn in checks:
                if not check_fn(content):
                    print(f"    ❌ {check_name}")
                    all_valid = False
    
    return all_valid


def main():
    """Run all verification checks."""
    print("\n" + "█"*70)
    print("RECURSION VISUALIZER - SETUP VERIFICATION")
    print("█"*70)
    
    results = {
        "File Structure": check_file_structure(),
        "Flask Imports": test_flask_imports(),
        "Tracer Import": test_tracer_import(),
        "Tracer Execution": test_tracer_execution(),
        "Templates": check_templates(),
    }
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("="*70)
        print("\nYou're ready to run the Flask app:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("="*70)
        print("\nFix the issues above, then run this script again.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()