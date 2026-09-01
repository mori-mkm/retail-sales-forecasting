# realização dos testes de estacionariedade

def teste_estacionaridade(df_vendas, lojas_):
    #Teste de Dickey-Fuller
    from statsmodels.tsa.stattools import adfuller
    import pandas as pd
    import numpy as np
    print('Dickey-Fuller Test')
    #Série vazia
    serie = pd.Series()
    #Listas dos nomes das lojas com series estaci. e n estaci.
    estac   = []
    n_estac = []
    #Calculo do teste de Dickey-Fuller
    for loja in lojas_:
        serie = df_vendas[loja].dropna()
        dftest = adfuller(serie, autolag='AIC')
        dfoutput = pd.Series(dftest[1:2])
        
        if dfoutput[0] < 0.05: 
            estac.append(loja) 
        else:
            n_estac.append(loja)
    print("Quant. estacionárias = {first} e não estacionárias {second}".format(first= (len(estac)), second=(len(n_estac))))

    return estac, n_estac;

