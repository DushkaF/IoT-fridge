def get_catalog():
    data = {"foods":
        [
            {
                "expiration_date": "12.12.2022",
                "expiration_days": "89 сут.",
                "expiration_warning": True,
                "good_img": "https://национальный-каталог.рф/s3/med/972f3851-9a44-d9e5-1fab-1127e22c7352.jpg",
                "good_quantity": 0.38,
                "good_unit": "кг",
                "product_name": "Торт Медовик Черёмушки к/у 0.38кг"
            },
            {
                "expiration_date": "20.09.2022",
                "expiration_days": "Срок хранения до 40 суток (включительно)",
                "expiration_warning": False,
                "good_img": None,
                "good_quantity": 380,
                "good_unit": "г",
                "product_name": "Сметана массовая доля жира 15 %, масса нетто 380 г, товарный знак \"Малочны гасцiнец\""
            },
            {
                "expiration_date": "03.01.2023",
                "expiration_days": "не более 270 суток сут.",
                "expiration_warning": False,
                "good_img": "https://национальный-каталог.рф/s3/med/14047ee4ae2d7905186267768401a9e4.jpg",
                "good_quantity": 1,
                "good_unit": "кг",
                "product_name": "Молоко \"Сударыня\" 2,5% 1кг"
            },
            {
                "expiration_date": None,
                "expiration_days": None,
                "expiration_warning": True,
                "good_img": "https://национальный-каталог.рф/s3/med/775dfdbf-b3c9-e8f6-70ff-f235c3a45f3c.jpg",
                "good_quantity": 0.23,
                "good_unit": "кг",
                "product_name": "Соус Heinz Сырный, 230 г",
                "status": 200
            }
        ],
        "status": 200}

    return data
