import pytest
from core.complexity_analyzer import ComplexityAnalyzer

class DummyLLM:
    def analyze_complexity(self, code, ast):
        return {"time_complexity": "O(n)", "space_complexity": "O(1)", "confidence": 0.95, "explanation": "Test", "bottlenecks": [], "reasoning": "Test"}

def test_complexity_analyzer_integration(monkeypatch):
    analyzer = ComplexityAnalyzer(api_key="dummy")
    monkeypatch.setattr(analyzer, "llm_client", DummyLLM())
    code = "for i in range(10): pass"
    result = analyzer.analyze(code)
    assert result["final_analysis"]["time_complexity"] == "O(n)"
    assert result["final_analysis"]["confidence"] == 0.95 