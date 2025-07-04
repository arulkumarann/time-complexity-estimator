import pytest
from core.llm_client import LLMClient

class DummyModel:
    def generate_content(self, prompt):
        class Response:
            text = '{"time_complexity": "O(n)", "space_complexity": "O(1)", "confidence": 0.9}'
        return Response()

def test_llm_client_parses_json(monkeypatch):
    client = LLMClient(api_key="dummy")
    monkeypatch.setattr(client, "model", DummyModel())
    result = client.analyze_complexity("def f(): pass", {})
    assert result["time_complexity"] == "O(n)"
    assert result["space_complexity"] == "O(1)"
    assert result["confidence"] == 0.9 