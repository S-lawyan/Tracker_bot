test_json = {'state': 0, 'payloadVersion': 2, 'data': {'products': [
    {'id': 146734961, 'root': 124298459, 'kindId': 0, 'brand': 'Philips', 'brandId': 6012, 'siteBrandId': 16012,
     'colors': [{'name': 'черный', 'id': 0}], 'subjectId': 710, 'subjectParentId': 657,
     'name': 'Безмешковый пылесос PowerPro Expert FC9732 01', 'supplier': 'Техника для дома Philips',
     'supplierId': 219159, 'supplierRating': 4.8, 'supplierFlags': 0, 'pics': 12, 'rating': 5, 'reviewRating': 4.8,
     'feedbacks': 64, 'panelPromoId': 178695, 'promoTextCard': 'ШОК-ВЫХОДНЫЕ', 'promoTextCat': 'ШОК-ВЫХОДНЫЕ',
     'volume': 693, 'viewFlags': 25, 'promotions': [63484, 81773, 92742, 113253, 162613, 163950, 178695], 'sizes': [
        {'name': '', 'origName': '0', 'rank': 0, 'optionId': 246899407,
         'stocks': [{'wh': 208277, 'dtype': 4, 'qty': 2, 'priority': 43354, 'time1': 3, 'time2': 62},
                    {'wh': 507, 'dtype': 4, 'qty': 312, 'priority': 85911, 'time1': 4, 'time2': 26}], 'time1': 4,
         'time2': 26, 'wh': 507, 'dtype': 4,
         'price': {'basic': 2899000, 'product': 1802000, 'total': 1802000, 'logistics': 0, 'return': 0},
         'saleConditions': 0,
         'payload': 'HDx/gCWBeiEHaVuvJS6FkBV7jZOrz7OCss6TB8W39vRbhZhtV9gNyIygWzDECyiYt2bP46BZw9JWlLcRXw'}], 'time1': 4,
     'time2': 26, 'wh': 507, 'dtype': 4}]}}

product = test_json["data"]["products"][0]

stop = 0

