import mlflow
import pandas as pd

model = mlflow.pyfunc.load_model('model/')

cols = model.metadata.signature.inputs

data_dict = {}
for c in cols:
    name = c.name
    if name == 'Crop_Year':
        data_dict[name] = [0]
    elif name == 'Area':
        data_dict[name] = [0.0]
    else:
        data_dict[name] = [False]
df = pd.DataFrame(data_dict)

df = pd.DataFrame(data_dict)

df.at[0, 'Crop_Year'] = 2015
df.at[0, 'Area'] = 10.0
df.at[0, 'State_Name_Karnataka'] = True
df.at[0, 'District_Name_BANGALORE RURAL'] = True

pred = model.predict(df)
print('Success prediction:', pred[0])
