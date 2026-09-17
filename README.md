# Wallet Simulator

A tiny API for simulating sending and receiving money. It uses in-memory data and a fake bank—nothing leaves your machine.

## Run it

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API.

## Endpoints

- `GET /balance/{name}` — see a wallet balance.
- `POST /send` — send money from one wallet to another through the fake bank.
- `POST /receive` — simulate receiving money from outside the wallet.
- `GET /transactions` — see simulated transfers.

The app begins with `alice: 1000.00` and `bob: 250.00`.
