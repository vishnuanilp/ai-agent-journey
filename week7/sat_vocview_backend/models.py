from pydantic import BaseModel

class BusinessRequest(BaseModel):
    customer_id: int
    business_type: str
    message: str
    priority: str