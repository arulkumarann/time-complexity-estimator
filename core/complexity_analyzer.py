from typing import Dict, Any, Optional
from dataclasses import asdict
import json

from .ast_parser import ASTParser
from .llm_client import LLMClient

class ComplexityAnalyzer:
    """Main analyzer that combines AST parsing with LLM analysis."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.ast_parser = ASTParser()
        self.llm_client = LLMClient(api_key)
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """Perform complete complexity analysis."""
        
        if not code or not code.strip():
            raise ValueError("Code cannot be empty")
        
        try:
            ast_analysis = self.ast_parser.parse(code)
        except Exception as e:
            return {
                'error': f'AST parsing failed: {str(e)}',
                'ast_analysis': None,
                'llm_analysis': None,
                'final_analysis': None
            }
        
        ast_dict = asdict(ast_analysis)
        llm_analysis = self.llm_client.analyze_complexity(code, ast_dict)
        
        final_analysis = self._combine_analyses(ast_analysis, llm_analysis)
        
        return {
            'ast_analysis': ast_dict,
            'llm_analysis': llm_analysis,
            'final_analysis': final_analysis,
            'code': code
        }
    
    def _combine_analyses(self, ast_analysis, llm_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Combine AST and LLM analyses for final result."""
        
        # Extract key metrics
        loop_complexity = self._estimate_loop_complexity(ast_analysis.loops)
        has_recursion = len(ast_analysis.recursive_calls) > 0
        
        llm_time = llm_analysis.get('time_complexity', 'O(?)')
        llm_confidence = llm_analysis.get('confidence', 0.5)
        
        if llm_confidence > 0.8:
            final_complexity = llm_time
            analysis_method = 'LLM (high confidence)'
        elif loop_complexity and llm_confidence > 0.5:
            final_complexity = llm_time
            analysis_method = 'LLM + AST validation'
        else:
            final_complexity = loop_complexity or 'O(1)'
            analysis_method = 'AST-based estimation'
        
        return {
            'time_complexity': final_complexity,
            'space_complexity': llm_analysis.get('space_complexity', 'O(1)'),
            'confidence': llm_confidence,
            'analysis_method': analysis_method,
            'key_factors': {
                'loops': len(ast_analysis.loops),
                'max_nesting': ast_analysis.max_nesting_level,
                'recursion': has_recursion,
                'builtin_calls': ast_analysis.builtin_calls
            },
            'explanation': llm_analysis.get('explanation', 'No detailed explanation available'),
            'bottlenecks': llm_analysis.get('bottlenecks', []),
            'recommendations': self._generate_recommendations(ast_analysis, llm_analysis)
        }
    
    def _estimate_loop_complexity(self, loops) -> Optional[str]:
        
        if not loops:
            return None
        
        max_nesting = max(loop.nested_level for loop in loops)
        
        if max_nesting == 1:
            return 'O(n)'
        elif max_nesting == 2:
            return 'O(n²)'
        elif max_nesting == 3:
            return 'O(n³)'
        else:
            return f'O(n^{max_nesting})'
    
    def _generate_recommendations(self, ast_analysis, llm_analysis: Dict[str, Any]) -> list:
        
        recommendations = []
        
        # Check for nested loops
        if ast_analysis.max_nesting_level > 2:
            recommendations.append(
                f"Consider optimizing nested loops (depth: {ast_analysis.max_nesting_level}). "
                "Look for opportunities to reduce nesting or use more efficient algorithms."
            )
        
        # Check for inefficient built-ins
        if 'sorted' in ast_analysis.builtin_calls:
            recommendations.append(
                "Consider if sorting is necessary or if a more efficient approach exists."
            )
        
        # Check for recursion
        if ast_analysis.recursive_calls:
            recommendations.append(
                "Recursive functions detected. Consider memoization or iterative approaches "
                "for better performance."
            )
        
        return recommendations 