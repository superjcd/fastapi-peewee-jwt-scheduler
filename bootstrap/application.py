import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes.routes import api_router
from app.providers.database import db, redis_client
from app.providers import logging_provider
from app.providers import handle_exception
from config.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("starting app")
    yield
    print("shutting down app")
    cleanup()

def cleanup():
    if not db.is_closed():
        db.close()

    if redis_client:
        redis_client.close()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    prepare_app(app)
    # third party providers
    register_provider(app, logging_provider)
    register_provider(app, handle_exception)
    return app

def prepare_app(app:FastAPI):
    app.debug = settings.DEBUG
    app.title = settings.NAME

    add_global_middleware(app)
    install_router(app, api_router, prefix="/api")

def add_global_middleware(app: FastAPI):
    """
    注册全局中间件
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def install_router(app, api_router, prefix):
    app.include_router(api_router, prefix=prefix)
    if app.debug:
        for route in app.routes:
            print({'path': route.path, 'name': route.name, 'methods': route.methods})


def register_provider(app, provider):
    assert hasattr(provider, "register")
    provider.register(app)
    logging.info(provider.__name__ + ' registered')
