import pytest
from pydantic import ValidationError
from models import BusinessRequest

def test_rejects_string_customer_id():
    with pytest.raises(ValidationError):
        BusinessRequest(
            customer_id="c123",
            business_type="clinic",
            message="test",
            priority="high",
        )