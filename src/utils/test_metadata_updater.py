import ast
import pandas as pd
import subprocess
import os

def extract_function_names_map(test_file_path):
    func_names_map = {}
    with open(test_file_path, "r") as file:
        tree = ast.parse(file.read())
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]
    for i, name in enumerate(function_names, 1):
        func_names_map[f'TC_{i}'] = name
    return func_names_map

def get_changed_lines(filepath, since_commit="HEAD~1"):
    # Get changed lines in the file since the given commit
    result = subprocess.run(
        ["git", "diff", since_commit, "HEAD", "--unified=0", filepath],
        capture_output=True, text=True
    )
    changed_lines = set()
    for line in result.stdout.splitlines():
        if line.startswith("@@"):
            # Example: @@ -10,0 +11,2 @@
            parts = line.split(" ")
            for part in parts:
                if part.startswith("+"):
                    # +11,2 means lines 11 and 12 were added/changed
                    nums = part[1:].split(",")
                    start = int(nums[0])
                    count = int(nums[1]) if len(nums) > 1 else 1
                    changed_lines.update(range(start, start + count))
    return changed_lines

def get_test_function_lines(filepath):
    # Map test function names to their line ranges
    with open(filepath, "r") as f:
        tree = ast.parse(f.read(), filename=filepath)
    func_lines = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start)
            func_lines[node.name] = set(range(start, end + 1))
    return func_lines

def update_recently_changed(csv_path, test_file, since_commit="HEAD~1"):
    df = pd.read_csv(csv_path)
    changed_lines = get_changed_lines(test_file, since_commit)
    func_lines = get_test_function_lines(test_file)
    df["recently_changed"] = 0
    for idx, row in df.iterrows():
        func_name = row["test_case_id"]  # Should match test function name
        if func_name in func_lines and changed_lines & func_lines[func_name]:
            df.at[idx, "recently_changed"] = 1
    df.to_csv(csv_path, index=False)
    print("recently_changed updated in", csv_path)
