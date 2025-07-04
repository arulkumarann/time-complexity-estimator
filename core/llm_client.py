import google.generativeai as genai
from typing import Optional, Dict, Any
import json
import re
from config import Config

class LLMClient:
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def analyze_complexity(self, code: str, ast_analysis: Dict[str, Any]) -> Dict[str, Any]:
        
        prompt = self._build_analysis_prompt(code, ast_analysis)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_llm_response(response.text)
        except Exception as e:
            return {
                'error': f'LLM analysis failed: {str(e)}',
                'time_complexity': 'Unknown',
                'space_complexity': 'Unknown',
                'confidence': 0.0
            }
    
    def _build_analysis_prompt(self, code: str, ast_analysis: Dict[str, Any]) -> str:
        
        return f"""
You are an expert algorithm analyst. Analyze the following Python code snippet and provide a detailed time complexity analysis.

CODE TO ANALYZE:
```python
{code}
```

STRUCTURAL ANALYSIS (from AST parsing):
- Maximum nesting level: {ast_analysis.get('max_nesting_level', 0)}
- Number of loops: {len(ast_analysis.get('loops', []))}
- Loop types: {[loop['type'] for loop in ast_analysis.get('loops', [])]}
- Recursive functions: {ast_analysis.get('recursive_calls', [])}
- Built-in function calls: {ast_analysis.get('builtin_calls', [])}
- Data structures used: {ast_analysis.get('data_structures', [])}

Please provide your analysis in the following JSON format:
{{
    "time_complexity": "O(...)",
    "space_complexity": "O(...)",
    "explanation": "Detailed explanation of the complexity analysis",
    "bottlenecks": ["list", "of", "performance", "bottlenecks"],
    "confidence": 0.0-1.0,
    "reasoning": "Step-by-step reasoning for the complexity determination"
}}

Focus on:
1. Loop analysis and nesting effects
2. Recursive call patterns
3. Built-in function complexities
4. Data structure operations
5. Overall algorithm efficiency

Be precise and provide confidence score based on code clarity and complexity patterns.
"""
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response and extract structured data."""
        
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        return self._extract_fallback_info(response_text)
    
    def _extract_fallback_info(self, text: str) -> Dict[str, Any]:
        
        time_complexity = self._extract_complexity(text, 'time')
        space_complexity = self._extract_complexity(text, 'space')
        
        return {
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'explanation': text[:500] + "..." if len(text) > 500 else text,
            'bottlenecks': [],
            'confidence': 0.5,
            'reasoning': 'Fallback analysis due to parsing issues'
        }
    
    def _extract_complexity(self, text: str, complexity_type: str) -> str:
        
        pattern = rf'{complexity_type}.*?complexity.*?O\([^)]+\)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            o_match = re.search(r'O\([^)]+\)', match.group(0))
            if o_match:
                return o_match.group(0)
        
        return 'O(?)' 