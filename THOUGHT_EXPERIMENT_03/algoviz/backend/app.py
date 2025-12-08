"""
Flask API server for algorithm visualization.
Provides REST endpoints for algorithm discovery and trace generation.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from algorithms.registry import registry

# Import all algorithms to register them
from algorithms.interval_coverage.algorithm import IntervalCoverageAlgorithm

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


@app.route('/api/algorithms', methods=['GET'])
def list_algorithms():
    """Get list of all available algorithms."""
    try:
        algorithms = registry.list_all()
        return jsonify({
            'success': True,
            'algorithms': algorithms,
            'count': len(algorithms)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/algorithms/categories', methods=['GET'])
def list_categories():
    """Get list of all algorithm categories."""
    try:
        categories = registry.get_categories()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/algorithms/<category>', methods=['GET'])
def list_by_category(category):
    """Get algorithms by category."""
    try:
        algorithms = registry.list_by_category(category)
        return jsonify({
            'success': True,
            'category': category,
            'algorithms': algorithms,
            'count': len(algorithms)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/algorithm/<algorithm_id>', methods=['GET'])
def get_algorithm_info(algorithm_id):
    """Get detailed algorithm metadata."""
    try:
        algorithm = registry.get(algorithm_id)
        return jsonify({
            'success': True,
            'algorithm': algorithm.metadata
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/algorithm/<algorithm_id>/example', methods=['GET'])
def get_example(algorithm_id):
    """Get default example input for an algorithm."""
    try:
        algorithm = registry.get(algorithm_id)
        example = algorithm.get_default_example()
        return jsonify({
            'success': True,
            'example': example
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/algorithm/<algorithm_id>/trace', methods=['POST'])
def generate_trace(algorithm_id):
    """Generate execution trace for algorithm with user input."""
    try:
        algorithm = registry.get(algorithm_id)
        input_data = request.json
        
        # Validate input
        if not algorithm.validate_input(input_data):
            return jsonify({
                'success': False,
                'error': 'Invalid input format',
                'details': 'Input does not match expected schema'
            }), 400
        
        # Execute algorithm and get trace
        trace, result = algorithm.execute_traced(input_data)
        
        return jsonify({
            'success': True,
            'trace': trace,
            'result': result
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Execution failed: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'registered_algorithms': len(registry.list_all())
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Algorithm Visualizer Backend")
    print("="*60)
    print(f"Registered algorithms: {len(registry.list_all())}")
    for algo in registry.list_all():
        print(f"  • {algo['id']}: {algo['name']}")
    print("="*60)
    print("Server running on http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')