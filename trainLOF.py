import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

# Carregue seus dados em um DataFrame
dados = pd.read_csv('dadosTreino.csv')

#remove empty rows
dados = dados.dropna()

# Crie um modelo LOF
lof = LocalOutlierFactor()

#train model
lof.fit(dados)

#save model
import pickle
pickle.dump(lof, open('lof.pkl', 'wb'))



# Ajuste o modelo aos seus dados
outliers = lof.fit_predict(dados)



# Identifique os pontos de dados anômalos
anomalias = dados[outliers == -1]
print(anomalias)
