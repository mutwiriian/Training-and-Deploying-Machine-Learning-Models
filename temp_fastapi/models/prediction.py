from pydantic import BaseModel

#create response model for the prediction object
class TemperaturePrediction(BaseModel):
    temp_pred: float