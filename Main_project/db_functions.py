import datetime

import decoder
import database

def get_catalog():
    data = {}
    try:
        product_cards = database.ProductCard.query.order_by(database.ProductCard.expiration_date).all()
    except:
        print("DB get fail")
        data["status"] = 500
        return data

    for card in product_cards:
        if "food_cards" not in data:
            data["food_cards"] = []

        expiration_date = None
        if card.expiration_date != None:
            dt = datetime.datetime.fromtimestamp(card.expiration_date / 1000.0)
            expiration_date = dt.strftime('%d.%m.%Y')

        data_to_json = {
            "id": card.id,
            "expiration_date": expiration_date,
            "expiration_days": card.expiration_days,
            "expiration_warning": card.expiration_warning,
            "good_img": card.good_img,
            "good_quantity": card.good_quantity,
            "good_unit": card.good_unit,
            "product_name": card.product_name
        }
        data["food_cards"].append(data_to_json)
    data["status"] = 200
    return data



def add_product_card(content):
    status = 200
    if content['status'] == 410:
        print("product was deleted")
    elif content['status'] == 201:
        product = decoder.good_candidate
        product_card = database.ProductCard(
            check_date=product["check_date"],
            expiration_date=product["expiration_date"],
            expiration_days=product["expiration_days"],
            expiration_warning=product["expiration_warning"],
            good_img=product["good_img"],
            good_quantity=product["good_quantity"],
            good_unit=product["good_unit"],
            product_name=product["product_name"]
        )
        try:
            database.db.session.add(product_card)
            database.db.session.commit()
            print("product was accept")
        except Exception as e:
            print(e)
            status = 500
            print("BD fail!")
    decoder.good_candidate = None
    return status