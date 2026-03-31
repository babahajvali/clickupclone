import httpx
from django.conf import settings


def verify_captcha_token(token: str, remote_ip: str | None = None) -> tuple[
    bool, str]:
    if not token:
        return False, "CAPTCHA token is required."

    if not settings.CAPTCHA_SECRET_KEY:
        return False, "CAPTCHA is not configured."

    payload = {
        "secret": settings.CAPTCHA_SECRET_KEY,
        "response": token,
    }

    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        response = httpx.post(
            settings.CAPTCHA_VERIFY_URL,
            data=payload,
            timeout=5.0,
        )
        response.raise_for_status()
        response_data = response.json()
    except (httpx.HTTPError, ValueError):
        return False, "CAPTCHA verification request failed."

    if response_data.get("success"):
        return True, ""

    return False, "CAPTCHA validation failed."
