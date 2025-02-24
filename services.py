from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from models import User, Post
from schema import UserCreate, PostCreate
import hashlib, secrets

from schema import UserLogin

import jwt
from fastapi import HTTPException

# Secret key for encoding and decoding the token
SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
ALGORITHM = "HS256"  # Algorithm used for encoding


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(16)

    @staticmethod
    def validate_token(token: str):
        try:
            # Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")  # Get the user ID from the payload
            if user_id is None:
                raise HTTPException(status_code=403, detail="Invalid token")
            return user_id  # Return the user ID
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token")

    @staticmethod
    def create_access_token(user_id: int):
        # Create the token with an expiration time
        expiration = datetime.utcnow() + timedelta(minutes=30)  # Token valid for 30 minutes
        payload = {"user_id": user_id, "exp": expiration}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def signup(self, user_data: UserCreate):
        hashed_password = AuthService.hash_password(user_data.password)
        user = User(name=user_data.name, email=user_data.email, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {"token": AuthService.create_access_token(user_id=user.id)}

    def login(self, user_data: UserLogin):
        user = self.db.query(User).filter(User.email == user_data.email).first()
        if not user or user.password != AuthService.hash_password(user_data.password):
            raise ValueError("Invalid email or password")
        return {"token": AuthService.create_access_token(user_id=user.id)}


class PostService:
    def __init__(self, db: Session):
        self.db = db

    def add_post(self, user_id: int, post_data: PostCreate):
        post = Post(user_id=user_id, text=post_data.text)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return {"postID": post.id}

    def get_posts(self, user_id: int):
        return self.db.query(Post).filter(Post.user_id == user_id).all()

    def delete_post(self, user_id: int, post_id: int):
        post = self.db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if post:
            self.db.delete(post)
            self.db.commit()
            return {"message": "Post deleted"}
        else:
            raise ValueError("Post not found")