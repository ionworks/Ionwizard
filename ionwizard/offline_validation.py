import os
import json
import base64
import pathlib
from typing import Any
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def verify_offline(license_path: str | pathlib.Path):
    verify_license(decode_license(get_license_file(license_path)))


def verify_license(decoded_license: dict[str, Any]):
    try:
        verify_key = VerifyKey(
            bytes.fromhex(os.environ["IONWORKS_OFFLINE_PUBLIC_KEY"]),
        )
        verify_key.verify(
            ("license/%s" % decoded_license["enc"]).encode(),
            base64.b64decode(decoded_license["sig"]),
        )
    except (AssertionError, BadSignatureError) as e:
        raise ValueError("Verification failed!") from e


def decode_license(license_file: str) -> dict[str, Any]:
    payload = license_file.replace("-----BEGIN LICENSE FILE-----\n", "")
    payload.replace("-----END LICENSE FILE-----\n", "")
    data = json.loads(base64.b64decode(payload))
    alg = data["alg"]
    if alg != "aes-256-gcm+ed25519":
        raise RuntimeError("License must be encoded with the ED25519 algorithm.")
    return data


def get_license_file(license_path: str | pathlib.Path) -> str:
    license_file = None
    try:
        with open(license_path) as f:
            license_file = f.read()
    except (FileNotFoundError, PermissionError) as e:
        raise FileNotFoundError("License key file not found.") from e
    return license_file
