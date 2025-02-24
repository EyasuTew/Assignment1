from sqlalchemy.orm import Session
from models import User, Post
from schema import UserCreate, PostCreate
import hashlib, secrets

from schema import UserLogin


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(16)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def signup(self, user_data: UserCreate):
        hashed_password = AuthService.hash_password(user_data.password)
        user = User(name=user_data.name, email=user_data.email, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {"token": AuthService.generate_token()}

    def login(self, user_data: UserLogin):
        user = self.db.query(User).filter(User.email == user_data.email).first()
        if not user or user.password != AuthService.hash_password(user_data.password):
            raise ValueError("Invalid email or password")
        return {"token": AuthService.generate_token()}


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