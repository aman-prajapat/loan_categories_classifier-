import pickle
import json
import pandas as pd
import xgboost
import sys

xgModel = pickle.load(open('xgboost_model.pkl','rb'))
colNames = pickle.load(open('finalColumnsName.pkl','rb'))
catColandLabels = json.load(open('CatColumnsAndlabels.json','rb'))
educational_mapping = json.load(open('education_mapping.json','rb'))

def preprocess(filepath):
    
    print("Data Preprocessing...")
    new_data = pd.read_excel(filepath)
    new_data['EDUCATION'] = new_data['EDUCATION'].apply(lambda x : educational_mapping[x])
    encoded_data = pd.get_dummies(new_data,catColandLabels.keys())
    return encoded_data

def predict(data):
    print("Data prediction...")
    X = data[colNames]
    predicted_values  = xgModel.predict(X)
    return pd.Series(predicted_values, name="PredictedValues")


def saveToFile(predicted_values,filepath):
    cat ={0:'P1',1:'P2',2:'P3',3:'P4'}

    raw_data = pd.read_excel(filepath)
    pd.concat([raw_data,predicted_values,predicted_values.apply(lambda x: cat[x])],axis = 1).to_csv('final_data.csv')
    print("File saved at root location")

if __name__ == '__main__':
    data = preprocess(sys.argv[1])
    predicted_values = predict(data)
    saveToFile(predicted_values,sys.argv[1])


