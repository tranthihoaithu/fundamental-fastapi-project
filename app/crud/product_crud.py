from sqlalchemy.orm import Session
from ..schemas import product_schemas
from .. import models


# create product
def create_product(db: Session, product: product_schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, description=product.description,
                                stock_quantity=product.stock_quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# update
def update_product(db: Session, product_id: int, product_data: product_schemas.ProductUpdate):
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


# read list product
def get_list_products(db: Session):
    return db.query(models.Product).all()


# Delete
def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
