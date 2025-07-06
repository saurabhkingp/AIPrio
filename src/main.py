from src.data.dataset_loader import DatasetLoader
from src.ai.prioritizer import TestCasePrioritizer
import os
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Set up paths
    data_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

    # Load data
    loader = DatasetLoader(data_path)
    X, y = loader.get_features_and_labels()
    test_case_ids = loader.get_test_cases()

    # Train prioritizer
    prioritizer = TestCasePrioritizer()
    prioritizer.train(X, y)

    # Prioritize test cases
    prioritized = prioritizer.prioritize(X, test_case_ids)
    print("Prioritized test cases (from highest to lowest):")
    for tc_id, priority in prioritized:
        print(f"{tc_id}: Priority {priority}")

    # --- Combined Visualization: Feature Importance & Prioritized Test Cases ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Feature Importance
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

    # Prioritized Test Cases
    tc_ids_sorted = [tc_id for tc_id, _ in prioritized]
    priorities_sorted = [priority for _, priority in prioritized]
    bars = ax2.bar(tc_ids_sorted, priorities_sorted, color='orange')
    ax2.set_xlabel('Test Case ID')
    ax2.set_ylabel('Predicted Priority (1 = Highest)')
    ax2.set_title('Test Case Priority Order (Who Runs First?)')
    ax2.invert_yaxis()  # So 1 (high) is at the top

    plt.tight_layout()
    plt.show()  # Show non-blocking
    #plt.pause(5)          # Keep the window open for 5 seconds
    #plt.close()

if __name__ == "__main__":
    main()