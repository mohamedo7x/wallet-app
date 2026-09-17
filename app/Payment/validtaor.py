




from decimal import Decimal


def validate_payment(self, sender: str, recipient: str, amount: Decimal):
    sender = sender.lower()
    recipient = recipient.lower()

    if sender == recipient:
        raise ValueError("Sender and recipient must be different.")

    if amount <= 0:
        raise ValueError("Amount must be positive.")

    if self.balance_of(sender) < amount:
        raise ValueError("Not enough money in the sender wallet.")

    return sender, recipient