# Week 2: Stream Ciphers and Pseudorandomness
# LCG, XOR Stream Cipher and OTP Implementation

import random

# ============ LINEAR CONGRUENTIAL GENERATOR ============
def lcg_generator(seed, a=1664525, c=1013904223, m=2**32, count=20):
    values = []
    x = seed
    for _ in range(count):
        x = (a * x + c) % m
        values.append(x)
    return values

# ============ XOR STREAM CIPHER ============
def xor_encrypt(plaintext, key):
    encrypted = []
    for i in range(len(plaintext)):
        encrypted.append(ord(plaintext[i]) ^ ord(key[i % len(key)]))
    return encrypted

def xor_decrypt(encrypted, key):
    decrypted = ""
    for i in range(len(encrypted)):
        decrypted += chr(encrypted[i] ^ ord(key[i % len(key)]))
    return decrypted

# ============ OTP SIMULATION ============
def otp_encrypt(plaintext):
    key = [random.randint(0, 255) for _ in range(len(plaintext))]
    encrypted = [ord(plaintext[i]) ^ key[i] for i in range(len(plaintext))]
    return encrypted, key

def otp_decrypt(encrypted, key):
    return "".join(chr(encrypted[i] ^ key[i]) for i in range(len(encrypted)))

# ============ TESTING ============
print("===== LCG PSEUDORANDOM GENERATOR =====")
seed = 42
values = lcg_generator(seed)
print(f"Seed: {seed}")
print(f"Generated values: {values[:10]}")

print("\n===== XOR STREAM CIPHER =====")
message = "HELLO CRYPTO"
key = "KEY"
encrypted = xor_encrypt(message, key)
decrypted = xor_decrypt(encrypted, key)
print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")

print("\n===== ONE TIME PAD SIMULATION =====")
message2 = "SECURE"
encrypted2, key2 = otp_encrypt(message2)
decrypted2 = otp_decrypt(encrypted2, key2)
print(f"Original:  {message2}")
print(f"OTP Key:   {key2}")
print(f"Encrypted: {encrypted2}")
print(f"Decrypted: {decrypted2}")