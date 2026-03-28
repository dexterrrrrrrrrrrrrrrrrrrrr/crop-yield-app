import mlflow.sklearn
import pandas as pd

model = mlflow.sklearn.load_model('model/')

feature_names = model.feature_names_in_.tolist()

input_data = {col: 0.0 for col in feature_names}
input_data['Crop_Year'] = 2015.0
input_data['Area'] = 10.0
input_data['State_Karnataka'] = 1.0
input_data['District_BANGALORE RURAL'] = 1.0
input_data['Season_Rabi'] = 1.0
input_data['Crop_Rice'] = 1.0

input_df = pd.DataFrame([input_data])

pred = model.predict(input_df)

print('Sklearn prediction:', pred[0])
