from src.data.dataset_loader import DatasetLoader
from src.ai.prioritizer import TestCasePrioritizer
from src.utils.test_metadata_updater import update_recently_changed, extract_function_names_map
from src.utils.variables import *
from utils.helpers import update_csv_with_total_durations_and_results
from utils.helpers import generate_test_data_from_functions
import os
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import ast
from prettytable import PrettyTable
import pandas as pd
from sklearn.cluster import KMeans

def main():
    """
    Main entry point for the AI-powered test case prioritization pipeline.
    - Loads a sample dataset of test cases.
    - Trains a Random Forest model to predict test case priority.
    - Prints the prioritized test cases from highest to lowest.
    - Displays two plots:
        1. Feature importance of the model, showing which features make a test case important.
        2. The prioritized test cases with their predicted priority values.
    """
    
    table = PrettyTable()

    if not os.path.exists(TEST_DATA_CSV) or os.stat(TEST_DATA_CSV).st_size == 0:
        generate_test_data_from_functions(TEST_DATA_CSV, TEST_SAMPLE_CASES)
    
    # Update the 'recently_changed' column in the dataset
    update_recently_changed(
        csv_path=TEST_DATA_CSV,
        test_file=TEST_SAMPLE_CASES,
        since_commit=SINCE_COMMIT
    )
    data_path = TEST_DATA_CSV

    # Check if CSV has enough feature data for ML prioritization
    df = pd.read_csv(TEST_DATA_CSV)
    feature_cols = ["last_result", "duration", "recently_changed"]
    # If all feature columns are empty or NaN, skip ML prioritization
    if df[feature_cols].isnull().all().all() or df[feature_cols].eq('').all().all():
        print("No historical test data found. Running all tests to collect initial metrics for prioritization.")
        # Run all tests in default order
        result = subprocess.run([
            'pytest',
            TESTS_DIR,
            '--maxfail=3',
            '--disable-warnings',
            '-v'
        ], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # After pytest run, update CSV with total durations and results
        update_csv_with_total_durations_and_results(TEST_DATA_CSV, os.path.join(PROJECT_ROOT, "test_durations.json"))
        return
    # If priority column is empty or NaN, use clustering to assign default priorities
    if df['priority'].isnull().all() or df['priority'].eq('').all():
        from sklearn.cluster import KMeans

        df = pd.read_csv(TEST_DATA_CSV)
        features = df[["last_result", "duration", "recently_changed"]].fillna(0)
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['priority'] = kmeans.fit_predict(features)
        # Optionally, map cluster labels to 1=high, 2=medium, 3=low
        priority_map = {0:1, 1:2, 2:3}
        df['priority'] = df['priority'].map(priority_map)
        df.to_csv(TEST_DATA_CSV, index=False)

    loader = DatasetLoader(data_path)
    X, y = loader.get_features_and_labels()
    test_case_ids = loader.get_test_cases()

    prioritizer = TestCasePrioritizer()
    prioritizer.train(X, y)

    # Prioritize test cases
    prioritized = prioritizer.prioritize(X, test_case_ids)
    table.field_names = ["Rank", "TestCase ID", "Predicted Priority"]
    for idx, (tc_id, priority) in enumerate(prioritized, 1):
        table.add_row([idx, tc_id, str(priority)])
    print(table)
    
    # Write prioritized test function names for pytest integration
    # Map test_case_ids to actual test function names in test_sample_cases.py
    func_names_map = extract_function_names_map(TEST_SAMPLE_CASES)
    with open(PRIORITIZED_TESTS_TXT, "w") as f:
        for tc_id, _ in prioritized:
            func_name = func_names_map.get(tc_id, tc_id)
            f.write(f"{func_name}\n")

    # Run pytest and show output in console
    print("\nRunning pytest in prioritized order...\n" + "="*40)
    result = subprocess.run([
        'pytest',
        TESTS_DIR,
        '--maxfail=3',
        '--disable-warnings',
        '-v'
    ], capture_output=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # After pytest run, update CSV with total durations and results
    update_csv_with_total_durations_and_results(TEST_DATA_CSV, os.path.join(PROJECT_ROOT, "test_durations.json"))

    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # feature_names = ["last_result", "duration", "recently_changed"]
    # readable_funny_feature_names = [
    #     "Last Result (Pass/Fail)",
    #     "Test Duration (Seconds)",
    #     "Recently Changed (Yes/No)"
    # ]
    # importances = prioritizer.model.feature_importances_
    # ax1.barh(readable_funny_feature_names, importances, color='skyblue')
    # ax1.set_xlabel('Feature Importance')
    # ax1.set_title('Which Features Make a Test Case Important?')

    # tc_ids_sorted = [tc_id for tc_id, _ in prioritized]
    # priorities_sorted = [priority for _, priority in prioritized]
    # bars = ax2.bar(tc_ids_sorted, priorities_sorted, color='orange')
    # ax2.set_xlabel('Test Case ID')
    # ax2.set_ylabel('Predicted Priority (1 = Highest)')
    # ax2.set_title('Test Case Priority Order (Who Runs First?)')
    # ax2.invert_yaxis()  

    # plt.tight_layout()
    # plt.show(block=False)  
    # plt.pause(5)         
    # plt.close()

if __name__ == "__main__":
    main()