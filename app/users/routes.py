from fastapi import APIRouter, HTTPException, Query
from app.users.schemas import UserResponse, UserCreate, UserUpdate
from typing import Optional
from app.database import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])

# home
# @user_router.get("/home")
# def home():
#     return "Hello"

# Create User
@user_router.post("/")
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
@user_router.delete("/{user_id}")
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
@user_router.patch("/{user_id}")
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
@user_router.get("/{user_id}")
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
@user_router.get("/")
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