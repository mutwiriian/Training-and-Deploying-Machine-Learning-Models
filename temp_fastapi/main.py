import uvicorn
from fastapi import FastAPI

from api.routes.router import api_router
from core.event_handlers import (startup_handler,shutdown_handler)

#instantiate the FastAPI object and assign models and event handlers 
def get_app() -> FastAPI:
    app = FastAPI(title='Inference for Support Vector,Random Forest and LightGBM Models',
                  description='Inference from Scikit-Learn models for high dimensional data',
                  version='0.0.1')
    app.include_router(api_router)

    app.add_event_handler('startup',startup_handler(app))
    app.add_event_handler('shutdown',shutdown_handler(app))
    return app

app = get_app()

#start the server by running the file
#alternatively you can use the CLI
if __name__=='__main__':
    uvicorn.run('main:app',host='127.0.0.1',port=8080,reload=True)
