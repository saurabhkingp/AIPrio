import pandas as pd
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.test_metadata_updater import extract_function_names_map
from utils.variables import *

def log_message(message):
    print(f"[LOG] {message}")

def calculate_metrics(true_labels, predicted_labels):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='weighted')
    recall = recall_score(true_labels, predicted_labels, average='weighted')
    f1 = f1_score(true_labels, predicted_labels, average='weighted')

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

def generate_sample_test_data(filepath):
    """
    Generates a sample CSV dataset for test case prioritization.
    """
    testcases_names=extract_function_names_map(TEST_SAMPLE_CASES)
    data = {
        'test_case_id': [f'{i}' for i in testcases_names.values()],
        'last_result': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0],  # 1=pass, 0=fail
        'duration': [12, 30, 15, 10, 25, 14, 28, 11, 13, 27],
        'recently_changed': [1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
        'priority': [2, 1, 2, 3, 1, 2, 1, 3, 2, 1]  # 1=high, 2=medium, 3=low
    }
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Sample test data generated at {filepath}")

def update_csv_with_total_durations_and_results(csv_path, durations_path):
    """
    Sums durations for all parameterized variants and updates the CSV with total duration and result per base test name.
    Handles multiple parameterized test functions.
    Sets result to 1 for any fail (None or 1), 0 for all pass.
    Overwrites last_result for all test cases found in durations.
    """
    df = pd.read_csv(csv_path)
    with open(durations_path, "r") as f:
        durations = json.load(f)

    total_durations = {}
    results_map = {}
    for k, v in durations.items():
        base = k.split("[")[0]
        duration = 0
        result = 0
        if isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], (int, float)):
                duration = v[0]
            if len(v) > 1:
                if v[1] is None or v[1] == 1:
                    result = 1
                else:
                    result = 0
        elif isinstance(v, (int, float)):
            duration = v
            result = 0
        total_durations.setdefault(base, 0)
        total_durations[base] += duration
        # If any variant failed, mark as fail (1), else pass (0)
        if base not in results_map:
            results_map[base] = result
        else:
            results_map[base] = max(results_map[base], result)

    # Overwrite last_result for all test cases found in durations
    for idx, row in df.iterrows():
        func_name = row["test_case_id"]
        if func_name in total_durations:
            df.at[idx, "duration"] = round(total_durations[func_name], 4)
        if func_name in results_map:
            df.at[idx, "last_result"] = results_map[func_name]
        else:
            # If not found in results_map, set to empty or default
            df.at[idx, "last_result"] = ''
    df.to_csv(csv_path, index=False)
    print("Updated CSV with total test durations and results.")

def generate_test_data_from_functions(csv_path, test_file):
    from utils.test_metadata_updater import extract_function_names_map
    import pandas as pd
    func_names_map = extract_function_names_map(test_file)
    test_case_ids = list(func_names_map.values())
    columns = ['test_case_id', 'last_result', 'duration', 'recently_changed', 'priority']
    df = pd.DataFrame({
        'test_case_id': test_case_ids,
        'last_result': ['']*len(test_case_ids),
        'duration': ['']*len(test_case_ids),
        'recently_changed': ['']*len(test_case_ids),
        'priority': ['']*len(test_case_ids)
    })
    df.to_csv(csv_path, index=False)
    print(f"Created new CSV with columns and test_case_ids from {test_file}, all other columns empty.")
