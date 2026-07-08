
import pytest
from models import BusinessRequest

def test_good_request_is_accepted():
    req = BusinessRequest(
        message="I need a booking",
        business_type="clinic",
        customer_id=1,
        priority="high",
    )
    assert req.priority == "high"
    assert req.customer_id == 1


def test_bad_priority_is_rejected():
    with pytest.raises(ValueError):
        BusinessRequest(
            message="hello",
            business_type="clinic",
            customer_id=1,
            priority="banana",
        )

@pytest.mark.parametrize("value", ["low", "normal", "high"])
def test_valid_priorities_accepted(value):
    req = BusinessRequest(
        message="hello",
        business_type="clinic",
        customer_id=1,
        priority=value,
    )
    assert req.priority == value

@pytest.mark.parametrize("bad_value", ["banana", "urgent", "", "HIGH"])
def test_invalid_priorities_rejected(bad_value):
    with pytest.raises(ValueError):
        BusinessRequest(
            message="hello",
            business_type="clinic",
            customer_id=1,
            priority=bad_value,
        )

@pytest.fixture
def valid_data():
    return {
        "message": "I need a booking",
        "business_type": "clinic",
        "customer_id": 1,
        "priority": "high",
    }

def test_good_request_with_fixture(valid_data):
    req = BusinessRequest(**valid_data)
    assert req.priority == "high"