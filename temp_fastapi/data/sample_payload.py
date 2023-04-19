import pandas as pd
import json
import os

dir=os.path.join(os.path.dirname(__file__))

data=pd.read_csv(os.path.join(dir,'sample_data.csv'))

example=data.sample(1).to_dict() #.to_json(os.path.join(dir,'example.json'))
example_dict={k: list(v.values())[0] for k,v in example.items()}

with open(os.path.join(dir,'example.json'),'w') as f:
    json.dump(example_dict,f)

