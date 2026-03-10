import ast
import json
from typing import List, Dict, Any

# Import all rule modules
import rules.unsafe_eval as unsafe_eval
import rules.sql_injection as sql_injection
import rules.command_injection as command_injection
import rules.hardcoded_secret as hardcoded_secret

# List of all active rule detectors
ACTIVE_RULES = [
    unsafe_eval.detect,
    sql_injection.detect,
    command_injection.detect,
    hardcoded_secret.detect,
]

def analyze_code(code: str) -> List[Dict[str, Any]]:
    """
    Analyzes Python source code using AST parsing to detect security vulnerabilities.
    
    Args:
        code (str): The Python source code to analyze.
        
    Returns:
        List[Dict[str, Any]]: A list of detected security issues.
    """
    vulnerabilities = []
    
    try:
        # Parse the source code into an Abstract Syntax Tree (AST)
        # This converts the code string into a structural representation without executing it
        tree = ast.parse(code)
    except SyntaxError as e:
        # If the code isn't valid Python, we handle the syntax error gracefully
        return [{
            "type": "Syntax Error",
            "severity": "High",
            "line": getattr(e, "lineno", 0),
            "message": f"Syntax error: {e.msg}"
        }]
        
    # Execute each rule module on the parsed AST
    for rule_detector in ACTIVE_RULES:
        # Each rule_detector is expected to return a list of vulnerability dicts
        issues = rule_detector(tree)
        vulnerabilities.extend(issues)
        
    return vulnerabilities

if __name__ == "__main__":
    # Example usage / test case to verify functionality
    test_code = "eval(user_input)"
    
    print("Testing Code:")
    print(test_code)
    print("\nExpected output: [{'type': 'Unsafe eval() usage', 'severity': 'High', 'line': 1}]")
    print("\nActual output:")
    
    results = analyze_code(test_code)
    print(json.dumps(results, indent=2))
