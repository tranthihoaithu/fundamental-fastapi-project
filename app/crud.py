from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password


# Create
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email== email).first()


# create product
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, description=product.description, stock_quantity=product.stock_quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# update
def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product_data.dict().items():
            if value is not None:
                setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


# read product
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


# Delete
def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product