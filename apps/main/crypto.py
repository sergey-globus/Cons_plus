from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import os
from django.conf import settings

class GOSTCrypto:
    def __init__(self):
        # Получаем ключ из настроек Django (hex строка)
        key_hex = settings.ENCRYPTION_KEY
        self.key = bytes.fromhex(key_hex)  # Конвертируем hex в байты
        if len(self.key) != 32:
            raise ValueError(f"Encryption key must be 32 bytes long for AES-256. Got {len(self.key)} bytes")

    def encrypt(self, data):
        if not data:
            return data
            
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(data.encode('utf-8'), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(iv + encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_data):
        if not encrypted_data:
            return encrypted_data
            
        encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
        iv = encrypted_data[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
        return decrypted_data.decode('utf-8')