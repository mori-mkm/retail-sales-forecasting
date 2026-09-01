## Validar as previsões do modelo 
## Link fonte: https://medium.com/ensina-ai/princ%C3%ADpios-b%C3%A1sicos-para-criar-previs%C3%B5es-de-s%C3%A9ries-temporais-e58c451a25b


def mae(predicao, teste):
    import numpy as np

#    print("Erro Médio da Previsão")
    erro = teste - predicao 
    return round(np.abs(erro).mean(), 1)

def mfe(predicao, teste):
    import numpy as np

#    print("Erro Médio Absoluto")
    erro = teste - predicao 
    return round(erro.mean(), 1)

def mse(predicao, teste):
    import numpy as np

#    print("Erro Quadrático Médio")
    erro = ( teste - predicao )**2
    return round(erro.mean(), 1)

def rmse(predicao, teste):

#    print("Erro Quadrático Médio da Raiz")
    from sklearn.metrics import mean_squared_error

    return round(mean_squared_error(predicao, teste)**(1/2),1);

# Function for mean_absolute_percentage_error
def mape(predicao, teste):
    import numpy as np 
    
#    print("Erro Percentual Médio Absoluto")
    return round(np.mean(np.abs((teste - predicao) / teste))*100 ,1)

def acuracia(predicao, teste):
    import pandas as pd
    from datetime import datetime
    primeiro_dia = (datetime.strftime(teste.index.tolist()[0], '%Y-%m-%d'))
    ultimo_dia   = (datetime.strftime(teste.index.tolist()[-1], '%Y-%m-%d'))

    ERRO = (teste - predicao[primeiro_dia:ultimo_dia]).sum()
    MAE  = mae(predicao[primeiro_dia:ultimo_dia], teste)
    MFE  = mfe(predicao[primeiro_dia:ultimo_dia], teste)
    MSE  = mse(predicao[primeiro_dia:ultimo_dia], teste)
    MAPE = mape(predicao[primeiro_dia:ultimo_dia], teste)
    RMSE = rmse(predicao[primeiro_dia:ultimo_dia], teste)

    acuracias = {"ERRO":ERRO, "MAE":MAE, "MFE":MFE, "MSE":MSE, "RMSE":RMSE, "MAPE":MAPE }
    return pd.DataFrame(list(acuracias.items()),columns = ["Métricas", "Valores"])
