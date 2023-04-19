from pydantic import BaseModel
import json
import os

cols_path= os.path.join(os.path.dirname(__file__),'..','data','cols.json')

with open(cols_path,'r') as f:
    cols=json.load(f)

fields={}
for col_name,col_type in cols.items():
    fields[col_name]=eval(col_type)

class TemperaturePredictionPayload(BaseModel):
    __annotations__=fields

#test_df=pd.DataFrame({
#    'column_1':[34,67],
#    'column_2':[34.7,25.8],
#    'column_3':[12,9],
#    'column_4':[45.9,32.1]
#    })
#os.path.join(os.path.dirname(__file__),'../data/sample_data.csv')
#sample_data_path='./temp_fastapi/data/sample_data.csv'
#test_df=pd.read_csv(sample_data_path)

#sample_payload=TemperaturePredictionPayload(**test_df.iloc[1])
#print(sample_payload)
#print(sample_payload.wtd_mean_fie)

def payload_to_list(temp_payload: TemperaturePredictionPayload)-> list:
    return [temp_payload.__getattribute__(col) for col in cols.keys()] #getattr(temp_payload,col)

#list_form=payload_to_list(sample_payload)
#print(list_form)