# Week 3: Period, Linear Complexity and Randomness Testing
# Statistical Randomness Testing Implementation

import random

# ============ LCG GENERATOR ============
def lcg(seed, a=1664525, c=1013904223, m=2**32):
    x = seed
    sequence = []
    for _ in range(100):
        x = (a * x + c) % m
        sequence.append(x % 2)
    return sequence

# ============ FREQUENCY TEST ============
def frequency_test(sequence):
    ones = sum(sequence)
    zeros = len(sequence) - ones
    print(f"Frequency Test:")
    print(f"  Ones:  {ones}")
    print(f"  Zeros: {zeros}")
    if abs(ones - zeros) < 10:
        print("  Result: PASS - Sequence is balanced")
    else:
        print("  Result: FAIL - Sequence is unbalanced")

# ============ RUNS TEST ============
def runs_test(sequence):
    runs = 1
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i-1]:
            runs += 1
    print(f"\nRuns Test:")
    print(f"  Total runs: {runs}")
    if runs > 40:
        print("  Result: PASS - Good randomness detected")
    else:
        print("  Result: FAIL - Poor randomness detected")

# ============ MEAN TEST ============
def mean_test(sequence):
    mean = sum(sequence) / len(sequence)
    print(f"\nMean Test:")
    print(f"  Mean value: {mean:.4f}")
    if 0.4 <= mean <= 0.6:
        print("  Result: PASS - Mean is close to 0.5")
    else:
        print("  Result: FAIL - Mean is far from 0.5")

# ============ PERIOD DETECTION ============
def find_period(sequence):
    for period in range(1, len(sequence)//2):
        if sequence[:period] == sequence[period:2*period]:
            return period
    return len(sequence)

# ============ TESTING ============
print("===== RANDOMNESS TESTING SYSTEM =====")
print("Generating 100 random bits using LCG...\n")

sequence = lcg(42)
print(f"First 20 bits: {sequence[:20]}")

frequency_test(sequence)
runs_test(sequence)
mean_test(sequence)

print("\n===== PERIOD ANALYSIS =====")
small_seq = lcg(42)[:20]
period = find_period(small_seq)
print(f"Sequence: {small_seq}")
print(f"Estimated Period: {period}")

print("\n===== PYTHON RANDOM COMPARISON =====")
random_seq = [random.randint(0,1) for _ in range(100)]
print(f"Python random first 20 bits: {random_seq[:20]}")
frequency_test(random_seq)