import pandas as pd
import os
from src.utils.helpers import generate_sample_test_data


class DatasetLoader:
    """
    Loads and prepares test case data for prioritization.
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        if not os.path.exists(csv_path):
            generate_sample_test_data(csv_path)
        self.data = pd.read_csv(csv_path)

    def get_features_and_labels(self):
        X = self.data[["last_result", "duration", "recently_changed"]]
        y = self.data["priority"]
        return X, y

    def get_test_cases(self):
        return self.data["test_case_id"].tolist()