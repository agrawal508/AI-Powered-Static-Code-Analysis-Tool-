import ast
from typing import List, Dict, Any

def detect(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects usages of unsafe functions like eval() and exec().
    
    Args:
        tree (ast.AST): The parsed Abstract Syntax Tree of the code.
        
    Returns:
        List[Dict[str, Any]]: A list of detected vulnerabilities.
    """
    issues = []
    
    # ast.walk recursively yields all nodes in the AST
    for node in ast.walk(tree):
        # Look for function calls
        if isinstance(node, ast.Call):
            # Check if it's a direct function call by name (e.g., eval() rather than obj.eval())
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in ("eval", "exec"):
                    issues.append({
                        "type": f"Unsafe {func_name}() usage",
                        "severity": "High",
                        "line": node.lineno,
                    })
                    
    return issues
