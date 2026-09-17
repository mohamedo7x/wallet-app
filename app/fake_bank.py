"""A pretend bank used only by this local simulation."""

from uuid import uuid4


class FakeBank:
    """Always accepts requests and creates a fake reference number."""


    def __init__(self) -> None:
        self._code = "LRT3030349994"    
    def approve_transfer(self , transfear:str) -> str:
        return f"FAKE-{uuid4().hex[:10].upper()} {transfear} ACCEPTED"
