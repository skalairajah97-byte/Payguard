from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pydantic import Field 
import uuid


app = FastAPI()

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
def charges(charge: ChargeRequest):
    id = uuid.uuid4()
    return {"charge_id": id}



