# Week 5: Block Ciphers and Feistel Structure
# Feistel Cipher Implementation and Avalanche Effect

# ============ SUBSTITUTION BOX ============
SBOX = [0x6,0x4,0xC,0x5,0x0,0x7,0x2,0xE,
        0x1,0xF,0x3,0xD,0x8,0xA,0x9,0xB]

def substitute(value):
    return SBOX[value % 16]

# ============ FEISTEL ROUND FUNCTION ============
def feistel_round(left, right, key):
    new_right = left ^ substitute(right ^ key)
    new_left = right
    return new_left, new_right

# ============ FEISTEL ENCRYPT ============
def feistel_encrypt(plaintext, keys):
    left = (plaintext >> 4) & 0xF
    right = plaintext & 0xF
    print(f"Initial - Left: {left:04b}, Right: {right:04b}")
    for i, key in enumerate(keys):
        left, right = feistel_round(left, right, key)
        print(f"Round {i+1} - Left: {left:04b}, Right: {right:04b}")
    return (left << 4) | right

# ============ FEISTEL DECRYPT ============
def feistel_decrypt(ciphertext, keys):
    left = (ciphertext >> 4) & 0xF
    right = ciphertext & 0xF
    for key in reversed(keys):
        left, right = feistel_round(left, right, key)
    return (left << 4) | right

# ============ AVALANCHE EFFECT ============
def count_diff_bits(a, b):
    diff = a ^ b
    count = 0
    while diff:
        count += diff & 1
        diff >>= 1
    return count

# ============ TESTING ============
print("===== FEISTEL CIPHER IMPLEMENTATION =====")
keys = [0x3, 0xA, 0x7, 0x5]
plaintext = 0xAB
print(f"Plaintext:  {plaintext:08b} ({plaintext})")
print(f"Keys: {[hex(k) for k in keys]}")

print("\n===== ENCRYPTION PROCESS =====")
ciphertext = feistel_encrypt(plaintext, keys)
print(f"Ciphertext: {ciphertext:08b} ({ciphertext})")

print("\n===== DECRYPTION PROCESS =====")
decrypted = feistel_decrypt(ciphertext, keys)
print(f"Decrypted:  {decrypted:08b} ({decrypted})")
print(f"Match: {plaintext == decrypted}")

print("\n===== AVALANCHE EFFECT TEST =====")
plaintext2 = plaintext ^ 0x01
ciphertext2 = feistel_encrypt(plaintext2, keys)
diff_bits = count_diff_bits(ciphertext, ciphertext2)
print(f"Original plaintext:  {plaintext:08b}")
print(f"Modified plaintext:  {plaintext2:08b}")
print(f"Original ciphertext: {ciphertext:08b}")
print(f"Modified ciphertext: {ciphertext2:08b}")
print(f"Bits changed: {diff_bits}")
if diff_bits >= 2:
    print("Avalanche Effect: GOOD")
else:
    print("Avalanche Effect: WEAK")