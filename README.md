# Time Complexity Analyzer

A system that estimates the time and space complexity of Python code snippets using a hybrid approach combining Abstract Syntax Tree (AST) parsing with Large Language Model (LLM) analysis.

## Features

- **Hybrid Analysis**: Combines static AST parsing with AI-powered analysis
- **Multiple Output Formats**: Rich console output, JSON, and plain text
- **Comprehensive Metrics**: Time complexity, space complexity, confidence scores
- **Smart Recommendations**: Optimization suggestions based on code patterns
- **CLI Interface**: Easy-to-use command-line interface
- **Demo Mode**: Built-in examples with known complexities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arulkumarann/time-complexity-estimator.git
cd time-complexity-estimator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

## Usage

### Analyze Code Directly

```bash
python main.py analyze "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr"
```

### Analyze Code from File

```bash
python main.py analyze-file algorithm.py
```

### Run Demo

```bash
python main.py demo
```

### Output Formats

- **Rich** (default): Beautiful console output with syntax highlighting
- **JSON**: Machine-readable format for integration
- **Plain**: Simple text output

```bash
python main.py analyze "code here" --format json
```

### Components

1. **AST Parser** (`core/ast_parser.py`):
   - Extracts loops, functions, nesting levels
   - Identifies recursive calls and data structures
   - Provides structural complexity indicators

2. **LLM Client** (`core/llm_client.py`):
   - Integrates with Google's Gemini API
   - Analyzes code with AST context
   - Provides detailed explanations and confidence scores

3. **Complexity Analyzer** (`core/complexity_analyzer.py`):
   - Combines AST and LLM analyses
   - Generates final complexity estimates
   - Provides optimization recommendations

## Sample Outputs

### Example 1: Linear Search
```
Time Complexity: O(n)
Space Complexity: O(1)
Confidence: 0.95
Analysis Method: LLM (high confidence)
```

### Example 2: Bubble Sort
```
Time Complexity: O(n²)
Space Complexity: O(1)
Confidence: 0.92
Analysis Method: LLM + AST validation
Key Factors: 2 nested loops, no recursion
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Configuration

Edit `config.py` to customize:
- API settings
- Analysis parameters
- Output preferences

## API Integration

Use the analyzer programmatically:

```python
from core import ComplexityAnalyzer

analyzer = ComplexityAnalyzer(api_key="your-key")
result = analyzer.analyze(code)
print(result['final_analysis']['time_complexity'])
```
