from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

class User_Data(BaseModel):
    name: str
    age: int
    profession: str

class Update_User_Data(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    profession: Optional[str] = None

users = {}
app = FastAPI()

@app.get("/home")
def home():
    return "Hello"

@app.post("/create-user/{user_id}")
def create_user(user_id: int, user_data: User_Data):
    if user_id in users:
        raise HTTPException(status_code=404, detail="User ID already Exist")
    
    users[user_id] = user_data
    return "User Created Successfully"

@app.delete("/delete-user")
def delete_user(user_id: int = Query(..., description="ID of the User to Delete")):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User ID does not Exist")
    
    del users[user_id]
    return "Deleted User Successfully"

@app.put("/update-user/{user_id}")
def update_user(user_id: int, user_data: Update_User_Data):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User ID does not Exist")
    
    users[user_id] = user_data
    return "User Updated Successfully"

@app.get("/list-users")
def list_users():
    return list(users.values())

@app.get("/user-info-by-id/{user_id}")
def user_info_by_id(user_id: int, fields: Optional[str] = Query(None, description="Comma-separated fields, e.g. name,age")):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User ID does not Exist")
    
    if fields:
        field = fields.split(",")
        filtered_user = {}
        for k, v in users[user_id].dict().items():
            if k in field:
                filtered_user[k] = v
        return filtered_user
    return users[user_id]