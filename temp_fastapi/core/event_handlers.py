from typing import Callable
from fastapi import FastAPI
from services.ml_model import TemperaturePredictionModel
from core.config import PATH_SVR,PATH_RF,PATH_GBM
from enum import Enum

#restrict models to run inferences on
class ModelPaths(str,Enum):
    model_path_rf=PATH_RF
    model_path_svr=PATH_SVR
    model_path_lgbm=PATH_GBM

#attach/instantiate models to fastapi object when FastAPI app is created
def _startup_model(app: FastAPI) -> None:
    app.state.model_rf=TemperaturePredictionModel(ModelPaths.model_path_rf)
    app.state.model_svr=TemperaturePredictionModel(ModelPaths.model_path_svr)
    app.state.model_lgbm=TemperaturePredictionModel(ModelPaths.model_path_lgbm)

#delete models from FastAPI app instance when app is closing
def _shutdown_model(app: FastAPI) -> None:
    app.state.model_rf= None
    app.state.model_svr= None
    app.state.model_gbm= None

#define a wrapper around function to instantiate app
def startup_handler(app : FastAPI) -> Callable:
    def startup() -> None:
        _startup_model(app)
    return startup

#define wrapper around function to close app
def shutdown_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)
    return shutdown





