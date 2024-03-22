from datetime import timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud, authentication, security

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/login/", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"email": db_user.email, "username": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/products/", response_model=schemas.ProductCreate)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db=db, product=product)
    return db_product


@app.put("/products/{product_id}", response_model=schemas.ProductUpdate)
def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db=db, product_id=product_id, product_data=product_data)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404 , detail="product not found")
    return db_product


@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product