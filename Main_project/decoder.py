import datetime
import json
import re
import copy
from get_HS import Lib
from nalog_python import NalogRuPython

# decoder_QR = NalogRuPython()        # Need authorisation with phone

good_candidate = None

decoder_HS = Lib()


def HSdecoder(code_pack):
    global good_candidate
    data_to_save = {}
    code_type = code_pack['format']
    code_data = code_pack['text']
    if code_type == 7:
        decoded_json = decoder_HS.infoFromEAN13(code_data)
        data_to_save = parser_good_code(decoded_json)
        # print(json.dumps(data_to_save, indent=4, ensure_ascii=False))
    elif code_type == 5:
        decoded_json = decoder_HS.infoFromDataMatrix(code_data)
        data_to_save = parser_good_code(decoded_json)
        # print(json.dumps(decoded_json, indent=4, ensure_ascii=False))
    elif code_type == 11:
        # ticket = decoder_QR.get_ticket(code_data)
        # print(json.dumps(ticket, indent=4, ensure_ascii=False))
        return {"status": 401}
    else:
        return {"status": 405}
    if data_to_save is not None:
        good_candidate = data_to_save
        data_to_send = copy.deepcopy(data_to_save)
        if data_to_send["expiration_date"] is not None:
            dt = datetime.datetime.fromtimestamp(data_to_send["expiration_date"] / 1000.0)
            data_to_send["expiration_date"] = dt.strftime('%d.%m.%Y')
        data_to_send["status"] = 200
        data_to_send.pop("check_date")
        return data_to_send
    else:
        return {"status": 404}


def parser_good_code(content):
    if not content["codeFounded"]:
        return None
    print(json.dumps(content, indent=4, ensure_ascii=False))
    quantity = None
    quantity_unit = None
    expiration_days = None
    expiration_date = None
    expiration_in_ms = None
    expiration_warning = False
    expiration_rough = True
    if "milkData" in content:
        if "expireDate" in content["milkData"]:
            expiration_date = int(content["milkData"]["expireDate"])
    elif "expiration" in content:
        expiration_in_ms = int(content["expiration"])
    else:
        expiration_warning = True

    for attr in content["catalogData"][0]["good_attrs"]:
        if attr["attr_id"] in [15448, 66, 2715]:
            quantity = float(attr["attr_value"])
            quantity_unit = attr["attr_value_type"]

        if attr["attr_id"] in [21500, 71]:
            if attr["attr_id"] == 21500 and expiration_in_ms is None:
                expiration_days = attr["attr_name"]
                expiration_rough = True
            elif attr["attr_id"] == 71:
                expiration_days = attr["attr_value"] + " " + attr["attr_value_type"]
                expiration_rough = False

            if expiration_in_ms is None or not expiration_rough:
                expiration_days_splitted = (expiration_days[re.search(r"\d", expiration_days).start():]).split()
                if expiration_days_splitted[1].find("сут") != -1 or expiration_days_splitted[1].find("дней") != -1 or \
                        expiration_days_splitted[1].find("день") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 1000 * 3600 * 24
                elif expiration_days_splitted[1].find("час") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 1000 * 3600
                elif expiration_days_splitted[1].find("месяц") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 1000 * 3600 * 24 * 30
                elif expiration_days_splitted[1].find("год") != -1 or expiration_days_splitted[1].find("лет") != -1:
                    expiration_in_ms = int(expiration_days_splitted[0]) * 1000 * 3600 * 24 * 30 * 12
    if expiration_in_ms is not None and expiration_date is None:
        expiration_date = int(content["checkDate"]) + expiration_in_ms

    good_img = None
    if len(content["catalogData"][0]["good_images"]) != 0:
        good_img = content["catalogData"][0]["good_images"][0]["photo_url"]

    data_to_save = {
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
