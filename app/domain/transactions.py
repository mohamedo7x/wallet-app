from collections import deque
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
import time
from app.domain.transaction_status import TransactionStatus
from app.schemas.payment_schema import WebhookBody
from app.parsers.base import parse_payment_string




class TransactionService:
    def __init__(self ) -> None:
        self._transactions: list[dict[str, str]] = []
        self.incoming_payment_events = deque()

    def create(
        self,
        sender: str,
        recipient: str,
        amount: str,
        reference: str,
    ) -> dict:
        transaction = {
            "id": str(uuid4()),
            "status": TransactionStatus.PENDING,
            "type": "send",
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "reference": reference,
            "time": datetime.now(
                timezone.utc
            ).astimezone().strftime("%Y-%m-%d %H:%M:%S%z"),
        }

        self._transactions.append(transaction)

        return transaction
    def get_all(self) -> list[dict[str, Any]]:
        return [
            {
                **transaction,
                "status": transaction["status"].label,
            }
            for transaction in self._transactions
        ]
        
    
    def handel_incoming_payment(self,payment:WebhookBody):
        self.incoming_payment_events.append(payment)



        # time.sleep(3)
        data:dict[str, str] = parse_payment_string(payment.request)
        payment_data = data["payment_data"]
        amount = payment_data[8:].replace(",", ".")
        refrence = str(uuid4())
        transaction = self.create(
        reference=refrence,
        sender=data["sender_account"],
        recipient=data["receiver_account"],
        amount=amount,
        )
            
        print(transaction)

