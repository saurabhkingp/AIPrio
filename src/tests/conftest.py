import pytest
import os

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
