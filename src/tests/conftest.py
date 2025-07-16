import pytest
import os
import time
import json

durations = {}
results = {}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    start = time.perf_counter()
    outcome = yield
    end = time.perf_counter()
    durations[item.name] = round(end - start, 4)
    # Determine pass/fail from outcome
    rep = outcome.get_result()
    # If the test failed, rep.failed is True
    results[item.name] = 1 if getattr(rep, 'failed', False) else 0


def pytest_sessionfinish(session, exitstatus):
    # Save durations and results to a single JSON file at the end of the test session
    out_path = os.path.join(os.path.dirname(__file__), "..", "..", "test_durations.json")
    # Load previous data if exists
    data = {}
    if os.path.exists(out_path):
        with open(out_path, "r") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
    # Update with new durations and results
    for k in durations:
        # Store as [duration, result] for easier CSV update
        data[k] = [durations[k], results.get(k, None)]
    # Also keep any other keys (e.g., parameterized tests) from previous runs
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

def pytest_collection_modifyitems(session, config, items):
    prioritized_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "prioritized_tests.txt")
    )
    if not os.path.exists(prioritized_file):
        return  # No prioritization file, run as normal

    with open(prioritized_file) as f:
        priority_order = [line.strip() for line in f if line.strip()]

    # Map test function names to their order in the prioritized list
    order_map = {name: idx for idx, name in enumerate(priority_order)}

    def sort_key(item):
        # For parameterized tests, item.name includes the parameter (e.g., test_positive_number[5-True])
        # We want to match the base function name only
        base_name = item.originalname if hasattr(item, 'originalname') else item.name.split('[')[0]
        return order_map.get(base_name, len(order_map))

    items.sort(key=sort_key)
