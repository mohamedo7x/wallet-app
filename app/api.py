"""HTTP API for the wallet simulation."""
from typing import Any
from fastapi import FastAPI, HTTPException , Response
from app.schemas.payment_schema import SendMoney, WebhookBody
from app.fake_bank import FakeBank
from app.domain.wallet import WalletService
from app.database.Database import Database
from app.config import get_settings 

app = FastAPI(title="Wallet Simulator",version="1.0.0")
db_path = get_settings().database_path
connection = Database(db_path)
wallets = WalletService(FakeBank())




@app.get("/health")
def health() -> dict: return {"status": "ok"}



@app.get("/balance/{name}")
def get_balance(name: str) -> dict[str, str]:
    return {"name": name.lower(), "balance": f"{wallets.balance_of(name):.2f}"}


@app.post("/send")
def send_money(payment: SendMoney) -> Response:
    try:
        xmlrequest = wallets.send(payment)
        return Response(
            content=xmlrequest,
            media_type="application/xml"
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error



@app.post("/webhook/receive")
def receive_money(payment: WebhookBody) ->  dict[str, str]:
    request = wallets.receive(payment)
    return request

    verify_signature(payment)
    check_idempotency(payment)
    wallets.receive(payment.recipient, payment.amount)



@app.get("/transactions")
def get_transactions() -> list[dict[str, Any]]:
    return wallets.get_transactions()
