import hashlib
import os
import base64
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key, private_key.public_key()

def sign_document(private_key, document):
    return private_key.sign(
        document,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify_signature(public_key, document, signature):
    try:
        public_key.verify(
            signature, document,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def fig1_signature_generation():
    print("\n" + "="*55)
    print("  Fig 1: Digital Signature Generation")
    print("="*55)
    print("\n[Step 1 - Generating RSA-2048 Key Pair]")
    private_key, public_key = generate_key_pair()
    pub_pem = public_key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    print("  + Private Key generated (kept secret - never shared)")
    print(f"  + Public Key preview: {pub_pem.splitlines()[1][:50]}...")
    documents = {
        "contract_v1.pdf": b"LEGAL CONTRACT: Services Agreement between Alpha Corp and Beta Ltd.",
        "invoice_007.pdf": b"INVOICE #007: Amount Due $4,500 - Due Date: 2024-12-01",
        "report_nov.docx": b"SECURITY REPORT November 2024: No critical vulnerabilities found.",
    }
    print(f"\n[Step 2 - Signing Documents with Private Key]")
    print(f"  {'Document':<25} {'SHA-256 Digest':<45} {'Sig Preview'}")
    print("  " + "-" * 90)
    signatures = {}
    for fname, content in documents.items():
        sig = sign_document(private_key, content)
        digest = hashlib.sha256(content).hexdigest()[:40]
        signatures[fname] = (content, sig)
        print(f"  {fname:<25} {digest}...  {sig[:8].hex()}...")
    print(f"\n  + All {len(documents)} documents signed using RSA-2048 + SHA-256 + PSS padding")
    return private_key, public_key, signatures

def fig2_signature_verification(private_key, public_key, signatures):
    print("\n" + "="*55)
    print("  Fig 2: Signature Verification Process")
    print("="*55)
    print(f"\n  {'Document':<25} {'Scenario':<25} {'Result'}")
    print("  " + "-" * 70)
    for fname, (content, sig) in signatures.items():
        valid = verify_signature(public_key, content, sig)
        print(f"  {fname:<25} {'Original document':<25} {'VALID - Authentic' if valid else 'INVALID'}")
        tampered = content + b" [TAMPERED]"
        result = verify_signature(public_key, tampered, sig)
        print(f"  {fname:<25} {'Tampered content':<25} {'VALID' if result else 'INVALID - Tampering detected!'}")
    _, wrong_pub = generate_key_pair()
    fname = list(signatures.keys())[0]
    content, sig = signatures[fname]
    wrong = verify_signature(wrong_pub, content, sig)
    print(f"\n  {'Wrong key test':<25} {'Mismatched key pair':<25} {'VALID' if wrong else 'INVALID - Wrong signer!'}")
    print("\n  [Non-Repudiation]")
    print("  Only the private key holder can sign.")
    print("  Anyone with the public key can verify.")

def fig3_certificate_creation(private_key, public_key):
    print("\n" + "="*55)
    print("  Fig 3: Certificate Creation Using OpenSSL")
    print("="*55)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "KE"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Nairobi"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "BIT4138 Cryptography Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, "cryptolab.bit4138.ac.ke"),
    ])
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    print("\n[X.509 Self-Signed Certificate Details]")
    print(f"  Subject       : BIT4138 Cryptography Lab, Nairobi, KE")
    print(f"  Issuer        : BIT4138 Cryptography Lab (Self-Signed)")
    print(f"  Serial Number : {cert.serial_number}")
    print(f"  Valid From    : {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Valid Until   : {(now + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Signature Alg : SHA256WithRSAEncryption")
    print(f"  Key Size      : 2048 bits")
    pem = cert.public_bytes(serialization.Encoding.PEM).decode()
    print(f"\n[PEM Certificate Preview]")
    for line in pem.splitlines()[:4]:
        print(f"  {line}")
    print("  ...")
    with open("certificate.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"\n  + Certificate saved to C:\\BIT4138\\certificate.pem")
    return cert

def fig4_document_validation(private_key, public_key, cert):
    print("\n" + "="*55)
    print("  Fig 4: Secure Document Validation")
    print("="*55)
    document = (
        "OFFICIAL DOCUMENT\n"
        "BIT4138 Advanced Cryptography - Grade Report\n"
        "Student: Abdirahman | Score: 87/100\n"
        f"Timestamp: {datetime.utcnow().isoformat()}Z"
    ).encode()
    signature = sign_document(private_key, document)
    envelope = {
        "document": base64.b64encode(document).decode(),
        "signature": base64.b64encode(signature).decode(),
        "algorithm": "RSA-PSS-SHA256",
        "issued_by": "BIT4138 Cryptography Lab",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    print("\n[Signed Document Envelope]")
    print(f"  Algorithm  : {envelope['algorithm']}")
    print(f"  Issued By  : {envelope['issued_by']}")
    print(f"  Timestamp  : {envelope['timestamp']}")
    print(f"  Signature  : {envelope['signature'][:48]}...")
    print("\n[Validation Checks]")
    doc_bytes = base64.b64decode(envelope["document"])
    sig_bytes = base64.b64decode(envelope["signature"])
    sig_valid = verify_signature(public_key, doc_bytes, sig_bytes)
    now = datetime.utcnow()
    cert_valid = cert.not_valid_before <= now <= cert.not_valid_after
    algo_ok = envelope["algorithm"] in ["RSA-PSS-SHA256", "ECDSA-SHA256"]
    checks = [
        ("Signature integrity", sig_valid),
        ("Certificate validity period", cert_valid),
        ("Algorithm approved", algo_ok),
    ]
    for name, result in checks:
        print(f"  {name:<30} {'PASS' if result else 'FAIL'}")
    overall = all(r for _, r in checks)
    print(f"\n  Overall: {'DOCUMENT AUTHENTIC AND TRUSTED' if overall else 'VALIDATION FAILED'}")

def fig5_certificate_testing(private_key, public_key, cert):
    print("\n" + "="*55)
    print("  Fig 5: Certificate Testing Results")
    print("="*55)
    msg = b"Test message for certificate validation."
    sig = sign_document(private_key, msg)
    tests = []
    result = verify_signature(public_key, msg, sig)
    tests.append(("Valid signature verification", result == True))
    corrupted = bytearray(sig)
    corrupted[10] ^= 0xFF
    result2 = verify_signature(public_key, msg, bytes(corrupted))
    tests.append(("Corrupted signature detection", result2 == False))
    result3 = verify_signature(public_key, msg + b" extra", sig)
    tests.append(("Modified message detection", result3 == False))
    _, pub2 = generate_key_pair()
    cert2 = (
        x509.CertificateBuilder()
        .subject_name(cert.subject)
        .issuer_name(cert.issuer)
        .public_key(pub2)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    tests.append(("Certificate serial uniqueness", cert.serial_number != cert2.serial_number))
    now = datetime.utcnow()
    cert_ok = cert.not_valid_before <= now <= cert.not_valid_after
    tests.append(("Certificate within validity period", cert_ok))
    print(f"\n  {'Test Case':<38} {'Status'}")
    print("  " + "-" * 50)
    passed = 0
    for name, result in tests:
        if result:
            passed += 1
        print(f"  {name:<38} {'PASS' if result else 'FAIL'}")
    print(f"\n  Tests Passed : {passed}/{len(tests)}")
    print(f"  Security Score: {passed/len(tests)*100:.0f}%")
    print("\n[Certificate Chain of Trust]")
    print("  Root CA -> Intermediate CA -> End-Entity Certificate")
    print("  Each level signs the next, creating a chain of trust.")
    print("  Self-signed certs are for development/testing only.")

if __name__ == "__main__":
    print("\n" + "*"*55)
    print("  BIT4138 - Week 7: Digital Signatures and Certificates")
    print("*"*55)
    private_key, public_key, signatures = fig1_signature_generation()
    fig2_signature_verification(private_key, public_key, signatures)
    cert = fig3_certificate_creation(private_key, public_key)
    fig4_document_validation(private_key, public_key, cert)
    fig5_certificate_testing(private_key, public_key, cert)
    print("\n" + "="*55)
    print("  Week 7 Complete")
    print("="*55 + "\n")