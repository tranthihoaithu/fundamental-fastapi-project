from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    pending = "ĐANG CHỜ XỬ LÝ"
    processing = "ĐANG XỬ LÝ"
    completed = "ĐÃ HOÀN THÀNH"
    cancelled = "ĐÃ HỦY"


class PaymentMethod(str, Enum):
    cash_on_delivery = "Thanh toán khi nhận hàng"
    credit_card = "Thẻ tín dụng"
    momo = "Ví điện tử MoMo"
    Bank_transfer = "Chuyển khoản ngân hàng"


class PaymentBase(BaseModel):
    user_ID: int
    order_id: int
    amount: float
    status: Status = Status.pending
    payment_method: PaymentMethod


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True