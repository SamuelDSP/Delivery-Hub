from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import products, users


def create_app() -> FastAPI:
    app = FastAPI(title="Product Management System", version="1.0.0")

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
    app.include_router(products.router)
    app.include_router(users.router)


app = create_app()
