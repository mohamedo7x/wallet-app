from decimal import Decimal

import pytest

from app.fake_bank import FakeBank
from app.domain.wallet import WalletService


def test_send_moves_money_between_wallets() -> None:
    wallets = WalletService(FakeBank())

    transaction = wallets.send("alice", "bob", Decimal("50.00"))

    assert wallets.balance_of("alice") == Decimal("950.00")
    assert wallets.balance_of("bob") == Decimal("300.00")
    assert transaction["type"] == "send"
    assert transaction["reference"].startswith("FAKE-")


def test_send_rejects_insufficient_money() -> None:
    wallets = WalletService(FakeBank())

    with pytest.raises(ValueError, match="Not enough"):
        wallets.send("bob", "alice", Decimal("999.00"))


def test_receive_creates_a_wallet_and_adds_money() -> None:
    wallets = WalletService(FakeBank())

    wallets.receive("charlie", Decimal("10.50"))

    assert wallets.balance_of("charlie") == Decimal("10.50")
