from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers.users import router as users_router
from api.routers.posts import router as posts_router
from core.errors import ConflictError, DomainError, NotFoundError, ValidationError
from core.responses import error
from middlewares.db_session import DbSessionMiddleware
from middlewares.jwt_auth import JwtAuthMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="Socialz")

    # Middlewares (order matters: auth → db session)
    app.add_middleware(JwtAuthMiddleware)
    app.add_middleware(DbSessionMiddleware)

    # Routers
    app.include_router(users_router)
    app.include_router(posts_router)

    # Global error handler mapping DomainError → consistent HTTP response
    @app.exception_handler(DomainError)
    async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
        status = 400
        if isinstance(exc, ValidationError):
            status = 422
        elif isinstance(exc, NotFoundError):
            status = 404
        elif isinstance(exc, ConflictError):
            status = 409

        return JSONResponse(
            status_code=status,
            content=error(exc.code, exc.message, details=exc.details),
        )

    return app


app = create_app()

