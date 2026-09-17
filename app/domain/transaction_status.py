# app/domain/transaction.py

from enum import IntEnum


class TransactionStatus(IntEnum):
    PENDING = 1
    RECEIVED = 2
    REJECTED = 3
    FAILED = 4

    @property
    def label(self) -> str:
        return {
            TransactionStatus.PENDING: "Pending",
            TransactionStatus.RECEIVED: "Received",
            TransactionStatus.REJECTED: "Rejected",
            TransactionStatus.FAILED: "Failed",
        }[self]