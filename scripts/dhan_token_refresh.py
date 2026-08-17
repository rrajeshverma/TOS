"""
Generate and validate a fresh Dhan access token using TOTP.

Secrets:
    ~/.tos_dhan_totp

Runtime token:
    ~/.tos_dhan_runtime.env
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pyotp
import requests

SECRET_FILE = Path.home() / ".tos_dhan_totp"
RUNTIME_TOKEN_FILE = Path.home() / ".tos_dhan_runtime.env"

TOKEN_URL = "https://auth.dhan.co/app/generateAccessToken"
PROFILE_URL = "https://api.dhan.co/v2/profile"


def load_secret_file() -> None:
    if not SECRET_FILE.exists():
        raise FileNotFoundError(f"Missing Dhan TOTP secret file: {SECRET_FILE}")

    for line in SECRET_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")

        if separator:
            os.environ[key.strip()] = value.strip()


def generate_token() -> tuple[str, str]:
    load_secret_file()

    client_id = os.environ["DHAN_CLIENT_ID"]
    pin = os.environ["DHAN_PIN"]
    secret = os.environ["DHAN_TOTP_SECRET"]

    totp = pyotp.TOTP(secret).now()

    response = requests.post(
        TOKEN_URL,
        params={
            "dhanClientId": client_id,
            "pin": pin,
            "totp": totp,
        },
        timeout=15,
    )

    data = response.json()

    if not response.ok or not data.get("accessToken"):
        message = data.get("message") or data.get("errorMessage") or data

        raise RuntimeError(f"Dhan token generation failed: {message}")

    access_token = data["accessToken"]
    expiry_time = str(data.get("expiryTime", ""))

    return access_token, expiry_time


def validate_token(access_token: str) -> str:
    response = requests.get(
        PROFILE_URL,
        headers={
            "access-token": access_token,
            "Content-Type": "application/json",
        },
        timeout=15,
    )

    data = response.json()

    if not response.ok:
        message = data.get("message") or data.get("errorMessage") or data

        raise RuntimeError(f"Dhan token validation failed: {message}")

    return str(data.get("tokenValidity", ""))


def write_runtime_token(
    client_id: str,
    access_token: str,
) -> None:
    content = f"DHAN_CLIENT_ID={client_id}\nDHAN_ACCESS_TOKEN={access_token}\n"

    RUNTIME_TOKEN_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fd, temp_path = tempfile.mkstemp(
        prefix=".tos_dhan_runtime.",
        dir=RUNTIME_TOKEN_FILE.parent,
        text=True,
    )

    try:
        os.chmod(temp_path, 0o600)

        with os.fdopen(
            fd,
            "w",
            encoding="utf-8",
        ) as handle:
            handle.write(content)

        os.replace(
            temp_path,
            RUNTIME_TOKEN_FILE,
        )

    except Exception:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass

        raise

    os.chmod(RUNTIME_TOKEN_FILE, 0o600)


def main() -> int:
    load_secret_file()

    client_id = os.environ["DHAN_CLIENT_ID"]

    access_token, expiry_time = generate_token()
    token_validity = validate_token(access_token)

    write_runtime_token(
        client_id=client_id,
        access_token=access_token,
    )

    print("✅ Dhan token refresh PASSED")
    print("expiryTime    :", expiry_time)
    print("token validity:", token_validity)
    print("runtime file  :", RUNTIME_TOKEN_FILE)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
