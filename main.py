from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import UserService, PostService, AuthService
from schema import UserCreate, UserLogin, PostCreate

app = FastAPI()



@app.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.signup(user_data)


@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.login(user_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/addpost")
def add_post(post_data: PostCreate, token: str = Depends(AuthService.validate_token), db: Session = Depends(get_db)):
    # Simulating token verification (in production, use a proper method)
    user_id = 1  # Assume token maps to user ID 1
    service = PostService(db)
    return service.add_post(user_id, post_data)


@app.get("/getposts")
def get_posts(token: str = Depends(AuthService.validate_token), db: Session = Depends(get_db)):
    user_id = 1  # Simulating token authentication
    service = PostService(db)
    return service.get_posts(user_id)


@app.delete("/deletepost")
def delete_post(post_id: int, token: str = Depends(AuthService.validate_token), db: Session = Depends(get_db)):
    user_id = 1  # Simulating token authentication
    service = PostService(db)
    try:
        return service.delete_post(user_id, post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
