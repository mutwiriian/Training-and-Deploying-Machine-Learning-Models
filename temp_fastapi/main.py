from fastapi import FastAPI

from temp_fastapi.api.routes.router import api_router
from temp_fastapi.core.event_handlers import (startup_handler,stop_app_handler)

def get_app() -> FastAPI:
    fast_app = FastAPI()
    fast_app.include_router(api_router)

    fast_app.add_event_handler('startup',startup_handler(fast_app))
    fast_app.add_event_handler('shutdown',stop_app_handler(fast_app))
    return fast_app

app = get_app()