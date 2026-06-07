# Week 1: Classical Cryptography
# Caesar Cipher and Vigenere Cipher Implementation

# ============ CAESAR CIPHER ============
def caesar_encrypt(text, shift):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, 26 - shift)

# ============ VIGENERE CIPHER ============
def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(char) - 65 + shift) % 26 + 65)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            result += chr((ord(char) - 65 - shift) % 26 + 65)
            key_index += 1
        else:
            result += char
    return result

# ============ TESTING ============
print("===== CAESAR CIPHER =====")
message = "SECURITY"
shift = 4
encrypted = caesar_encrypt(message, shift)
decrypted = caesar_decrypt(encrypted, shift)
print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")

print("\n===== VIGENERE CIPHER =====")
message2 = "NETWORK"
key = "KEY"
encrypted2 = vigenere_encrypt(message2, key)
decrypted2 = vigenere_decrypt(encrypted2, key)
print(f"Original:  {message2}")
print(f"Key:       {key}")
print(f"Encrypted: {encrypted2}")
print(f"Decrypted: {decrypted2}")