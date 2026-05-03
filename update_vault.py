import sys
import base64
from datetime import datetime
import os

if len(sys.argv) < 2:
    print("Usage: python update_vault.py \"Your text to encode\"")
    sys.exit(1)

text_to_encode = sys.argv[1]
encoded_bytes = base64.b64encode(text_to_encode.encode('utf-8'))
encoded_string = encoded_bytes.decode('utf-8')

if not os.path.exists('data_vault.txt'):
    open('data_vault.txt', 'a').close()

with open('data_vault.txt', 'w') as f:
    f.write(encoded_string)
print(f"data_vault.txt updated with Base64 encoded data.")
