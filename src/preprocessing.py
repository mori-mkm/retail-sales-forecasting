# preprocessar o arquivo:
# tirar 2020 e lojas faltantes
# arrumar cabeçalhos e tamanho das fontes (limpeza)
# 1) verificar os que tem 36 meses e colocar num dataframe
#       (anos 2015 a 2017, inteiros)
# 2) verificar os que tem 24 meses e colocar em outro dataframe
#       (2 anos inteiros entre entre 2015 e 2017)
# 3) verificar quais tem 48 meses e colocar num dataframe
# 4) verificar quais tem 60 meses e colocar num dataframe

# Referências interessantes
# https://stackoverflow.com/questions/37901716/flask-uploads-ioerror-errno-2-no-such-file-or-directory


def pre_processing(local):

    import numpy as np                      # vectors and matrices
    import pandas as pd                     # tables and data manipulations

    #Importando os dados
    #arquivo = 'static/uploads/VendasBrutasNormalizadas_v5.csv' 
    df = pd.read_csv(local, parse_dates=['DATA']).sort_values (ascending = True, by = 'DATA')
    print("Dados importados")

    #Renomeando as colunas
    colunas = ["lojas", "orc_real", "periodo", "venda_bruta", "ano", "mes", "dia", "ano-mes", "data", 
            "codigo_loja", "nome_loja", "regional", "ggl", "gerente_n1", "gerente_n2", "cidade", "estado", "uf",
            "modelo", "desempenho", 'mape']

    df.columns = colunas

    # Aplicando o Lower case em todas as variaveis 
    df["lojas"]      = df["lojas"].str.lower()
    df["orc_real"]  = df["orc_real"].str.lower()
    df["nome_loja"] = df["nome_loja"].str.lower()
    df["regional"]  = df["regional"].str.lower()
    df["ggl"]       = df["ggl"].str.lower()
    df["gerente_n1"]= df["gerente_n1"].str.lower()
    df["gerente_n2"]= df["gerente_n2"].str.lower()
    df["cidade"]    = df["cidade"].str.lower()
    df["estado"]    = df["estado"].str.lower()
    df["uf"]        = df["uf"].str.lower()

    # Retirando os anos de 2020 e 2021 da nossa base de dados
    df = df.loc[df["ano"]<2020]

    # Selecionando somente as lojas que tenham realizado e variáveis não nulas
    df_realizado = df[df['orc_real'] == 'realizado'].drop('modelo', axis = 1).drop('desempenho', axis = 1).dropna()

    # Dropar os valores zeros
    df_realizado.drop(labels = df_realizado.loc[df_realizado['venda_bruta']==0].index.tolist(), axis= 0, inplace=True)

    #Transformando as datas em index
    df_realizado.set_index('data', inplace = True)

    print("Base de dados limpa")

    #Segmentando as lojas por quantidade de meses no historico
    df_lojas_meses = df_realizado.lojas.value_counts().rename_axis('lojas').reset_index(name='meses')

    df_60 = df_lojas_meses.loc[df_lojas_meses.meses ==60]
    df_48 = df_lojas_meses.loc[(df_lojas_meses.meses < 60) & (df_lojas_meses.meses >= 48)]
    df_36 = df_lojas_meses.loc[(df_lojas_meses.meses < 48) & (df_lojas_meses.meses >= 36)]
    df_24 = df_lojas_meses.loc[(df_lojas_meses.meses < 36) & (df_lojas_meses.meses >= 24)]

    # Arquivando os dataframes em uma lista
    arquivador_df = [df_60, df_48, df_36, df_24]


    # Colocando os nomes destas lojas em uma unica lista
    lojas_60 = df_60.lojas.tolist()
    lojas_48 = df_48.lojas.tolist()
    lojas_36 = df_36.lojas.tolist()
    lojas_24 = df_24.lojas.tolist()
    arquivador_lojas = [lojas_60, lojas_48, lojas_36, lojas_24]

    #Tratando esses nomes, onde tirmos os espaços e os traços

    for j in range(len(arquivador_df)):
        for i in range(len(arquivador_df[j])):  
            arquivador_df[j].iloc[i,0] = arquivador_df[j].iloc[i,0].replace(" ", "")
            arquivador_df[j].iloc[i,0] = arquivador_df[j].iloc[i,0].replace("-", "") 


    #Agora vamos coletar os dados de venda bruta de cada loja e acresentaremos esses valores em um dataframe
    arquivador_realizado = []

    for j in range(len(arquivador_lojas)):
        df_all = []
        
        for i in range(len(arquivador_lojas[j])):
            _ = df_realizado[df_realizado.lojas == arquivador_lojas[j][i]][['venda_bruta']]
            #_.reset_index(drop=True, inplace=True)
            _.columns = [arquivador_lojas[j][i]]
            df_all.append(_.copy())
        #Aqui nos vamos mudar os nomes das colunas por um quesito de estitica 
        arquivador_realizado.append(pd.concat(df_all, axis=1))
        arquivador_realizado[j].columns = arquivador_df[j].lojas.to_list()
        arquivador_df[j] = arquivador_df[j].lojas.to_list()
    print("Base segmentada")     
        
    return arquivador_realizado, arquivador_df , arquivador_lojas;


