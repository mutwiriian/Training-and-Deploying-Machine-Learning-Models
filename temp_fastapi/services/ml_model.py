from models.payload import (TemperaturePredictionPayload,payload_to_list)
from models.prediction import TemperaturePrediction

from core.messages import NO_VALID_PAYLOAD

import numpy as np
import joblib

#define the class to create instances from model path, preprocess the data and make predictions
class TemperaturePredictionModel(object):
    def __init__(self,path):
        self.path=path
        self._load_local_model()

    #read .joblib model objects
    def _load_local_model(self):
        self.model=joblib.load(self.path)
    #extract individual column values
    def _preprocess(self,payload: TemperaturePredictionPayload) -> np.ndarray:
        processed=np.asarray(payload_to_list(payload)).reshape(1,-1)
        return processed
    
    #run prediction
    def _predict(self,features: np.ndarray) -> float:
        prediction: float = self.model.predict(features)
        return prediction
    
    #return prediction model
    def _process_prediction(self,prediction: float) -> TemperaturePrediction:
        tp=TemperaturePrediction(temp_pred=prediction)
        return tp
    
    #collect pre-processing steps and predictions
    def predict(self,payload: TemperaturePredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))
        
        processed_payload=self._preprocess(payload)
        prediction=self._predict(processed_payload)
        processed_prediction=self._process_prediction(prediction)
        return processed_prediction
    