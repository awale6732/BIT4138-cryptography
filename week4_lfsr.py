# Week 4: Stream Cipher Cryptanalysis
# LFSR Implementation and Analysis

# ============ LFSR GENERATOR ============
def lfsr(seed, taps, length):
    state = list(seed)
    sequence = []
    for _ in range(length):
        sequence.append(state[0])
        feedback = 0
        for tap in taps:
            feedback ^= state[tap]
        state = state[1:] + [feedback]
    return sequence

# ============ DETECT PERIOD ============
def detect_period(sequence):
    for period in range(1, len(sequence)//2):
        if sequence[:period] == sequence[period:2*period]:
            return period
    return len(sequence)

# ============ WEAKNESS ANALYSIS ============
def analyze_weakness(sequence):
    ones = sum(sequence)
    zeros = len(sequence) - ones
    print(f"Sequence length: {len(sequence)}")
    print(f"Ones: {ones}, Zeros: {zeros}")
    if abs(ones - zeros) < 5:
        print("Balance: GOOD")
    else:
        print("Balance: WEAK")

# ============ TESTING ============
print("===== LFSR SEQUENCE GENERATOR =====")
seed = [1, 0, 1, 1]
taps = [0, 3]
sequence = lfsr(seed, taps, 30)
print(f"Seed: {seed}")
print(f"Taps: {taps}")
print(f"Generated sequence: {sequence}")

print("\n===== PERIOD DETECTION =====")
period = detect_period(sequence)
print(f"Detected period: {period}")

print("\n===== WEAKNESS ANALYSIS =====")
analyze_weakness(sequence)

print("\n===== ATTACK SIMULATION =====")
print("Simulating known plaintext attack...")
known_plain = [1, 0, 1, 0, 1, 0]
known_cipher = [s ^ p for s, p in zip(sequence, known_plain)]
print(f"Known plaintext:  {known_plain}")
print(f"Known ciphertext: {known_cipher}")
recovered = [c ^ p for c, p in zip(known_cipher, known_plain)]
print(f"Recovered stream: {recovered}")
print("Attack successful - keystream recovered!")