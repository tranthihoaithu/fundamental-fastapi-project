from datetime import datetime
from http.client import HTTPException

from sqlalchemy.orm import Session
from .. import models
from ..schemas import order_schemas


# def create_order(db: Session, order: order_schemas.OrderCreate):
#
#     db_order = models.Order(user_id=order.user_id)
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)
#
#     for item in order.items:
#         db_order_item = models.OrderItem(product_id=item.product_id, quantity=item.quantity)
#         db.add(db_order_item)
#         db.commit()
#         db.refresh(db_order_item)
#
#     return db_order


def create_order(db: Session, order: order_schemas.OrderCreate):
    order_items = order.order_items
    subtotal = 0

    # Tính tổng giá trị đơn hàng
    for item in order_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product is not None:  # Kiểm tra xem sản phẩm có tồn tại hay không
            subtotal += product.price * item.quantity

    # Tạo đơn hàng
    db_order = models.Order(
        user_id=order.user_id,
        subtotal=subtotal,
        order_date=datetime,
        status="Pending",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    db.commit()

    # Tạo các mục đơn hàng và thêm vào cơ sở dữ liệu
    order_items_db = []
    for item in order_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product is not None:  # Kiểm tra xem sản phẩm có tồn tại hay không
            order_item = models.OrderItem(**item.dict(), order_id=db_order.id)
            order_items_db.append(order_item)

    db.add_all(order_items_db)  # Thêm tất cả các mục đơn hàng vào cơ sở dữ liệu
    db.commit()
    return db_order

