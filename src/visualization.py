# Referencia
# https://www.youtube.com/watch?v=Ra50xHZnCkY&ab_channel=UpCursoseTreinamentosOnline
# https://paulovasconcellos.com.br/15-comandos-de-matplotlib-que-talvez-voc%C3%AA-n%C3%A3o-conhe%C3%A7a-17cf88a75119
# o grafico acima são referencias de graficos legais em panda
import pandas as pd



def ver_GR_cth(ano):

    import pandas as pd

    filepath = 'static/uploads/Dados_graficos_base_teste.csv'
    arquivo = pd.read_csv(filepath)

    # ano = "{}-12".format(ano) *** ALTEREI AQUI POR CONTA DO QUE SAIU DO DATAFRAME
    arquivo_ano = arquivo[(arquivo['ANO'] == ano) & (arquivo['MES'] == 12)]
    nome_lojas = arquivo_ano.NOME_LOJA_COMPLETO.unique()

    colunas = ['Nome_Loja', 'Gerente_N1',
               'Gerente_N2', 'GR_real_%', 'Categ_GR_real',
               'GR_pred_%', 'Catg_GR_pred']

    # tem que incluir o dtype senão da problema
    Dados_GR = pd.DataFrame(columns=colunas, dtype=object)

    for lj in nome_lojas:

        # puxando os nomes dos gerentes nivel 1
        gerente_n1 = arquivo_ano[(arquivo_ano['ORC_REAL'] == 'PREDITO') & (
            arquivo_ano['NOME_LOJA_COMPLETO'] == lj)]['GERENTE_N1'].values[0]
        # puxando os nomes dos gerentes nivel 2
        gerente_n2 = arquivo_ano[(arquivo_ano['ORC_REAL'] == 'ORCADO') & (
            arquivo['NOME_LOJA_COMPLETO'] == lj)]['GERENTE_N2'].values[0]

        ##################################################
        ### Calcular o acumulado do predito e orçado #####
        ##################################################

        # CÁLCULO DO GR
        # puxando os dados de predito
        pred_lj_dez = arquivo_ano[(arquivo_ano['ORC_REAL'] == 'PREDITO') & (
            arquivo_ano['NOME_LOJA_COMPLETO'] == lj)]['VENDA_BRUTA'].values[0]
        # puxando os dados de planejado
        plan_lj_dez = arquivo_ano[(arquivo_ano['ORC_REAL'] == 'ORCADO') & (
            arquivo['NOME_LOJA_COMPLETO'] == lj)]['VENDA_BRUTA'].values[0]
        # puxando os dados de planejado
        real_lj_dez = arquivo_ano[(arquivo_ano['ORC_REAL'] == 'REALIZADO') & (
            arquivo['NOME_LOJA_COMPLETO'] == lj)]['VENDA_BRUTA'].values[0]

        # calculando o GR predito
        GR_pred_lj = round((pred_lj_dez / plan_lj_dez)*100, 2)

        # Identificando a categoria do GR Predito
        if GR_pred_lj >= 100:
            Catg_GR_pred_lj = "Alta probabilidade (>=100%)"

        elif GR_pred_lj <= 85:
            Catg_GR_pred_lj = "Baixa probabilidade (<85%)"

        else:
            Catg_GR_pred_lj = "Média probabilidade (85%>=P<100%)"

        # calculando o GR realizado
        GR_real_lj = round((real_lj_dez / plan_lj_dez)*100, 2)

        # Identificando a categoria do GR realizado
        if GR_real_lj >= 100:
            Catg_GR_real_lj = "Alta probabilidade (>=100%)"

        elif GR_real_lj <= 85:
            Catg_GR_real_lj = "Baixa probabilidade (<85%)"

        else:
            Catg_GR_real_lj = "Média probabilidade (85%>=P<100%)"

        to_append = [lj, gerente_n1, gerente_n2, GR_real_lj,
                     Catg_GR_real_lj, GR_pred_lj, Catg_GR_pred_lj]

        Dados_GR = Dados_GR.append(pd.DataFrame(
            [to_append], columns=colunas)).reset_index(drop=True)
        Dados_GR = Dados_GR.drop_duplicates()
    print(Dados_GR)
    print("acima dados de gr----------")

    return Dados_GR


def resumo_g_n1(Dados_GR):

    import pandas as pd
    gerentes_n1 = Dados_GR.Gerente_N1.unique()

    Dados_status_n1 = pd.DataFrame(
        columns=["Gerente_N1", "Status_N1_%"], dtype=object)

    for ger in gerentes_n1:
        baixa_n1 = Dados_GR.loc[(Dados_GR.Categ_GR_real == 'Baixa probabilidade (<85%)') &
                                (Dados_GR.Gerente_N1 == ger), "Gerente_N1"].count()
        n_lojas1 = Dados_GR.loc[Dados_GR["Gerente_N1"]
                                == ger, "Gerente_N1"].count()

        status_n1 = round((baixa_n1/n_lojas1)*100, 2)

        to_append = [ger, status_n1]

        Dados_status_n1 = Dados_status_n1.append(pd.DataFrame(
            [to_append], columns=["Gerente_N1", "Status_N1_%"])).reset_index(drop=True)
    return Dados_status_n1


def resumo_g_n2(Dados_GR):
    import pandas as pd
    gerentes_n2 = Dados_GR.Gerente_N2.unique()

    Dados_status_n2 = pd.DataFrame(
        columns=["Gerente_N2", "Status_N2_%"], dtype=object)

    for ger in gerentes_n2:
        baixa_n2 = Dados_GR.loc[(Dados_GR.Categ_GR_real == 'Baixa probabilidade (<85%)') &
                                (Dados_GR.Gerente_N2 == ger), "Gerente_N2"].count()
        n_lojas2 = Dados_GR.loc[Dados_GR.Gerente_N2 ==
                                ger, "Gerente_N2"].count()

        status_n2 = round((baixa_n2/n_lojas2)*100, 2)

        to_append = [ger, status_n2]

        Dados_status_n2 = Dados_status_n2.append(pd.DataFrame(
            [to_append], columns=["Gerente_N2", "Status_N2_%"])).reset_index(drop=True)
    return Dados_status_n2


def graf_GR_cth(Dados_GR, ano):
    import matplotlib.pyplot as plt
    # CRIANDO O GRÁFICO
    # selecionando só a coluna 'Categ_GR_real'
    Dados_GR_real_calculo = Dados_GR['Categ_GR_real']

    # contando os dados de alta probabilidade
    alta_prob = Dados_GR_real_calculo[Dados_GR_real_calculo ==
                                      'Alta probabilidade (>=100%)'].count()

    # contando os dados de média probabilidade
    media_prob = Dados_GR_real_calculo[Dados_GR_real_calculo ==
                                       'Média probabilidade (85%>=P<100%)'].count()

    # contando os dados de baixa probabilidade
    baixa_prob = Dados_GR_real_calculo[Dados_GR_real_calculo ==
                                       'Baixa probabilidade (<85%)'].count()

    # Pie chart
    labels = 'Alta Prob. (>=100%)', 'Média Prob. (85%>=P<100%)', 'Baixa Prob. (<85%)'
    sizes = [alta_prob, media_prob, baixa_prob]
    explode = (0, 0, 0.2)
    plt.rcParams['figure.figsize'] = (30, 10)
    plt.legend(labels, loc='best')
    plt.rc('font', size=20)
    plt.title('Distribuição das categorias de GR')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')

    fig = plt.gcf()
    # plt.show()
    fig.savefig('static/downloads/graf_categ_gr{}.png'.format(ano),
                format='png', transparent=False)
    return


def Conf_matrix(Dados_GR, ano):
    import numpy as np
    import pandas as pd
    import seaborn as sn
    import matplotlib.pyplot as plt
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix

    y_true = Dados_GR['Categ_GR_real']
    y_pred = Dados_GR['Catg_GR_pred']
    data_confmat = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(data_confmat, columns=np.unique(
        y_true), index=np.unique(y_true))
    df_cm.index.name = 'Realizado'
    df_cm.columns.name = 'Predito'
    plt.figure(figsize=(40, 10))
    plt.title('Matriz de confusão', fontsize=24, )
    sn.set(font_scale=1.4)  # for label size
    sn.heatmap(df_cm, cmap="Blues", annot=True,
               annot_kws={"size": 20})  # font size

    fig = plt.gcf()
    # plt.show()
    fig.savefig('static/downloads/MatConfDez{}.png'.format(ano),
                format='png', transparent=False)

    return


def Acuracia_MC(Dados_GR, ano):
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    Res_mat_conf_ano = Dados_GR[['Categ_GR_real', 'Catg_GR_pred']]
    accu_ano = accuracy_score(
        Res_mat_conf_ano['Categ_GR_real'], Res_mat_conf_ano['Catg_GR_pred'])
    Acuracia_Ano = round(accu_ano*100, 2)
    #print("acuracia do ano ", Acuracia_Ano)
    return Acuracia_Ano
