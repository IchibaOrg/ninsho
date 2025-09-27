import logging

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

from ninsho.api import auth
from ninsho.db.register_models import setup_models

logger = logging.getLogger(__name__)



def setup_api(api: FastAPI):
    api.include_router(auth.router, tags=["auth"])


def create_app() -> FastAPI:
    from ninsho.config import config

    setup_models()

    api = FastAPI(
        title=config.app_name, debug=config.debug, docs_url="/api_docs", redoc_url=None
    )

    api.add_middleware(
        SessionMiddleware,
        secret_key=config.app_session_secret_key,
        session_cookie="ninshosession"
    )

    setup_api(api)

    return api


app = create_app()

@app.get("/health")
def health() -> dict[str, str]:
    logger.debug("health called!")
    return {"status": "ok"}
