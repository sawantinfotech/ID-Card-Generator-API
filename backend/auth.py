from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import schemas, models, utils
from backend.database import get_db
import uuid
import hashlib

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.hash_password(user.password)
    api_key = utils.generate_key()
    api_secret = utils.generate_key()

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        api_key=api_key,
        api_secret=api_secret
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "username": db_user.username,
        "email": db_user.email,
        "api_key": db_user.api_key,
        "api_secret": db_user.api_secret
    }
