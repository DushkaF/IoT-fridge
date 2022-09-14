import json
import re

from get_HS import Lib
from nalog_python import NalogRuPython

# decoder_QR = NalogRuPython()        # Need authorisation with phone

decoder_HS = Lib()

def HSdecoder(code_pack):
    data_to_save = {}
    code_type = code_pack['format']
    code_data = code_pack['text']
    if code_type == 7:
        decoded_json = decoder_HS.infoFromEAN13(code_data)
        data_to_save= parser_good_code(decoded_json)
        # print(json.dumps(data_to_save, indent=4, ensure_ascii=False))
    elif code_type == 5:
        decoded_json = decoder_HS.infoFromDataMatrix(code_data)
        data_to_save = parser_good_code(decoded_json)
        # print(json.dumps(data_to_save, indent=4, ensure_ascii=False))
    elif code_type == 11:
        # ticket = decoder_QR.get_ticket(code_data)
        # print(json.dumps(ticket, indent=4, ensure_ascii=False))
        pass
    else:
        return {"status":404}
    return data_to_save

def parser_good_code(content):
    if not content["codeFounded"]:
        return {"status":404}
    print(json.dumps(content, indent=4, ensure_ascii=False))
    quantity = None
    quantity_unit = None
    expiration_days = None
    expiration_date = None
    expiration_in_ms = None
    expiration_warning = False
    if "milkData" in content:
        if "expireDate" in content["milkData"]:
            expiration_date = int(content["milkData"]["expireDate"])
    elif "expiration" in content:
        expiration_in_ms = int(content["expiration"])
    else:
        expiration_warning = True

    for attr in content["catalogData"][0]["good_attrs"]:
        if attr["attr_id"] in [15448, 66]:
            quantity = float(attr["attr_value"])
            quantity_unit = attr["attr_value_type"]
        if attr["attr_id"] in [21500, 71]:
            if attr["attr_id"] == 21500:
                expiration_days = attr["attr_name"]
            elif attr["attr_id"] == 71:
                expiration_days = attr["attr_value"] + " " + attr["attr_value_type"]
            if expiration_in_ms is None:
                expiration_days_splitted = expiration_days[re.search(r"\d", expiration_days).start():].split()
                if expiration_days_splitted[1].find("сут") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 3600*24*1000
                elif expiration_days_splitted[1].find("час") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 3600*1000
                elif expiration_days_splitted[1].find("месяц") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 3600*1000*24*30
                elif expiration_days_splitted[1].find("год") != -1 or expiration_days_splitted[1].find("лет") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 3600*1000*24*30*12
    if expiration_in_ms is not None and expiration_date is None:
        expiration_date = int(content["checkDate"]) + expiration_in_ms

    good_img = None
    if len(content["catalogData"][0]["good_images"]) != 0:
        good_img = content["catalogData"][0]["good_images"][0]["photo_url"]

    data_to_save = {
        "status":200,
        "product_name": content["productName"],
        "good_img": good_img,
        "good_quantity": quantity,
        "good_unit": quantity_unit,
        "expiration_days": expiration_days,
        "expiration_date": expiration_date,
        "expiration_warning": expiration_warning,
        "check_date": content["checkDate"],
    }
    return data_to_save