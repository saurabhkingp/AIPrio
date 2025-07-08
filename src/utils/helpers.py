import pandas as pd
import os
import sys
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
    print(testcases_names)
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
