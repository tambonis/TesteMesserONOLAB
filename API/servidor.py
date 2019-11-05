"""Nome do arquivo: servidor.py
"""

import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import dill as pickle
from pymongo import MongoClient

print('Running..')

def pre_processamento(df, estimativas):
        
    #Resolver nulls
    df['Gender'].fillna(estimativas['mode_gender'], inplace=True)
    df['Married'].fillna(estimativas['mode_married'], inplace=True)
    df['Dependents'].fillna(estimativas['mode_dependents'], inplace=True)
    df['Self_Employed'].fillna(estimativas['mode_self_employed'], inplace=True)
    df['Credit_History'].fillna(estimativas['mode_credit_history'], inplace=True)
    df['LoanAmount'].fillna(estimativas['mode_LoanAmount'], inplace=True)
    df['Loan_Amount_Term'].fillna(estimativas['mode_LoanAmountTerm'], inplace=True)
    
    df['Dependents'] = [str(x) for x in list(df['Dependents'])]
    
    gender_values = {'Female' : 0, 'Male' : 1} 
    married_values = {'No' : 0, 'Yes' : 1}
    education_values = {'Graduate' : 0, 'Not Graduate' : 1}
    employed_values = {'No' : 0, 'Yes' : 1}
    property_values = {'Rural' : 0, 'Urban' : 1, 'Semiurban' : 2}
    dependent_values = {'3+': 3, '0': 0, '2': 2, '1': 1}
    df.replace({'Gender': gender_values, 'Married': married_values, 'Education': education_values, \
                'Self_Employed': employed_values, 'Property_Area': property_values, \
                'Dependents': dependent_values}, inplace=True)
        
    #Adequacao estrutura de df
    
    df['Gender'] = df['Gender'].astype(int)
    df['Married'] = df['Married'].astype(int)
    df['CoapplicantIncome'] = df['CoapplicantIncome'].astype(float)
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].astype(float)
    df['Credit_History'] = df['Credit_History'].astype(float)
        
    return(df)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def apicall():
    """Chamada da API """
    
    print('API chamada: ')
    
    try:
        test_json = request.get_json()
        dados = pd.read_json(test_json, orient='records')

        #Getting the Loan_IDs separated out
        #loan_ids = test['Loan_ID']

    except Exception as e:
            raise e
            
    if dados.empty:
        return(bad_request())
    
    else:
        
        #Adequacoes
        pred_var = ['Gender','Married','Dependents','Education','Self_Employed','ApplicantIncome','CoapplicantIncome',\
                    'LoanAmount','Loan_Amount_Term','Credit_History','Property_Area']
        idd = dados['Loan_ID']
        dados = dados[pred_var]
        
        #Setando...
        modelagem_classificacao = './Modelos/modelo_classificao.pk'
        modelagem_regressao = './Modelos/modelo_regressao.pk'
        
        #Carregando modelos
        with open(modelagem_classificacao, 'rb') as f:
            modelagem_classificacao = pickle.load(f)
        with open(modelagem_regressao, 'rb') as f:
            modelagem_regressao = pickle.load(f)
            
        #Predicoes
        estimativas = modelagem_classificacao[1]
        dados = pre_processamento(dados, estimativas)
        modelo_classificacao = modelagem_classificacao[0]
        emprestar = modelo_classificacao.predict(dados) 

        dados = dados.drop(['LoanAmount'], 1)
        quanto = modelagem_regressao.predict(dados)
        
        #Adequacoes das predicoes para json
        if emprestar==1:
            emprestar='Y' 
        else: 
            emprestar='N'
            quanto = 0 
            
        results = [idd[0], emprestar, round(quanto[0], 2)]
        results = pd.DataFrame(results, index = ['ID', 'Emprestar', 'Quantidade (Milhares)']).transpose() 

        #Enviando...
        responses = jsonify(predictions=results.to_json(orient="records"))
        responses.status_code = 200
            
        #Salvar MongoDB
        
        print('Mongo...')
        
        to_mongo = results.to_dict('index')
        client = MongoClient('localhost')
        db = client.results #Criando banco de dados results
        db.results.insert_one(to_mongo[0])
        
        return (responses)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
