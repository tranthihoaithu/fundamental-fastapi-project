from sqlalchemy.orm import Session
from . import models, schemas


# Create
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password=user.password, last_name=user.last_name, first_name=user.first_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, price=product.price, stock_quantity=product.stock_quantity, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(user_id=payment.user_id, amount=payment.amount, status=payment.payment_status, payment_method=payment.payment_method)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def crete_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(user_id=order.user_id, product_id=order.product_id, quantity=order.quantity, total_price=order.total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# Read
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter( models.Product.id == product_id).first()


def get_payments(db: Session, payment_id: int):
    return db.query(models.Payment).filter( models.Payment.id== payment_id).first()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

