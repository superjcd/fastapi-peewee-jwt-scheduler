import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.routes import api_router
from app.providers.database import db, redis_client
# third party providers
from app.providers import app_provider
from app.providers import logging_provider
from app.providers import handle_exception

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("starting app")
    yield
    print("shutdown app")
    cleanup()

def cleanup():
    if not db.is_closed():
        db.close()

    if redis_client:
        redis_client.close()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    register_provider(app, logging_provider)
    register_provider(app, app_provider)
    register_provider(app, handle_exception)
    
    install_router(app, api_router, prefix="/api")
    return app


def register_provider(app, provider):
    assert hasattr(provider, "register")
    provider.register(app)
    logging.info(provider.__name__ + ' registered')


def install_router(app, api_router, prefix):
    app.include_router(api_router, prefix=prefix)
    if app.debug:
        for route in app.routes:
            print({'path': route.path, 'name': route.name, 'methods': route.methods})