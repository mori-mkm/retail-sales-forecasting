# diferenciação das séries

def diferenciacao(df_n_estac):
    from statsmodels.tsa.stattools import adfuller
    import pandas as pd
    print("Processo de diferenciação")
    
    n_estac = df_n_estac.columns.tolist()
    
    for loja in n_estac:
        df_n_estac[loja] =  df_n_estac[loja] - df_n_estac[loja].shift()  #Diferenciação

    df_n_estac.dropna( axis = 0,inplace=True)

    estac2   = []
    n_estac2 = [] 

    for loja in n_estac:  
      dftest = adfuller(df_n_estac[loja], autolag='AIC') #Teste Dickey-Fuller
      dfoutput = pd.Series(dftest[1:2]) #Verifico se é estacionária
      if dfoutput[0] < 0.05: 
        estac2.append(loja) 
      else:
        n_estac2.append(loja)
    print("Quant. estacionárias = {first} e não estacionárias {second}".format(first= (len(estac2)), second=(len(n_estac2))))

    #Dataframe com as séries estacionarias
    df_estac2 = df_n_estac[estac2]
    #Dataframe com as séries nao estacionarias
    df_n_estac2 = df_n_estac[n_estac2]
    print("Shape Df de estacionarias ={first} e de não estacionarias ={second}".format(first = df_estac2.shape, second=df_n_estac2.shape))

    return df_estac2,  estac2, df_n_estac2, n_estac2;

def invert_diferenciacao(df_diferenciado, df_original):
  import pandas as pd
  import numpy as np
  from datetime import datetime
  from dateutil.relativedelta import relativedelta

  df_prev      = pd.DataFrame(df_diferenciado)
  primeiro_dia = datetime.strftime(df_prev.index.tolist()[0], '%Y-%m-%d')
  ultimo_dia   = datetime.strftime(df_prev.index.tolist()[-14], '%Y-%m-%d')
  ultimo_dia   = datetime.strptime(ultimo_dia, '%Y-%m-%d') + relativedelta(months=+11)

  dRan = pd.date_range(start =primeiro_dia, end = ultimo_dia, freq='MS')   
  res  = dRan.strftime('%Y/%m/%d')
 
  df_prev.reset_index(drop=True, inplace = True)
  df_prev.insert(1, "data", res)
  df_prev['data'] = pd.to_datetime(df_prev['data'])
  df_prev.set_index('data', inplace = True) 

  return (df_prev.iloc[0].replace(np.nan, 0).astype(int).add(df_original.shift().replace(np.nan, 0).astype(int), fill_value=0))


def invert_diferenciacao_treino(df_diferenciado, df_original):
  import pandas as pd
  import numpy as np

  return ((df_diferenciado + df_original).dropna())



