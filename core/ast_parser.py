import ast
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class LoopInfo:
    type: str 
    line: int
    nested_level: int
    iterator_type: Optional[str] = None

@dataclass
class FunctionInfo:
    name: str
    line: int
    args_count: int
    has_recursion: bool = False
    calls_other_functions: List[str] = None

@dataclass
class ASTAnalysis:
    loops: List[LoopInfo]
    functions: List[FunctionInfo]
    max_nesting_level: int
    recursive_calls: List[str]
    builtin_calls: List[str]
    data_structures: List[str]

class ASTParser:    
    def __init__(self):
        self.current_nesting = 0
        self.max_nesting = 0
        self.loops = []
        self.functions = []
        self.recursive_calls = []
        self.builtin_calls = []
        self.data_structures = []
        self.current_function = None
    
    def parse(self, code: str) -> ASTAnalysis:
        self._reset()
        
        try:
            tree = ast.parse(code)
            self._analyze_node(tree)
            
            return ASTAnalysis(
                loops=self.loops,
                functions=self.functions,
                max_nesting_level=self.max_nesting,
                recursive_calls=self.recursive_calls,
                builtin_calls=list(set(self.builtin_calls)),
                data_structures=list(set(self.data_structures))
            )
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
    
    def _reset(self):
        """Reset parserstat"""
        self.current_nesting = 0
        self.max_nesting = 0
        self.loops = []
        self.functions = []
        self.recursive_calls = []
        self.builtin_calls = []
        self.data_structures = []
        self.current_function = None
    
    def _analyze_node(self, node: ast.AST):
        """Recursively analyze AST nodes"""
        if isinstance(node, ast.For):
            self._handle_for_loop(node)
        elif isinstance(node, ast.While):
            self._handle_while_loop(node)
        elif isinstance(node, ast.FunctionDef):
            self._handle_function_def(node)
        elif isinstance(node, ast.Call):
            self._handle_function_call(node)
        elif isinstance(node, (ast.List, ast.Dict, ast.Set)):
            self._handle_data_structure(node)
        
        for child in ast.iter_child_nodes(node):
            self._analyze_node(child)
    
    def _handle_for_loop(self, node: ast.For):
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        
        iterator_type = None
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
            iterator_type = node.iter.func.id
        
        self.loops.append(LoopInfo(
            type='for',
            line=node.lineno,
            nested_level=self.current_nesting,
            iterator_type=iterator_type
        ))
        
        for child in node.body:
            self._analyze_node(child)
        
        self.current_nesting -= 1
    
    def _handle_while_loop(self, node: ast.While):
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        
        self.loops.append(LoopInfo(
            type='while',
            line=node.lineno,
            nested_level=self.current_nesting
        ))
        
        for child in node.body:
            self._analyze_node(child)
        
        self.current_nesting -= 1
    
    def _handle_function_def(self, node: ast.FunctionDef):
        prev_function = self.current_function
        self.current_function = node.name
        
        function_info = FunctionInfo(
            name=node.name,
            line=node.lineno,
            args_count=len(node.args.args),
            calls_other_functions=[]
        )
        
        for child in node.body:
            self._analyze_node(child)
        
        self.functions.append(function_info)
        self.current_function = prev_function
    
    def _handle_function_call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # Check forrecursion
            if self.current_function and func_name == self.current_function:
                self.recursive_calls.append(func_name)
            
            # Track common builtin functions that affect complexity
            if func_name in ['sorted', 'max', 'min', 'sum', 'len', 'range']:
                self.builtin_calls.append(func_name)
    
    def _handle_data_structure(self, node: ast.AST):
        """Handle data structure creation."""
        if isinstance(node, ast.List):
            self.data_structures.append('list')
        elif isinstance(node, ast.Dict):
            self.data_structures.append('dict')
        elif isinstance(node, ast.Set):
            self.data_structures.append('set') 