import unittest
import os
from src.data.dataset_loader import DatasetLoader
from src.ai.prioritizer import TestCasePrioritizer

class TestTestCasePrioritizer(unittest.TestCase):
    def setUp(self):
        data_path = os.path.join(os.path.dirname(__file__), '../test_data.csv')
        loader = DatasetLoader(data_path)
        X, y = loader.get_features_and_labels()
        self.test_case_ids = loader.get_test_cases()
        self.prioritizer = TestCasePrioritizer()
        self.prioritizer.train(X, y)
        self.X = X

    def test_prioritize(self):
        prioritized = self.prioritizer.prioritize(self.X, self.test_case_ids)
        self.assertEqual(len(prioritized), len(self.test_case_ids))
        priorities = [p[1] for p in prioritized]
        self.assertEqual(priorities, sorted(priorities))

if __name__ == '__main__':
    unittest.main()