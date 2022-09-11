# - *- coding: utf- 8 - *-
from app import app
from nalog_python import NalogRuPython

# decoder_QR = NalogRuPython()        # Need authorisation with phone

if __name__ == "__main__":
    app.run(use_reloader=False)