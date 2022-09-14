import json

from get_HS import Lib

lib = Lib()
# print(lib.infoFromEAN13(4620021193701))
# print(lib.infoFromDataMatrix("0104600742014721215cdiNs\u001d93HKbs"))
# print(lib.infoFromQr("4087570038"))
print(json.dumps(lib.infoFromQr("80177173"), indent=4, ensure_ascii=False))