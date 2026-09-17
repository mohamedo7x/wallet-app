import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.domain.transaction_status import TransactionStatus





class SendMoney(BaseModel):
    sender: str = Field(min_length=1)
    recipient: str = Field(min_length=1)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    notes: list[str] = Field(default_factory=list)


class WebhookBody(BaseModel):
    request: str = Field(min_length=1)
    status: str = TransactionStatus.PENDING
    received_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )