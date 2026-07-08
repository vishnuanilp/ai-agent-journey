from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Customer(BaseModel):
    name: str
    phone: Optional[str] = None

class BusinessRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    business_type: str
    customer_id: int = Field(gt=0)
    priority: str
    customer: Optional[Customer] = None

    @field_validator("priority")
    def check_priority(cls, value):
        allowed = ["low", "normal", "high"]
        if value not in allowed:
            raise ValueError("priority must be low, normal, or high")
        return value
    
class BusinessResponse(BaseModel):
    reply: str
    model_used: str
    confidence: float