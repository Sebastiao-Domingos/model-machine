#!/usr/bin/env python
# coding: utf-8

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn


#In[1]:

import pandas as pn


prev = pn.read_csv("prev.csv")
print("Fechamento anterior : ",prev["Close"][0])
print("Previsão anterior: ",prev["target"][0])
data = pn.read_csv("data.csv")

try:
    amanha = pn.read_csv("amanha.csv")
    print("Fechamento atual: ", amanha["Close"][0])
    data = data.append(amanha[:1], sorted = True)
    amanha = amanha.drop(amanha[:1].index , axis=0)
    data.to_csv("data.csv" , index=False)
    amanha.to_csv("amanha.csv" , index=False)

except Exception:

    print("O fechamento ainda não ocorreu")

    pass
   

# data = dados.drop(dados[-1::].index , axis=0)
# data.to_csv("data.csv")
#Adicionar uma coluna com o valor da proxima linha para prever 

data["target"] = data["Close"][1:len(data)].reset_index(drop=True)

#Pegamos a ultima linha, que iremos usar para prever
# prev = data[-1::].drop("target" ,axis=1)
# data.to_csv("prev.csv")
#Pegar o valores de treino

train = data.drop(data[-1::].index , axis=0)

#Alterar  o valor do target para 0 ou 1 , ou seja para linha se o valor do close for maior que o target então o target será 1 senão 0

train.loc[train["target"] > train["Close"] , "target"] = 1

train.loc[train["target"] != 1 , "target"] = 0

# print(data.tail())
# print("prever")
# print(prev.tail())
# print("treino")
# print(train.tail())
#Criar o modelo de machine learning

y = train["target"]
X = train.drop("target" , axis=1)


#Separar o dataset em treino e teste
from sklearn.model_selection import train_test_split

X_train, X_test , y_train, y_test = train_test_split(X , y , test_size=0.3 , random_state=42)


#Criar o modelo de machine learning
from sklearn.ensemble import ExtraTreesClassifier

model = ExtraTreesClassifier()
model.fit(X_train , y_train)


#Testar o modelo
valor =  model.score(X_test , y_test)
print(f"Acurácia : {valor}")

prev["target"] = model.predict(prev)
print("Fechemaneto de ontem : " , prev["Close"][0])

if prev["target"][0] == 1:
    print("Vai subir")
else:
    print("Vai cair")


prev.to_csv("prev.csv" , index=False)

prev = model.predict(amanha)

print(prev)
# %%
