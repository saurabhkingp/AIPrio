from src.data.dataset_loader import DatasetLoader
from src.ai.prioritizer import TestCasePrioritizer
import os
import matplotlib.pyplot as plt
import numpy as np

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
    data_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

    loader = DatasetLoader(data_path)
    X, y = loader.get_features_and_labels()
    test_case_ids = loader.get_test_cases()

    prioritizer = TestCasePrioritizer()
    prioritizer.train(X, y)

    # Prioritize test cases
    prioritized = prioritizer.prioritize(X, test_case_ids)
    print("+------+--------------+--------------------+")
    print(f"| {'Rank':^4} | {'Test-CaseID':<12} | {'Predicted-Priority':^19}|")
    print("+------+--------------+--------------------+")
    for idx, (tc_id, priority) in enumerate(prioritized, 1):
        print(f"| {idx:^4} | {tc_id:<12} | {str(priority):^19}|")
    print("+------+--------------+---------------------+\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    feature_names = ["last_result", "duration", "recently_changed"]
    readable_funny_feature_names = [
        "Last Result (Pass/Fail)",
        "Test Duration (Seconds)",
        "Recently Changed (Yes/No)"
    ]
    importances = prioritizer.model.feature_importances_
    ax1.barh(readable_funny_feature_names, importances, color='skyblue')
    ax1.set_xlabel('Feature Importance')
    ax1.set_title('Which Features Make a Test Case Important?')

    tc_ids_sorted = [tc_id for tc_id, _ in prioritized]
    priorities_sorted = [priority for _, priority in prioritized]
    bars = ax2.bar(tc_ids_sorted, priorities_sorted, color='orange')
    ax2.set_xlabel('Test Case ID')
    ax2.set_ylabel('Predicted Priority (1 = Highest)')
    ax2.set_title('Test Case Priority Order (Who Runs First?)')
    ax2.invert_yaxis()  

    plt.tight_layout()
    plt.show(block=False)  
    plt.pause(5)         
    plt.close()

if __name__ == "__main__":
    main()