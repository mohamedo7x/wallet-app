from datetime import datetime, timezone
from decimal import Decimal
from xml.etree.ElementTree import Element, SubElement, tostring


def build_payment_request_xml(
    reference: str,
    amount: Decimal,
    sender_account_number: str,
    receiver_bank_code: str,
    receiver_account_number: str,
    beneficiary_name: str,
    notes: list[str] | None = None,
    payment_type: int = 99,
    charge_details: str = "SHA",
) -> str:
    root = Element("PaymentRequestMessage")

    transfer_info = SubElement(root, "TransferInfo")
    SubElement(transfer_info, "Reference").text = reference
    SubElement(transfer_info, "Date").text = datetime.now(
        timezone.utc
    ).astimezone().strftime("%Y-%m-%d %H:%M:%S%z")
    SubElement(transfer_info, "Amount").text = format(amount, ".2f")
    SubElement(transfer_info, "Currency").text = "SAR"

    sender_info = SubElement(root, "SenderInfo")
    SubElement(sender_info, "AccountNumber").text = sender_account_number

    receiver_info = SubElement(root, "ReceiverInfo")
    SubElement(receiver_info, "BankCode").text = receiver_bank_code
    SubElement(receiver_info, "AccountNumber").text = receiver_account_number
    SubElement(receiver_info, "BeneficiaryName").text = beneficiary_name
    
    if notes:
        notes_element = SubElement(root, "Notes")
        for note in notes:
            SubElement(notes_element, "Note").text = note

    if payment_type != 99:
        SubElement(root, "PaymentType").text = str(payment_type)

    if charge_details != "SHA":
        SubElement(root, "ChargeDetails").text = charge_details

    return tostring(root, encoding="unicode")