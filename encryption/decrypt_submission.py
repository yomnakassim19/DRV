# decrypt_submission.py

import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_submission(enc_file, key_file, output_csv, private_key_path):

    # Load private key
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Load encrypted symmetric key
    with open(key_file, "rb") as f:
        encrypted_key = f.read()

    # Decrypt symmetric key
    symmetric_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    fernet = Fernet(symmetric_key)

    # Decrypt data
    with open(enc_file, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_csv, "wb") as f:
        f.write(decrypted_data)

    print("✅ Decryption complete:", output_csv)


if __name__ == "__main__":
    decrypt_submission(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
