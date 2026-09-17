








from decimal import Decimal

from pydantic import BaseModel, Field


class SendMoney(BaseModel):
    sender: str = Field(min_length=1)
    recipient: str = Field(min_length=1)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    notes: list[str] = Field(default_factory=list)