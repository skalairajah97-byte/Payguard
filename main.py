from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pydantic import Field 
import uuid
from fastapi import Header

app = FastAPI()
idempotency_store = {}


class ChargeRequest(BaseModel):
    # your fields go here
    amount: float = Field(gt=0.01)
    currency: str
    payment_method: str
    description: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/charges", status_code=201)
def charges(charge: ChargeRequest, idempotency_key: Optional[str] = Header(None)):
    id = uuid.uuid4()
    if idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key]
    else:
        outcome = {"charge_id": str(id)}
        idempotency_store[idempotency_key] = outcome
        return outcome