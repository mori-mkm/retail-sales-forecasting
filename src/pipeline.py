##################################################################
###############  Importando as nossas bibliotecas  ###############
def simulacao(local, datas):
    from src.preprocessing import pre_processing
    from src.stationarity import teste_estacionaridade
    from src.differencing import diferenciacao, invert_diferenciacao, invert_diferenciacao_treino
    from src.forecasting import forecast
    from src.validation import acuracia, rmse, mape
    from src.train_test_split import split
    ##################################################################
    ######### Importando bibliotecas de tratamento de dados ##########
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import warnings
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    warnings.filterwarnings("ignore")

    ###################################################################################
    ############ Iniciando o préprocessamento dos dados ###############################
    print('')
    print('')
    print('############ Iniciando o préprocessamento dos dados #############################')

    arquivador_realizado, arquivador_df, arquivador_lojas = pre_processing(local)

    ###################################################################################
    ########### Visualização das lojas ##############
    plt.figure(figsize=(18, 4))
    for n in range(len(arquivador_realizado)):
        for loja in arquivador_realizado[n]:
            plt.plot(arquivador_realizado[n][loja],
                    label='loja {}'.format(loja[:4]))
    fig = plt.gcf()
    plt.legend()
    fig.savefig('static/downloads/todas_lojas.png',
                format='png', transparent=False)


    ###################################################################################
    ######### Sinalizando quais dessas lojas já são estacionárias ou não ##############
    print('')
    print('')
    print('######### Sinalizando quais dessas lojas já são estacionárias ou não ############')

    estac = [0, 0, 0, 0]
    n_estac = [0, 0, 0, 0]

    for i in range(len(arquivador_realizado)):
        estac[i], n_estac[i] = teste_estacionaridade(
            arquivador_realizado[i], arquivador_df[i])

    ###################################################################################
    ############ Diferenciando as series nao estacionarias [1ª tentativa] #############
    print('')
    print('')
    print('############ Diferenciando as series nao estacionarias [1ª tentativa] ###########')

    df_estac2 = [0, 0, 0, 0]
    estac2 = [0, 0, 0, 0]
    df_n_estac_2 = [0, 0, 0, 0]
    n_estac2 = [0, 0, 0, 0]

    for i in range(len(arquivador_realizado)):
        df_estac2[i],  estac2[i], df_n_estac_2[i], n_estac2[i] = diferenciacao(
            arquivador_realizado[i])

    ###################################################################################
    ############ Diferenciando as series nao estacionarias [2ª tentativa] #############
    print('')
    print('')
    print('############ Diferenciando as series nao estacionarias [2ª tentativa] ###########')

    df_estac3 = [0, 0, 0, 0]
    estac3 = [0, 0, 0, 0]
    df_n_estac3 = [0, 0, 0, 0]
    n_estac3 = [0, 0, 0, 0]

    for i in range(len(arquivador_realizado)):
        if len(n_estac2[i]) > 0:
            df_estac3[i],  estac3[i], df_n_estac3[i], n_estac3[i] = diferenciacao(
                df_n_estac_2[i])

    ###################################################################################
    ################## Separação de treino e teste ###################################
    print('')
    print('')
    print('################## Separação de treino e teste #################################')

    arquivador_treino = [0, 0, 0, 0]
    arquivador_teste = [0, 0, 0, 0]
    lojas_ = [0, 0, 0, 0]

    for i in range(len(arquivador_realizado)):
        if estac3[i] != 0:
            lojas_[i] = list(set(estac3[i]) | set(estac2[i]))
            arquivador_treino[i] = pd.DataFrame(columns=lojas_[i])
            arquivador_teste[i] = pd.DataFrame(columns=lojas_[i])
            for loja in lojas_[i]:
                try:
                    arquivador_treino[i][loja], arquivador_teste[i][loja] = split(
                        df_estac3[i][loja], 0.8)
                except:
                    arquivador_treino[i][loja], arquivador_teste[i][loja] = split(
                        df_estac2[i][loja], 0.8)

        else:
            lojas_[i] = estac2[i]
            arquivador_treino[i] = pd.DataFrame(columns=lojas_[i])
            arquivador_teste[i] = pd.DataFrame(columns=lojas_[i])
            for loja in lojas_[i]:
                arquivador_treino[i][loja], arquivador_teste[i][loja] = split(
                    df_estac2[i][loja], 0.8)

        arquivador_treino[i].to_csv('static/downloads/treino{}.txt'.format(i), index=True, header=lojas_[i])

    ###################################################################################
    ################## Modelo de predição SARIMAX #####################################
    print('')
    print('')
    print('################## Modelo de predição SARIMAX ###################################')
    arquivador_previsao = [0, 0, 0, 0]

    for i in range(len(arquivador_realizado)):
        arquivador_previsao[i] = pd.DataFrame(columns=lojas_[i])
        for loja in lojas_[i]:
            arquivador_previsao[i][loja] = forecast(arquivador_treino[i][loja])

        arquivador_previsao[i].to_csv('static/downloads/previsao{}.txt'.format(i), index=True, header=lojas_[i])

    ###################################################################################
    ############# Retornando a série ao estado original ###############################
    print('')
    print('')
    print('############# Retornando a série ao estado original #############################')
    arquivador_previsao_ = arquivador_previsao

    arquivador_tam = [0, 0, 0, 0]
    for n in range(len(arquivador_realizado)):
        tam_treino = []
        for loja in arquivador_previsao_[n]:
            tam_treino.append(len(arquivador_realizado[n][loja].dropna()))
        arquivador_tam[n] = tam_treino
        arquivador_tam[n] = max(arquivador_tam[n])
        arquivador_tam[n] = arquivador_tam[n]-1

    arquivador_realizado, arquivador_df, arquivador_lojas = pre_processing()

    for n in range(len(arquivador_realizado)):
        for loja in arquivador_previsao_[n]:

            df_prev = pd.DataFrame(arquivador_previsao_[n][loja])

            primeiro_dia = datetime.strftime(
                arquivador_teste[n][loja].index.tolist()[0], '%Y-%m-%d')
            primeiro_dia = datetime.strptime(
                primeiro_dia, '%Y-%m-%d') - relativedelta(months=1)
            ultimo_dia = datetime.strftime(
                arquivador_teste[n][loja]['2019'].index.tolist()[-1], '%Y-%m-%d')

            df_prev = df_prev[primeiro_dia:ultimo_dia].replace(
                np.nan, 0).astype(int)
            antiga = arquivador_realizado[n][loja][primeiro_dia:ultimo_dia].shift(
            ).replace(np.nan, 0).astype(int)

            if len(arquivador_treino[n][loja].dropna()) == arquivador_tam[n]:

                arquivador_previsao_[n][loja] = df_prev.add(antiga, axis=0)
            else:
                arquivador_previsao_[n][loja] = df_prev.add(antiga, axis=0)
                arquivador_previsao_[n][loja] = df_prev.add(antiga, axis=0)

        arquivador_previsao_[i].to_csv(
            'static/downloads/predicao{}.txt'.format(n), index=True, header=lojas_[i])

    ###################################################################################
    ######### Retornando os valores preditos ao DF original ###########################
    print('')
    print('')
    print('######### Retornando os valores preditos ao DF original #########################')
    # Importando o df original
    original = pd.read_csv('static/uploads/VendasBrutasBaseTeste.csv',
                        parse_dates=['DATA']).sort_values(ascending=True, by='DATA')



    arq_projecao = arquivador_previsao_

    for i in range(len(arquivador_previsao_)):
        arq_projecao[i].reset_index(inplace=True)
        arq_projecao[i].rename({'index': 'data'}, axis='columns', inplace=True)
        arq_projecao[i] = pd.melt(arq_projecao[i], id_vars='data',
                                value_vars=arq_projecao[i].columns.tolist()[1:], value_name='predicao')
        arq_projecao[i] = arq_projecao[i][arq_projecao[i]['data'].dt.strftime('%Y') > datas]
        arq_projecao[i].reset_index(inplace=True, drop=True)

    original['id'] = original["NOME_LOJA_COMPLETO"].str.lower()

    for i in range(len(original.NOME_LOJA_COMPLETO)):
        original.id[i] = original['id'][i].replace(" ", "")
        original.id[i] = original['id'][i].replace("-", "")

    # Criando um dicionário com as principais informações do dataframe original
    original_dict = original[['NOME_LOJA_COMPLETO', 'CODIGO_LOJA', 'NOME_LOJA', 'REGIONAL',
                            'GGL', 'GERENTE_N1', 'GERENTE_N2', 'CIDADE', 'ESTADO', 'UF',  'id']].to_dict('records')

    res_list = []
    for i in range(len(original_dict)):
        if original_dict[i] not in original_dict[i + 1:]:
            res_list.append(original_dict[i])

    # Criando um looping de iterações para que cada Id com sua respctiva data tenha uma linha no df novo com as  informações faltantes
    dados_graficos = original
    for n in range(len(arquivador_previsao_)):

        row_df = pd.DataFrame([])

        for j in range(len(arquivador_previsao_[n])):

            for i in range(len(res_list)):

                if (arq_projecao[n].iloc[j, 1] == res_list[i]['id']):

                    row = pd.Series([arquivador_previsao_[n].iloc[j, 0], arquivador_previsao_[n].iloc[j, 1], arquivador_previsao_[n].iloc[j, 2], res_list[i]['NOME_LOJA_COMPLETO'], res_list[i]
                                    ['CODIGO_LOJA'], res_list[i]['REGIONAL'], res_list[i]['GGL'], res_list[i]['GERENTE_N1'], res_list[i]['GERENTE_N2'], res_list[i]['CIDADE'], res_list[i]['ESTADO'], res_list[i]['UF']])

                    row_df = row_df.append(row, ignore_index=True)

        row_df.columns = ['data', 'variable', 'predicao', 'NOME_LOJA_COMPLETO', 'CODIGO_LOJA',
                        'REGIONAL', 'GGL', 'GERENTE_N1', 'GERENTE_N2',  'CIDADE', 'ESTADO', 'UF']

        to_apend = row_df

        # Dropando as colunas não necessárias
        to_apend = to_apend.drop(['variable'], axis=1)

        # Renomeando as colunas no dataframe a ser apendado
        to_apend.rename(
            columns={'data': 'DATA', 'predicao': 'VENDA_BRUTA'}, inplace=True)

        # Criando um dataframe com o nome das colunas do dataframe original
        colunas = original.columns

        # Inserindo as colunas faltantes para ficar igual ao dataframe original

        to_apend['ORC_REAL'] = 'PREDITO'
        to_apend['PERIODO'] = 'tbd'
        to_apend['ANO'] = to_apend['DATA'].dt.year
        to_apend['MES'] = to_apend['DATA'].dt.month
        to_apend['DIA'] = to_apend['DATA'].dt.day
        to_apend['ANO-MES'] = 'tbd'
        to_apend['NOME_LOJA'] = to_apend['NOME_LOJA_COMPLETO']
        to_apend['MODELO'] = 'tbd'
        to_apend['DESEMPENHO'] = 'tbd'

        to_apend = to_apend.reindex(columns=colunas)

        dados_graficos = pd.concat([dados_graficos, to_apend])

    ###################################################################################
    ################### Calcula da erro do modelo #####################################
    print('')
    print('')
    print('################### Calcula da erro do modelo ###################################')

    lojas_pred = dados_graficos.loc[(
        dados_graficos.ORC_REAL == 'PREDITO', 'NOME_LOJA_COMPLETO')].unique()

    arquivador_acu = pd.DataFrame(
        columns=['ERRO', 'MAE', 'MFE', 'MSE', 'RMSE', 'MAPE'])

    for loja in lojas_pred:
        orcado = dados_graficos.loc[(dados_graficos.NOME_LOJA_COMPLETO == loja) & (
            dados_graficos.ORC_REAL == "ORCADO")][['DATA', 'VENDA_BRUTA', 'NOME_LOJA_COMPLETO']].set_index('DATA')

        predito = dados_graficos.loc[(dados_graficos.NOME_LOJA_COMPLETO == loja) & (dados_graficos.ORC_REAL == "PREDITO")][[
            'DATA', 'VENDA_BRUTA', 'NOME_LOJA_COMPLETO']].set_index('DATA').dropna()
        fodase = acuracia(orcado.VENDA_BRUTA, predito.VENDA_BRUTA)
        fodase.drop(columns=['Métricas'], inplace=True)
        fodase = fodase.T
        fodase.columns = ['ERRO', 'MAE', 'MFE', 'MSE', 'RMSE', 'MAPE']
        fodase.reset_index(drop=True, inplace=True)
        fodase['NOME_LOJA_COMPLETO'] = orcado.NOME_LOJA_COMPLETO.drop_duplicates(
        ).reset_index(drop=True)
        arquivador_acu = pd.concat([arquivador_acu, fodase])
    arquivador_acu.reset_index(drop=True, inplace=True)
    arquivador_acu.to_csv('static/downloads/erros.csv')

    dados_graficos = pd.merge(left=dados_graficos, right=arquivador_acu[[
                            'MAPE', 'NOME_LOJA_COMPLETO']], how='left', left_on='NOME_LOJA_COMPLETO', right_on='NOME_LOJA_COMPLETO')

    ###################################################################################
    ###################  SALVANDO AS PREVISOES ########################################
    print('')
    print('')
    print('###################  SALVANDO AS PREVISOES #####################################')
    dados_graficos.drop(columns='id', inplace=True)
    dados_graficos.to_csv('static/uploads/Dados_graficos_base_teste.csv',index=False )

    return;
