import os

class GOSTCrypto:
    def __init__(self):
        key_hex = os.getenv('ENCRYPTION_KEY')
        if not key_hex:
            raise ValueError('ENCRYPTION_KEY is not set')
        self.key = bytes.fromhex(key_hex)
        # далее — остальная инициализация
