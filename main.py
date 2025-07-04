import click
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from core import ComplexityAnalyzer
from examples.sample_codes import SAMPLE_CODES
from config import Config

console = Console()

@click.group()
def cli():
    """Time Complexity Analyzer - Analyze code complexity using LLM + AST parsing."""
    pass

@cli.command()
@click.argument('code', type=str)
@click.option('--format', default='rich', help='Output format: rich, json, plain')
@click.option('--api-key', help='Gemini API key (or set GEMINI_API_KEY env var)')
def analyze(code: str, format: str, api_key: str):
    """Analyze time complexity of given code."""
    
    try:
        analyzer = ComplexityAnalyzer(api_key)
        result = analyzer.analyze(code)
        
        if format == 'json':
            click.echo(json.dumps(result, indent=2))
        elif format == 'plain':
            _print_plain_result(result)
        else:
            _print_rich_result(result)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--format', default='rich', help='Output format: rich, json, plain')
@click.option('--api-key', help='Gemini API key (or set GEMINI_API_KEY env var)')
def analyze_file(filename: str, format: str, api_key: str):
    """Analyze time complexity of code in a file."""
    
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        analyzer = ComplexityAnalyzer(api_key)
        result = analyzer.analyze(code)
        
        if format == 'json':
            click.echo(json.dumps(result, indent=2))
        elif format == 'plain':
            _print_plain_result(result)
        else:
            _print_rich_result(result)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('--api-key', help='Gemini API key (or set GEMINI_API_KEY env var)')
def demo(api_key: str):
    """Run demo with sample code snippets."""
    
    try:
        analyzer = ComplexityAnalyzer(api_key)
        
        console.print("[bold blue]Time Complexity Analyzer Demo[/bold blue]")
        console.print("Analyzing sample code snippets...\n")
        
        for name, sample in SAMPLE_CODES.items():
            console.print(f"[yellow]Analyzing: {name}[/yellow]")
            
            # Show code
            syntax = Syntax(sample['code'], "python", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=f"Code: {name}"))
            
            # Analyze
            result = analyzer.analyze(sample['code'])
            
            # Show results
            if 'final_analysis' in result:
                final = result['final_analysis']
                
                table = Table(title="Analysis Results")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="magenta")
                table.add_column("Expected", style="green")
                
                table.add_row("Time Complexity", 
                            final['time_complexity'], 
                            sample['expected_complexity'])
                table.add_row("Space Complexity", 
                            final['space_complexity'], 
                            "N/A")
                table.add_row("Confidence", 
                            f"{final['confidence']:.2f}", 
                            "N/A")
                
                console.print(table)
                console.print(f"[dim]Explanation: {final['explanation'][:100]}...[/dim]\n")
            
            console.print("-" * 50)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

def _print_rich_result(result: dict):
    
    if 'error' in result:
        console.print(f"[red]Error: {result['error']}[/red]")
        return
    
    # Code panel
    if 'code' in result:
        syntax = Syntax(result['code'], "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Analyzed Code"))
    
    # Results table
    if 'final_analysis' in result:
        final = result['final_analysis']
        
        table = Table(title="Complexity Analysis Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Time Complexity", final['time_complexity'])
        table.add_row("Space Complexity", final['space_complexity'])
        table.add_row("Confidence", f"{final['confidence']:.2f}")
        table.add_row("Analysis Method", final['analysis_method'])
        
        console.print(table)
        
        if final.get('explanation'):
            console.print(Panel(final['explanation'], title="Explanation"))
        
        if final.get('recommendations'):
            rec_text = "\n".join(f"• {rec}" for rec in final['recommendations'])
            console.print(Panel(rec_text, title="Recommendations"))

def _print_plain_result(result: dict):
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    if 'final_analysis' in result:
        final = result['final_analysis']
        print(f"Time Complexity: {final['time_complexity']}")
        print(f"Space Complexity: {final['space_complexity']}")
        print(f"Confidence: {final['confidence']:.2f}")
        print(f"Analysis Method: {final['analysis_method']}")
        
        if final.get('explanation'):
            print(f"Explanation: {final['explanation']}")

if __name__ == '__main__':
    cli() 