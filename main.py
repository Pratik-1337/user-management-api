from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    # id: int
    name: str = Field(min_length=2)
    age: int = Field(gt=0)
    profession: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    profession: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    profession: str

users = {}
app = FastAPI()

@app.get("/home")
def home():
    return "Hello"

@app.post("/users")
def create_user(user: UserCreate):
    user_id = len(users) + 1
    users[user_id] = user.model_dump()
    users[user_id]["id"] = user_id
    return users[user_id]

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User ID does not Exist")
    
    del users[user_id]
    return "Deleted User Successfully"

@app.put("/users/{user_id}")
def update_user(user_id: int, user:UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    users[user_id].update(user.model_dump(exclude_unset=True))
    return users[user_id]

@app.get("/users")
def list_users():
    return list(users.values())

@app.get("/users/{user_id}")
def user_info_by_id(user_id: int, fields: Optional[str] = Query(None, description="Comma-separated fields, e.g. name,age")):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User ID does not Exist")
    
    if fields:
        field = [f.strip() for f in fields.split(",")]
        filtered_user = {}
        for k, v in users[user_id].items():
            if k in field:
                filtered_user[k] = v
        return filtered_user
    return users[user_id]