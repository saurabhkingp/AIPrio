import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
TESTS_DIR = os.path.join(SRC_DIR, 'tests')
UTILS_DIR = os.path.join(SRC_DIR, 'utils')

TEST_DATA_CSV = os.path.join(SRC_DIR, 'test_data.csv')
TEST_SAMPLE_CASES = os.path.join(TESTS_DIR, 'test_sample_cases.py')
PRIORITIZED_TESTS_TXT = os.path.join(PROJECT_ROOT, 'prioritized_tests.txt')

SINCE_COMMIT = 'HEAD~1'
