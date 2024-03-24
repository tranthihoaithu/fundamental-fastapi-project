from sqlalchemy.orm import Session
from ..schemas import payment_schemas
from .. import models


def create_payment(db: Session, payment: payment_schemas.PaymentCreate):
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
