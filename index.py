import pandas as pn


dados = pn.read_csv("GSPC.csv")
dados = dados.drop("Date" , axis=1)

print(dados[-2::]) # listar as duas ultimas linhas
amanha = dados[-1::] # pegar a ultima linha
# amanha.to_csv("amanha.csv")

data = dados.drop(dados[-1::].index , axis=0)
# data.to_csv("data.csv")

#Adicionar uma coluna com o valor da proxima linha para prever 
data["target"] = data["Close"][1:len(data)].reset_index(drop=True)

#Pegamos a ultima linha, que iremos usar para prever
prev = data[-1::].drop("target" ,axis=1)

#Pegar o valores de treino
train = data.drop(data[-1::].index , axis=0)

#Alterar  o valor do target para 0 ou 1 , ou seja para linha se o valor do close for maior que o target então o target será 1 senão 0

train.loc[train["target"] > train["Close"] , "target"] = 1

train.loc[train["target"] != 1 , "target"] = 0

print(data.tail())

print("prever")
print(prev.tail())

print("treino")
print(train.tail())

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

prev = model.predict(amanha)

print(prev)