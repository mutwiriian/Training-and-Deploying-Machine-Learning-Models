from typing import Callable
from fastapi import FastAPI
from temp_fastapi.services.ml_model import TemperaturePredictionModel
from temp_fastapi.core.config import PATH_SVR,PATH_RF,PATH_GBM
from enum import Enum

class ModelPaths(str,Enum):
    model_path_rf=PATH_RF
    model_path_svr=PATH_SVR
    model_path_gbm=PATH_GBM

def _startup_model(app: FastAPI) -> None:
    app.state.model_rf=TemperaturePredictionModel(ModelPaths.model_path_rf)
    app.state.model_svr=TemperaturePredictionModel(ModelPaths.model_path_svr)
    app.state.model_gbm=TemperaturePredictionModel(ModelPaths.model_path_gbm)

def _shutdown_model(app: FastAPI) -> None:
    app.state.model_rf= None
    app.state.model_svr= None
    app.state.model_gbm= None

def startup_handler(app : FastAPI) -> Callable:
    def startup() -> None:
        _startup_model(app)
    return startup

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)
    return shutdown





