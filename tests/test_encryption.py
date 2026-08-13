from app.encryption import decrypt_data, encrypt_data


def test_encrypt_and_decrypt_round_trip():
    original = "Sensitive test data"

    encrypted = encrypt_data(original)
    decrypted = decrypt_data(encrypted)

    assert encrypted != original
    assert decrypted == original


def test_encrypted_value_is_not_plaintext():
    original = "Sensitive test data"

    encrypted = encrypt_data(original)

    assert original not in encrypted