import pytest
import time

# 1. Simple pass test
def test_login_success():
    time.sleep(1) 
    assert "user" == "user"

# 2. Simple fail test
def test_login_failure():
    assert 1 == 2

# 3. API response code check (simulated)
def test_api_status_code():
    start_time = time.time()
    response_code = 200  # Simulated
    elapsed_time = time.time() - start_time
    assert response_code == 200
    print(f"API call took {elapsed_time:.6f} seconds")

# 4. Parameterized test for input validation
@pytest.mark.parametrize("input_val,expected", [
    (5, True),
    (0, False),
    (-1, False)
])
def test_positive_number(input_val, expected):
    assert (input_val > 0) == expected

# 5. Test with fixture (simulated resource setup)
@pytest.fixture
def resource():
    return {"status": "ready"}

#

def test_resource_status(resource):
    assert resource["status"] == "ready"

# 6. Test with simulated execution time
def test_slow_operation():
    time.sleep(2.2)
    assert True

# 7. Test with exception handling
def test_raises_exception():
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0

# 8. Test with list comparison
def test_list_equality():
    assert sorted([3, 1, 2]) == [1, 2, 3]

# 9. Test with dictionary keys
def test_dict_keys():
    d = {"a": 1, "b": 2}
    assert "a" in d and "b" in d

# 10. Test with multiple assertions
def test_multiple_assertions():
    x = 10
    y = 5
    assert x > y
    assert x + y == 15
