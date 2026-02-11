from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
import sqlite3

# Init Database
def get_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor

conn, cursor = get_db()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    profession TEXT
)
""")
conn.commit()
conn.close()

class UserCreate(BaseModel):
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


app = FastAPI()

# home
@app.get("/home")
def home():
    return "Hello"

# Create User
@app.post("/users")
def create_user(user: UserCreate):
    
    conn, cursor = get_db()
    cursor.execute("""
        INSERT INTO users
        (name, age, profession)
        VALUES (?, ?, ?)
    """, (
        user.name,
        user.age,
        user.profession
    ))

    conn.commit()
    conn.close()
    return "Created User Successfully"

# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn, cursor = get_db()
    cursor.execute(
        f"DELETE FROM users WHERE id = ?",
        (user_id,),
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
  
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


# Update user
@app.patch("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    conn, cursor = get_db()
    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    cursor.execute("""
        UPDATE users
        SET name = ?, age = ?, profession = ?
        WHERE id = ?
    """, (
        user.name,
        user.age,
        user.profession,
        user_id
    ))

    conn.commit()
    conn.close()

    return {"message": "user updated successfully"}



# Get user by id
@app.get("/users/{user_id}")
def user_info(user_id: int, fields: Optional[str] = Query(None, description="Comma-separated fields, e.g. name,age")):
    
    allowed_fields = ["id", "name", "age", "profession"]

    if fields:
        selected_fields = [f.strip() for f in fields.split(",")]
        for f in selected_fields:
            if f not in allowed_fields:
                raise HTTPException(status_code=400, detail=f"Invalid field: {f}")
    else:
        selected_fields = allowed_fields

    columns = ", ".join(selected_fields)

    conn, cursor = get_db()
    cursor.execute(
        f"SELECT {columns} FROM users WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
  
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return dict(zip(selected_fields, row))

# List all users
@app.get("/users")
def list_users(fields: Optional[str] = Query(None, description="Comma-separated fields, e.g. name,age")):
    
    allowed_fields = ["id", "name", "age", "profession"]

    if fields:
        selected_fields = [f.strip() for f in fields.split(",")]
        for f in selected_fields:
            if f not in allowed_fields:
                raise HTTPException(status_code=400, detail=f"Invalid field: {f}")
    else:
        selected_fields = allowed_fields

    columns = ", ".join(selected_fields)

    conn, cursor = get_db()
    cursor.execute(
        f"SELECT {columns} FROM users"
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(zip(selected_fields, row)) for row in rows]