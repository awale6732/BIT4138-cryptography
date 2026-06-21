import hashlib
import hmac
import os
import sqlite3
import secrets
import string
import time
from datetime import datetime

def sha256_demo():
    print("\n" + "="*55)
    print("  Fig 1: SHA-256 Hash Generation")
    print("="*55)
    messages = [
        "Hello, Cryptography!",
        "BIT4138 Advanced Cryptography",
        "password123",
        "SecureP@ssw0rd!2024",
    ]
    print(f"\n{'Message':<30} {'SHA-256 Hash'}")
    print("-" * 97)
    for msg in messages:
        h = hashlib.sha256(msg.encode()).hexdigest()
        print(f"{msg:<30} {h}")
    print("\n[Avalanche Effect Demonstration]")
    msg1 = "password"
    msg2 = "Password"
    h1 = hashlib.sha256(msg1.encode()).hexdigest()
    h2 = hashlib.sha256(msg2.encode()).hexdigest()
    diff = sum(c1 != c2 for c1, c2 in zip(h1, h2))
    print(f"  '{msg1}' -> {h1}")
    print(f"  '{msg2}' -> {h2}")
    print(f"  Characters different: {diff}/64  ({diff/64*100:.1f}% change)")

def hash_password(password):
    salt = secrets.token_hex(16)
    salted = (salt + password).encode()
    hashed = hashlib.sha256(salted).hexdigest()
    return salt, hashed

def password_hashing_demo():
    print("\n" + "="*55)
    print("  Fig 2: Password Hashing System")
    print("="*55)
    passwords = ["admin123", "SecurePass!", "qwerty", "Tr0ub4dor&3"]
    print(f"\n{'Password':<16} {'Salt':<34} {'Hashed Password'}")
    print("-" * 115)
    for pwd in passwords:
        salt, hashed = hash_password(pwd)
        print(f"{pwd:<16} {salt:<34} {hashed}")
    print("\n[Same password hashed twice - different output due to salt]")
    s1, h1 = hash_password("admin123")
    s2, h2 = hash_password("admin123")
    print(f"  Hash 1: {h1}")
    print(f"  Hash 2: {h2}")
    print(f"  Identical: {h1 == h2}  <- Salting prevents rainbow table attacks")

def init_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    return conn

def register_user(conn, username, password):
    salt, hashed = hash_password(password)
    conn.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                 (username, salt, hashed, datetime.now().isoformat()))
    conn.commit()

def authenticate_user(conn, username, password):
    row = conn.execute(
        "SELECT salt, password_hash FROM users WHERE username=?", (username,)
    ).fetchone()
    if not row:
        return False
    salt, stored_hash = row
    attempt_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return hmac.compare_digest(attempt_hash, stored_hash)

def login_auth_demo():
    print("\n" + "="*55)
    print("  Fig 3: Login Authentication Workflow")
    print("="*55)
    conn = init_db()
    users = [
        ("alice",   "Alicep@ss99"),
        ("bob",     "B0bSecure!"),
        ("charlie", "Ch@rlie2024"),
    ]
    print("\n[Step 1 - Registering Users]")
    for uname, pwd in users:
        register_user(conn, uname, pwd)
        print(f"  + '{uname}' registered  (plaintext password NEVER stored)")
    print("\n[Step 2 - Database Contents (no plaintext)]")
    print(f"  {'Username':<10} {'Salt':<34} {'Stored Hash'}")
    print("  " + "-" * 100)
    for row in conn.execute("SELECT username, salt, password_hash FROM users"):
        print(f"  {row[0]:<10} {row[1]:<34} {row[2]}")
    attempts = [
        ("alice",   "Alicep@ss99",   True),
        ("alice",   "wrongpassword", False),
        ("bob",     "B0bSecure!",    True),
        ("unknown", "anypass",       False),
    ]
    print("\n[Step 3 - Login Attempts]")
    print(f"  {'Username':<10} {'Password':<18} {'Result'}")
    print("  " + "-" * 45)
    for uname, pwd, expected in attempts:
        result = authenticate_user(conn, uname, pwd)
        status = "ACCESS GRANTED" if result else "ACCESS DENIED"
        print(f"  {uname:<10} {pwd:<18} {status}")

def hash_verification_demo():
    print("\n" + "="*55)
    print("  Fig 4: Hash Verification Results")
    print("="*55)
    documents = {
        "contract.pdf":  b"This is a legal contract between Party A and Party B.",
        "report.docx":   b"Monthly security report - November 2024.",
        "firmware.bin":  b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09",
    }
    hashes = {}
    print("\n[File Integrity Verification via SHA-256]")
    for fname, content in documents.items():
        h = hashlib.sha256(content).hexdigest()
        hashes[fname] = h
        print(f"  {fname}: {h}")
    print("\n[Simulating tampered file]")
    tampered = b"This is a legal contract between Party A and Party C."
    tampered_hash = hashlib.sha256(tampered).hexdigest()
    original_hash = hashes["contract.pdf"]
    match = hmac.compare_digest(tampered_hash, original_hash)
    print(f"  Original hash : {original_hash}")
    print(f"  Tampered hash : {tampered_hash}")
    print(f"  Integrity check: {'PASSED' if match else 'FAILED - file has been modified!'}")

def password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 12:
        score += 2; feedback.append("+ Length >= 12")
    elif len(password) >= 8:
        score += 1; feedback.append("~ Length 8-11")
    else:
        feedback.append("- Too short")
    if any(c.isupper() for c in password):
        score += 1; feedback.append("+ Uppercase")
    else:
        feedback.append("- No uppercase")
    if any(c.islower() for c in password):
        score += 1; feedback.append("+ Lowercase")
    if any(c.isdigit() for c in password):
        score += 1; feedback.append("+ Digits")
    else:
        feedback.append("- No digits")
    if any(c in string.punctuation for c in password):
        score += 2; feedback.append("+ Special chars")
    else:
        feedback.append("- No special chars")
    weak_list = ["password","123456","qwerty","admin","letmein"]
    if password.lower() in weak_list:
        score = 0; feedback.append("- Common password!")
    labels = {0:"Very Weak",1:"Very Weak",2:"Weak",3:"Fair",
              4:"Good",5:"Strong",6:"Very Strong",7:"Excellent"}
    return {"score": score, "label": labels.get(score,"Strong"), "feedback": feedback}

def security_testing_demo():
    print("\n" + "="*55)
    print("  Fig 5: Password Security Testing")
    print("="*55)
    test_passwords = [
        "password","12345678","Admin1!",
        "Tr0ub4dor&3","X9#mK@pL2!qR","qwerty123"
    ]
    print(f"\n  {'Password':<20} {'Score':<8} {'Strength'}")
    print("  " + "-" * 45)
    for pwd in test_passwords:
        result = password_strength(pwd)
        print(f"  {pwd:<20} {result['score']}/7    {result['label']}")
    print("\n[Hash Algorithm Speed Comparison]")
    sample = b"BenchmarkPassword2024!"
    iterations = 100000
    for algo in ["md5","sha1","sha256","sha512"]:
        start = time.perf_counter()
        for _ in range(iterations):
            hashlib.new(algo, sample).hexdigest()
        elapsed = time.perf_counter() - start
        print(f"  {algo.upper():<8}: {iterations:,} hashes in {elapsed:.3f}s"
              f"  ({iterations/elapsed:,.0f} hashes/sec)")
    print("\n  NOTE: MD5/SHA-1 are too fast - INSECURE for passwords!")
    print("        Use bcrypt or Argon2 for real password storage.")

if __name__ == "__main__":
    print("\n" + "*"*55)
    print("  BIT4138 - Week 6: Hashing and Password Security")
    print("*"*55)
    sha256_demo()
    password_hashing_demo()
    login_auth_demo()
    hash_verification_demo()
    security_testing_demo()
    print("\n" + "="*55)
    print("  Week 6 Complete")
    print("="*55 + "\n")