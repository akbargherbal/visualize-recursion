"""
Central registry for all algorithms.
Enables dynamic algorithm discovery and registration.
"""

from typing import Dict, Type, List
from algorithms.base_algorithm import BaseAlgorithm


class AlgorithmRegistry:
    """Central registry for all algorithms"""
    
    def __init__(self):
        self._algorithms: Dict[str, Type[BaseAlgorithm]] = {}
    
    def register(self, algorithm_class: Type[BaseAlgorithm]):
        """
        Register an algorithm class (used as decorator).
        
        Usage:
            @registry.register
            class MyAlgorithm(BaseAlgorithm):
                ...
        
        Args:
            algorithm_class: Algorithm class to register
        
        Returns:
            The same class (for decorator pattern)
        """
        instance = algorithm_class()
        self._algorithms[instance.id] = algorithm_class
        print(f"✓ Registered algorithm: {instance.id} ({instance.name})")
        return algorithm_class
    
    def get(self, algorithm_id: str) -> BaseAlgorithm:
        """
        Get algorithm instance by ID.
        
        Args:
            algorithm_id: Unique algorithm identifier
        
        Returns:
            Fresh instance of the algorithm
        
        Raises:
            ValueError: If algorithm not found
        """
        if algorithm_id not in self._algorithms:
            raise ValueError(f"Algorithm '{algorithm_id}' not found")
        return self._algorithms[algorithm_id]()
    
    def list_all(self) -> List[Dict]:
        """
        List all registered algorithms with their metadata.
        
        Returns:
            List of algorithm metadata dictionaries
        """
        return [
            self._algorithms[alg_id]().metadata 
            for alg_id in sorted(self._algorithms.keys())
        ]
    
    def list_by_category(self, category: str) -> List[Dict]:
        """
        List algorithms in a specific category.
        
        Args:
            category: Category name (e.g., 'Intervals', 'Sorting')
        
        Returns:
            List of algorithm metadata for that category
        """
        return [
            meta for meta in self.list_all() 
            if meta['category'].lower() == category.lower()
        ]
    
    def get_categories(self) -> List[str]:
        """
        Get list of all unique categories.
        
        Returns:
            Sorted list of category names
        """
        categories = set(
            algo().metadata['category'] 
            for algo in self._algorithms.values()
        )
        return sorted(categories)


# Global registry instance
registry = AlgorithmRegistry()