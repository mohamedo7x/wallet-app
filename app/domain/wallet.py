"""Small in-memory wallet service."""


from decimal import Decimal
from typing import Any
from uuid import uuid4
from app.Payment.validtaor import validate_payment
from app.domain.transaction_status import TransactionStatus
from app.schemas.payment_schema import SendMoney
from app.fake_bank import FakeBank
from app.infrastructure.xml.builder import build_payment_request_xml
from app.domain.transactions import TransactionService






class WalletService:
    """Holds wallet balances and transactions while the app is running."""

    def __init__(self, bank: FakeBank) -> None:
        self.bank = bank
        self.accounts: dict[str, dict[str, str | Decimal]] = {
            "alice": {
                "client_id": "client-001",
                "balance": Decimal("1000.00"),
            },
            "bob": {
                "client_id": "client-002",
                "balance": Decimal("250.00"),
            },
            "charlie": {
                "client_id": "client-003",
                "balance": Decimal("750.00"),
            },
            "david": {
                "client_id": "client-004",
                "balance": Decimal("1500.00"),
            },
            "emma": {
                "client_id": "client-005",
                "balance": Decimal("500.00"),
            },
        }
        self._transaction = TransactionService()



    def get_transactions(self) -> list[dict[str, Any]]:
        return self._transaction.get_all()
    
    def balance_of(self, name: str) -> Decimal:
        """Return a balance, creating a new empty wallet if needed."""
        account = self.accounts.setdefault( 
        name.lower(),
        {
            "client_id": f"client-{len(self.accounts) + 1:03d}",
            "balance": Decimal("0.00"),
        },
        )
        return account["balance"]
    
    def send(self,payment: SendMoney) -> str:
        """Move money between two local wallets after bank approval."""
        sender,recipient = validate_payment(self, payment.sender , payment.recipient, payment.amount)

        reference = str(uuid4())
        
        xml_request = build_payment_request_xml(
            reference=reference,
            amount=payment.amount,
            sender_account_number=str(self.accounts[sender]["client_id"]),
            receiver_bank_code=self.bank._code,
            receiver_account_number=str(self.accounts[recipient]["client_id"]),
            beneficiary_name=recipient,
            notes=payment.notes
        )

        # Bank approval must happen before changing local balances.
        self.bank.approve_transfer(xml_request)

        self.accounts[sender]["balance"] -= payment.amount
        self.accounts[recipient]["balance"] = self.balance_of(recipient) + payment.amount


        self._transaction.create(
            sender=payment.sender,
            recipient=payment.recipient,
            amount=f"{payment.amount:.2f}",
            reference=reference,
        ) 

        return xml_request

    def receive(self, recipient: str, amount: Decimal) -> dict[str, str]:
        """Simulate an incoming payment approved by the fake bank."""
        recipient = recipient.lower()
        reference = self.bank.approve_transfer()
        self.balances[recipient] = self.balance_of(recipient) + amount

        transaction = {
            "type": "receive",
            "recipient": recipient,
            "amount": f"{amount:.2f}",
            "reference": reference,
        }
        self.transactions.append(transaction)
        return transaction
