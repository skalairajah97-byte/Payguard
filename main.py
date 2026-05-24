from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pydantic import Field 
import uuid
from fastapi import Header
from jose import jwt

app = FastAPI()
idempotency_store = {}
fake_users = {"merchant1": "password123"}
SECRET_KEY = "payguard-secret"

class ChargeRequest(BaseModel):
    # your fields go here
    amount: float = Field(gt=0.01)
    currency: str
    payment_method: str
    description: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/charges", status_code=201)
def charges(charge: ChargeRequest, idempotency_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
   if authorization == None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
   parts = authorization.split(" ")
   login_token = parts[1]
   try: 
       jwt.decode(login_token, SECRET_KEY, algorithms=["HS256"])
   except:
        raise HTTPException(status_code=401, detail="Invalid credentials")
   id = uuid.uuid4()
   if idempotency_key in idempotency_store:
         return idempotency_store[idempotency_key]
   else:
        outcome = {"charge_id": str(id)}
        idempotency_store[idempotency_key] = outcome
        return outcome
    

@app.post("/auth/token", status_code = 200)
def login_token(info: LoginRequest):
    if info.username in fake_users and info.password == fake_users[info.username]: 
        login_token = jwt.encode({"sub": info.username}, SECRET_KEY, algorithm="HS256")
        return{"Token": login_token}
    else: 
        raise HTTPException(status_code=401, detail="Invalid credentials")
    