import urllib.request
import json
import time
import random

from typing import Tuple, Optional


def fetch_json_with_retries(url: str, timeout: float = 5.0, retries: int = 2, backoff_base: float = 0.5) -> Tuple[Optional[object], Optional[str]]:
    """Fetch JSON from `url` with simple retry/backoff.

    Returns (payload_or_none, error_message_or_none).
    """
    last_exc = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.load(resp)
            return data, None
        except Exception as e:
            last_exc = e
            if attempt == retries:
                return None, str(e)
            # exponential backoff with small jitter
            sleep_sec = backoff_base * (2 ** attempt) + random.uniform(0, backoff_base)
            try:
                time.sleep(sleep_sec)
            except Exception:
                # In tests, time.sleep may be patched to raise or be a no-op - ignore
                pass
    return None, str(last_exc) if last_exc is not None else 'unknown error'