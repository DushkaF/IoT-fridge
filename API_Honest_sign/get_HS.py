# НЕЧестный Знак
# (C) 2021, li0ard, ЦРПТ

import requests, urllib

class Lib:
	def __init__(self):
		pass

	def _get(self, content, type):
		return requests.get(f"https://mobile.api.crpt.ru/mobile/check?code={content}&codeType={type}").json()

	def infoFromDataMatrix(self, xymatrix):
		return self._get(xymatrix, "datamatrix")

	def infoFromEAN13(self, ean13):
		return self._get(ean13, "ean13")

	# def infoFromEAN8(self, ean8):
	# 	return self._get(ean8, "ean8")

	def infoFromQr(self, qr):
		return self._get(qr, "qr")