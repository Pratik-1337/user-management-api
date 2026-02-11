# User Management FastAPI

A simple user management API built with FastAPI.  
It supports creating, updating, deleting, and listing users using run time memory storage.

---

## Features
- Create a user with ID  
- Update user details  
- Delete a user  
- List all users  
- Get user details by ID  
- Optional field-based filtering  

---

## Tech Stack
- Python  
- FastAPI  
- Pydantic  

---

## How to Run

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Start the server:
```
uvicorn main:app --reload
```

3. Open API docs in browser:
```
http://127.0.0.1:8000/docs
```

## Notes

- Data is stored in a SQL Database