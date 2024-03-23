from sqlalchemy.orm import Session
from ..schemas import user_schemas
from .. import models
from ..security import hash_password


# Create
def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
