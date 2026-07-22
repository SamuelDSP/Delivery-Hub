from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.routes import orders, products, users


def create_app() -> FastAPI:
    app = FastAPI(title="Product Management System", version="1.0.0")

    @app.get("/")
    def health_check():
        return {"status": "ok"}

    add_cors_middleware(app)
    include_routers(app)

    return app


def add_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_routers(app: FastAPI):
    include_api_routers(app)
    include_api_routers(app, prefix="/api")
    include_api_routers(app, prefix="/api/backend")


def include_api_routers(app: FastAPI, prefix: str = ""):
    app.include_router(auth_router.router, prefix=prefix)
    app.include_router(products.router, prefix=prefix)
    app.include_router(orders.router, prefix=prefix)
    app.include_router(users.router, prefix=prefix)


app = create_app()
