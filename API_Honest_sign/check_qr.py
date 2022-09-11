import json

from nalog_python import NalogRuPython

client = NalogRuPython()
qr_code = "t=20220910T2051&s=64.99&fn=9960440302359187&i=15349&fp=2377967000&n=1"
ticket = client.get_ticket(qr_code)
print(json.dumps(ticket, indent=4, ensure_ascii=False))