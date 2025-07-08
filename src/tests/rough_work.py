import ast

def extract_function_names(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())
    return [node.name if node.name.startswith("test_") else None for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
func_names_map={}
file_path = r"ai-test-prioritization\src\tests\test_sample_cases.py"
function_names = extract_function_names(file_path)
function_names = [name for name in function_names if name is not None]
for i,j in enumerate(function_names,1):
    func_names_map[f'TC_{i}'] = j
print(func_names_map)
