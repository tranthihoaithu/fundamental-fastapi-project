

from pydantic import BaseModel
from typing import List


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderBase(BaseModel):
    user_id: int
    order_items: List[OrderItemCreate]


class OrderCreate(OrderBase):
    pass


class OrderItem(OrderItemBase):
    order_item_id: int

    class Config:
        orm_mode = True


class Order(OrderBase):
    id: int
    order_items: List[OrderItem] = []
    subtotal: float
    status: str
    # order_date: datetime

    class Config:
        orm_mode = True



