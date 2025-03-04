import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC 
import pickle

# Load data
file_path = r'Data_final3.csv'
df = pd.read_csv(file_path)

# Separate features and target variable
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

oversample = SMOTE(sampling_strategy={0: 169, 1: 169, 2: 169, 3: 169, 4: 169,5: 169, 6: 169, 7: 169, 8: 169})
X, y = oversample.fit_resample(X, y)


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=104, test_size=0.10, shuffle=True)



model = XGBClassifier(objective='multi:softprob')

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

pickle.dump(model, open('model.pkl','wb'))

# Loading model to compare the results
# model = pickle.load(open('model.pkl','rb'))

# print(y_pred)

accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)