# from .base import TransactionParser


# class BankTransactionParser(TransactionParser):

#     def parse(self, data: str) -> dict[str, str]:
#         amount, reference, date = data.split("//")

#         return {
#             "amount": amount,
#             "reference": reference,
#             "date": date,
#         }