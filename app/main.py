from datetime import timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, authentication, security
from .crud import product_crud, user_crud, order_crud
from .schemas import user_schemas, product_schemas, order_schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=user_schemas.User)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)


@app.post("/login/", response_model=user_schemas.Token)
def login_user(user: user_schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=authentication.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authentication.create_access_token(
        data={"email": db_user.email, "username": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/products/", response_model=product_schemas.ProductCreate)
def create_product(product: product_schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = product_crud.create_product(db=db, product=product)
    return db_product


@app.put("/products/{product_id}", response_model=product_schemas.ProductUpdate)
def update_product(product_id: int, product_data: product_schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = product_crud.update_product(db=db, product_id=product_id, product_data=product_data)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/products/{product_id}", response_model=product_schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return db_product


@app.delete("/products/{product_id}", response_model=product_schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db),):
    db_product = product_crud.delete_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/prodcuts/", response_model=list[product_schemas.Product])
def get_list_products(db: Session = Depends(get_db)):
    products = product_crud.get_list_products(db)
    return products


@app.post("/orders/", response_model=order_schemas.Order)
def create_order(order: order_schemas.OrderCreate, db: Session = Depends(get_db)):
    order_items = order.order_items
    for item in order_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found.")
        elif product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough quantity available for product with id {item.product_id}.")

        product.stock_quantity -= item.quantity

    return order_crud.create_order(db=db, order=order)


# @app.post("/orders/", response_model=order_schemas.Order)
# def place_order(order: order_schemas.OrderCreate, db: Session = Depends(get_db)):
#     total_price = 0
#     for item in order.items:
#         product = product_crud.get_product(db, product_id=item.product_id)
#         if product is None:
#             raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
#         if product.stock_quantity < item.quantity:
#             raise HTTPException(status_code=400, detail=f"Insufficient stock for product with ID {item.product_id}")
#
#         product.stock_quantity -= item.quantity
#         item_price = product.price * item.quantity
#         total_price += item_price
#
#     db_order = order_crud.create_order(db, order)
#     db_order.total_price = total_price
#     return db_order