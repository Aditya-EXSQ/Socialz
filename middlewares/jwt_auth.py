from __future__ import annotations

from typing import Callable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class JwtAuthMiddleware(BaseHTTPMiddleware):
    """
    Minimal JWT middleware stub.

    README says: extract JWT, validate, attach request.user_id.
    You can extend this later; for now it sets `request.state.user_id = None`
    unless a real auth implementation is added.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # TODO: parse Authorization header and validate JWT
        request.state.user_id = _extract_user_id_placeholder(request)
        return await call_next(request)


def _extract_user_id_placeholder(_: Request) -> Optional[int]:
    return None

