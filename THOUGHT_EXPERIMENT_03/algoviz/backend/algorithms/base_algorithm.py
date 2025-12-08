"""
Abstract base class for all algorithms.
Provides consistent interface and metadata loading.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
import json
import os


class BaseAlgorithm(ABC):
    """Abstract base class for all algorithms"""
    
    def __init__(self):
        self.metadata = self.load_metadata()
    
    @abstractmethod
    def execute_traced(self, input_data: Any) -> Tuple[Dict, Any]:
        """
        Execute algorithm with full trace capture.
        
        Args:
            input_data: Algorithm input (format depends on algorithm)
        
        Returns:
            tuple: (trace_dict, result)
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data format.
        
        Args:
            input_data: Data to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_default_example(self) -> Any:
        """
        Get default example input for this algorithm.
        
        Returns:
            Default input data
        """
        pass
    
    def load_metadata(self) -> Dict:
        """Load metadata.json from algorithm directory"""
        # Get the directory where the algorithm class is defined
        import inspect
        class_file = inspect.getfile(self.__class__)
        class_dir = os.path.dirname(class_file)
        metadata_path = os.path.join(class_dir, 'metadata.json')
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                return json.load(f)
        else:
            # Return minimal metadata if file doesn't exist
            return {
                'id': self.__class__.__name__.lower(),
                'name': self.__class__.__name__,
                'category': 'Unknown',
                'description': 'No description available'
            }
    
    @property
    def id(self) -> str:
        """Get algorithm ID"""
        return self.metadata['id']
    
    @property
    def name(self) -> str:
        """Get algorithm name"""
        return self.metadata['name']
    
    @property
    def category(self) -> str:
        """Get algorithm category"""
        return self.metadata['category']
    
    @property
    def complexity(self) -> Dict[str, str]:
        """Get time/space complexity"""
        return self.metadata.get('complexity', {
            'time': 'Unknown',
            'space': 'Unknown'
        })