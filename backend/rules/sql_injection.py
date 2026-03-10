import ast
from typing import List, Dict, Any

def detect(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Detects possible SQL Injection vulnerabilities.
    Looks for cursor.execute() calls that use string concatenation or f-strings.
    """
    issues = []
    
    for node in ast.walk(tree):
        # Look for function calls
        if isinstance(node, ast.Call):
            # Check if it's a method call like obj.execute()
            if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
                # Check the first argument of execute()
                if node.args:
                    first_arg = node.args[0]
                    
                    # Vulnerable: String concatenation (e.g., "SELECT * FROM users WHERE id=" + user_input)
                    if isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Add):
                        issues.append({
                            "type": "Possible SQL Injection",
                            "severity": "Critical",
                            "line": node.lineno,
                            "message": "String concatenation detected in execute() call."
                        })
                    
                    # Vulnerable: F-strings (e.g., f"SELECT * FROM users WHERE id={user_input}")
                    elif isinstance(first_arg, ast.JoinedStr):
                        issues.append({
                            "type": "Possible SQL Injection",
                            "severity": "Critical",
                            "line": node.lineno,
                            "message": "F-string detected in execute() call."
                        })
                        
                    # Vulnerable: .format() (e.g., "SELECT * FROM users WHERE id={}".format(user_input))
                    elif isinstance(first_arg, ast.Call) and isinstance(first_arg.func, ast.Attribute):
                        if first_arg.func.attr == "format":
                            issues.append({
                                "type": "Possible SQL Injection",
                                "severity": "Critical",
                                "line": node.lineno,
                                "message": ".format() string formatting detected in execute() call."
                            })
                            
                    # Vulnerable: string modulo % (e.g., "SELECT * FROM ... %s" % user_input)
                    elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Mod):
                       issues.append({
                           "type": "Possible SQL Injection",
                           "severity": "Critical",
                           "line": node.lineno,
                           "message": "String formatting (%) detected in execute() call."
                       })

    return issues
