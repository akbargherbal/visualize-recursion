import os
import json
from pathlib import Path


def create_file(path, content=""):
    """Create a file with optional content."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created: {path}")


def create_project_structure():
    """Create the entire project structure with empty files."""

    # Root directory
    root = "algoviz"

    # Backend structure
    backend_files = {
        # Main Flask app
        f"{root}/backend/app.py": "",
        f"{root}/backend/config.py": "",
        f"{root}/backend/requirements.txt": "",
        # Core modules
        f"{root}/backend/core/__init__.py": "",
        f"{root}/backend/core/tracer.py": "",
        f"{root}/backend/core/validation.py": "",
        f"{root}/backend/core/serialization.py": "",
        # Examples
        f"{root}/backend/examples/interval_coverage.json": "",
        f"{root}/backend/examples/interval_intersection.json": "",
    }

    # Algorithms structure
    algorithm_dirs = [
        "interval_coverage",
        "interval_intersection",
        "merge_intervals",
        "sorting/quicksort",
        "sorting/mergesort",
    ]

    # Add algorithm files
    for algo in algorithm_dirs:
        backend_files.update(
            {
                f"{root}/backend/algorithms/{algo}/__init__.py": "",
                f"{root}/backend/algorithms/{algo}/algorithm.py": "",
                f"{root}/backend/algorithms/{algo}/tracer.py": "",
                f"{root}/backend/algorithms/{algo}/metadata.json": "{}",
            }
        )

    # Add base algorithm files
    backend_files.update(
        {
            f"{root}/backend/algorithms/__init__.py": "",
            f"{root}/backend/algorithms/base_algorithm.py": "",
            f"{root}/backend/algorithms/registry.py": "",
        }
    )

    # Frontend structure
    frontend_files = {
        # Pages
        f"{root}/frontend/src/pages/HomePage.jsx": "",
        f"{root}/frontend/src/pages/AlgorithmPage.jsx": "",
        f"{root}/frontend/src/pages/AboutPage.jsx": "",
        # Common components
        f"{root}/frontend/src/components/common/Header.jsx": "",
        f"{root}/frontend/src/components/common/AlgorithmCard.jsx": "",
        f"{root}/frontend/src/components/common/PlaybackControls.jsx": "",
        # Visualization components
        f"{root}/frontend/src/components/visualizations/TimelineView.jsx": "",
        f"{root}/frontend/src/components/visualizations/TreeView.jsx": "",
        f"{root}/frontend/src/components/visualizations/ArrayView.jsx": "",
        f"{root}/frontend/src/components/visualizations/GraphView.jsx": "",
        f"{root}/frontend/src/components/visualizations/CallStackView.jsx": "",
        # Input components
        f"{root}/frontend/src/components/inputs/IntervalInput.jsx": "",
        f"{root}/frontend/src/components/inputs/ArrayInput.jsx": "",
        f"{root}/frontend/src/components/inputs/GraphInput.jsx": "",
        # Hooks
        f"{root}/frontend/src/hooks/useTracePlayer.js": "",
        f"{root}/frontend/src/hooks/useAlgorithmList.js": "",
        f"{root}/frontend/src/hooks/useVisualization.js": "",
        # Services and utils
        f"{root}/frontend/src/services/api.js": "",
        f"{root}/frontend/src/utils/traceHelpers.js": "",
        f"{root}/frontend/src/utils/visualizationRegistry.js": "",
        # Main app files
        f"{root}/frontend/src/App.jsx": "",
        f"{root}/frontend/src/index.js": "",
        # Config files
        f"{root}/frontend/package.json": json.dumps(
            {
                "name": "algoviz-frontend",
                "version": "0.1.0",
                "private": True,
                "dependencies": {
                    "react": "^18.0.0",
                    "react-dom": "^18.0.0",
                    "react-router-dom": "^6.0.0",
                    "axios": "^1.0.0",
                },
                "scripts": {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject",
                },
            },
            indent=2,
        ),
        # Public directory (empty)
        f"{root}/frontend/public/.gitkeep": "",
    }

    # Root files
    root_files = {
        f"{root}/README.md": "# AlgoViz - Algorithm Visualization Tool\n\nInteractive visualization of algorithms.",
    }

    # Create all files
    all_files = {**backend_files, **frontend_files, **root_files}

    for filepath, content in all_files.items():
        create_file(filepath, content)

    print(f"\n✅ Project structure created at: {root}")
    print("📁 Total files created:", len(all_files))


if __name__ == "__main__":
    print("Scaffolding AlgoViz project...\n")
    create_project_structure()

    print("\n📦 Next steps:")
    print("1. cd algoviz/backend && pip install -r requirements.txt")
    print("2. cd algoviz/frontend && npm install")
    print("3. Check README.md for project details")
