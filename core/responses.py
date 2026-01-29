from typing import Any, Optional


def success(data: Any, *, meta: Optional[dict] = None) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": meta or {},
    }


def error(code: str, message: str, *, details: Optional[dict] = None) -> dict:
    payload: dict = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload

