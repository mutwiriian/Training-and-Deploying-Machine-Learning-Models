from pydantic import BaseModel

class TemperaturePrediction(BaseModel):
    temp_pred: float