import json
from get_HS import Lib
# from main import decoder_QR

decoder_HS = Lib()

def HSdecoder(code_pack):
    data_to_save = {}
    code_type = code_pack['format']
    code_data = code_pack['text']
    if code_type == 7:
        decoded_json = decoder_HS.infoFromEAN13(code_data)
        data_to_save= parser_good_code(decoded_json)
        print(json.dumps(data_to_save, indent=4, ensure_ascii=False))
    elif code_type == 5:
        decoded_json = decoder_HS.infoFromDataMatrix(code_data)
        data_to_save = parser_good_code(decoded_json)
        print(json.dumps(data_to_save, indent=4, ensure_ascii=False))
    elif code_type == 11:
        # ticket = decoder_QR.get_ticket(code_data)
        # print(json.dumps(ticket, indent=4, ensure_ascii=False))
        pass
    return data_to_save

def parser_good_code(content):
    if not content["codeFounded"]:
        return {"status":404}

    quantity = []
    expiration_days = []
    expiration = None
    if "expiration" in content:
        expiration = content["expiration"]
    for attr in content["catalogData"][0]["good_attrs"]:
        if attr["attr_id"] == 15448:
            quantity = attr
        if attr["attr_id"] == 21500:
            expiration_days = attr
    data_to_save = {
        "status":200,
        "productName": content["productName"],
        "good_img": content["catalogData"][0]["good_images"],
        "good_quantity": quantity,
        "expiration_days": expiration_days,
        "checkDate":content["checkDate"],
        "expiration":expiration
    }
    return data_to_save