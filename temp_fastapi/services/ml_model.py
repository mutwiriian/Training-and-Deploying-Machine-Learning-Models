from temp_fastapi.models.payload import (TemperaturePredictionPayload,payload_to_list)
from temp_fastapi.models.prediction import TemperaturePrediction

from temp_fastapi.core.messages import NO_VALID_PAYLOAD

import numpy as np
import joblib

class TemperaturePredictionModel(object):
    def __init__(self,path):
        self.path=path
        self._load_local_model()

    def _load_local_model(self):
        self.model=joblib.load(self.path)

    def _preprocess(self,payload: TemperaturePredictionPayload) -> np.ndarray:
        processed=np.asarray(payload_to_list(payload)).reshape(1,-1)
        return processed
    
    def _process_prediction(self,prediction: float) -> TemperaturePrediction:
        tp=TemperaturePrediction(temp_pred=prediction)
        return tp
    
    def _predict(self,features: np.ndarray) -> float:
        prediction: float = self.model.predict(features)
        return prediction
    
    def predict(self,payload: TemperaturePredictionPayload):
        if payload is None:
            raise ValueError(NO_VALID_PAYLOAD.format(payload))
        
        processed_payload=self._preprocess(payload)
        prediction=self._predict(processed_payload)
        processed_prediction=self._process_prediction(prediction)
        return processed_prediction


