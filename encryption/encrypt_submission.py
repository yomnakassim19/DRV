# encrypt_submission.py

import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt_submission(input_csv, output_enc, output_key, public_key_path):

    # Generate symmetric key
    symmetric_key = Fernet.generate_key()
    fernet = Fernet(symmetric_key)

    # Encrypt CSV
    with open(input_csv, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(output_enc, "wb") as f:
        f.write(encrypted_data)

    # Load public key
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Encrypt symmetric key with RSA
    encrypted_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_key, "wb") as f:
        f.write(encrypted_key)

    print("✅ Encrypted successfully")
    print(f"Generated: {output_enc}, {output_key}")


if __name__ == "__main__":
    encrypt_submission(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
