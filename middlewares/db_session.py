from __future__ import annotations

from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from db.session import get_session


class DbSessionMiddleware(BaseHTTPMiddleware):
    """
    Creates exactly one DB session per request and attaches it as:
      request.state.db

    Transaction boundaries live in services (commit) and this middleware
    provides rollback-on-error + reliable close.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        db = get_session()
        request.state.db = db
        try:
            response = await call_next(request)
            return response
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

