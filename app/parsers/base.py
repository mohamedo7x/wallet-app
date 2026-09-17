

# from abc import ABC, abstractmethod


# class TransactionParser(ABC):

#     @abstractmethod
#     def parse(self, data: str) -> dict[str, str]:
#         pass



    


def parse_payment_string(payment_string: str) -> dict[str, str]:
    client_id, payment_data, reference, metadata = (
        payment_string.split("|")[0],
        payment_string.split("|")[1].split("#")[0],
        payment_string.split("#")[1],
        payment_string.split("#", 2)[2],
    )

    metadata_parts = metadata.split("/")

    metadata_dict = {
        metadata_parts[i]: metadata_parts[i + 1]
        for i in range(0, len(metadata_parts), 2)
    }

    return {
        "client_id": client_id,
        "payment_data": payment_data,
        "reference": reference,
        **metadata_dict,
    }