from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.domain.transaction_status import TransactionStatus


class TransactionService:
    def __init__(self) -> None:
        self._transactions: list[dict[str, str]] = []

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