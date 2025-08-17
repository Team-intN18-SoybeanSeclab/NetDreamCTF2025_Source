import base64

def encrypt(plaintext, key):
    key_sum = sum(ord(char) for char in key)
    if not plaintext.startswith("flag{"):
        plaintext = "flag{" + plaintext
    if not plaintext.endswith("}"):
        plaintext += "}"
    
    encrypted = []
    for char in plaintext:
        encrypted_char = (ord(char) + key_sum) % 256 
        encrypted.append(encrypted_char)

    encrypted_bytes = bytes(encrypted)
    base64_encoded = base64.b64encode(encrypted_bytes).decode('utf-8')
    shift = key_sum % 26
    caesar_shifted = ""
    for char in base64_encoded:
        if char.isalpha():
            shifted_char = chr(((ord(char) - ord('A') + shift) % 26 + ord('A'))) if char.isupper() else chr(((ord(char) - ord('a')) + shift) % 26 + ord('a'))
            caesar_shifted += shifted_char
        else:
            caesar_shifted += char
    hex_encoded = caesar_shifted.encode('utf-8').hex()
    
    return hex_encoded

key = "xx_xx_xx_xx_xx_xx_xx_xx_xx_xx_xx_xx_xx_xx"

plaintext = "Thi5 1s th3 Fl@g" 

ciphertext = encrypt(plaintext, key)
print(ciphertext)

#686545356839417466377a5266364133695a54556a376857696f6c4e67377a5166364248