# referencia util https://zetcode.com/python/flask/
# referencia boa de upload e download de arquivos
##################################################################
########## Importando as bibliotecas para aplicação ##############
from threading import Timer
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from src.pipeline import simulacao
import pandas as pd
from src.visualization import ver_GR_cth, graf_GR_cth, resumo_g_n1, resumo_g_n2, Conf_matrix, Acuracia_MC
import webbrowser
import warnings
warnings.filterwarnings("ignore")


##################################################################
###################### CODIGO FLASK ##############################
##################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever'


class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])


@app.route('/')
def index():
    return redirect(url_for('upload'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(f'static/uploads/{filename}')
        return redirect(url_for('uploaded'))

    return render_template('index.html', form=form)


#up_file = 'static/uploads/Dados_graficos_base_teste.csv'
# df_up = pd.read_csv(up_file)  # corrigir esse head


@app.route('/uploaded', methods=("POST", "GET"))
def uploaded():

    up_file = 'static/uploads/Dados_graficos_base_teste.csv'
    df_up = pd.read_csv(up_file)  # corrigir esse head

    return render_template('uploaded.html',
                           tables=[df_up.to_html(classes='data')],
                           titles=df_up.columns.values,
                           header="true", table_id="table")

####################################################
## Aqui temos que colocar os dados com as prediç ###
## retirar a importação de dados do visualização ###
####################################################


# print(nome_lojas_teste)
#print("acima é o teste do nome de lojas --------")

# Atualização dos gráficos
#tabela_GR19 = ver_GR_cth(2019)
#Graf_GR19 = graf_GR_cth(tabela_GR19, 2019)


#tabela_GR18 = ver_GR_cth(2018)
#Graf_GR18 = graf_GR_cth(tabela_GR19, 2018)
# print(tabela_GR18)
#print("tabela 18 acima ------------")
# print(tabela_GR19)
#print("tabela 19 acima ------------")

#fpg = 'static/uploads/Dados_graficos_base_teste.csv'
#fpg18 = pd.read_csv(fpg)
# fpg18 = fpg18[
#    (fpg18['ANO'] == 2018) &
#    (fpg18['MES'] == 12) &
#    (fpg18['ORC_REAL'] == 'PREDITO')]
#print("fpg 18 aqui embaixo----------")
# print(fpg18)
#print("len do df", len(fpg18))


#fpg = 'static/uploads/Dados_graficos_base_teste.csv'
#file_path_graf = pd.read_csv(fpg)

#tabela_GR19 = ver_GR_cth(2019)
#tabela19_g_n1 = resumo_g_n1(tabela_GR19)
#tabela19_g_n2 = resumo_g_n2(tabela_GR19)
# print(tabela_GR19)
#print("tabela gr19 acima-----")
# print(tabela19_g_n1)
#print("tabela g19 acima----")


#fpp = 'static/uploads/VendasBrutasBaseTeste.csv'
#file_path_preprocess = pd.read_csv(fpp)

#predicao_2019 = simulacao(file_path_preprocess, 2019)
# print(predicao_2019)


@app.route('/cockpit', methods=['GET'])
def cockpit():

    fpp = 'static/uploads/VendasBrutasBaseTeste.csv'
    file_path_preprocess = pd.read_csv(fpp)

    simulacao(file_path_preprocess, '2019')
    # print(predicao_2019)

    # Verificação se tem dados no ano
    fpg = 'static/uploads/Dados_graficos_base_teste.csv'
    file_path_graf = pd.read_csv(fpg)

    TabelaVazia = pd.DataFrame(columns=['Sem dados'], dtype=object)

    # Verificação se tem dados em 2018
    file_path_graf_2018 = file_path_graf[
        (file_path_graf['ANO'] == 2018) &
        (file_path_graf['MES'] == 12) &
        (file_path_graf['ORC_REAL'] == 'PREDITO')]

    if len(file_path_graf_2018) == 0:
        tabela_GR18 = TabelaVazia
        tabela18_g_n1 = TabelaVazia
        tabela18_g_n2 = TabelaVazia
        Imagem18 = 'static/downloads/vazio.jpg',
    else:
        tabela_GR18 = ver_GR_cth(2018)
        tabela18_g_n1 = resumo_g_n1(tabela_GR18)
        tabela18_g_n2 = resumo_g_n2(tabela_GR18)
        Imagem18 = 'static/downloads/graf_categ_gr2018.png',

    # print(tabela_GR18)

# Verificação se tem dados em 2019
    file_path_graf_2019 = file_path_graf[
        (file_path_graf['ANO'] == 2019) &
        (file_path_graf['MES'] == 12) &
        (file_path_graf['ORC_REAL'] == 'PREDITO')]

    if len(file_path_graf_2019) == 0:
        tabela_GR19 = TabelaVazia
        tabela19_g_n1 = TabelaVazia
        tabela19_g_n2 = TabelaVazia
        #Imagem19 = 'static/downloads/vazio.jpg',

    else:
        tabela_GR19 = ver_GR_cth(2019)
        tabela19_g_n1 = resumo_g_n1(tabela_GR19)
        tabela19_g_n2 = resumo_g_n2(tabela_GR19)
        #user_image19 = 'static/downloads/graf_categ_gr2019.png',

    return render_template('cockpit.html',
                           # user_image18=Imagem18,
                           # user_image19=Imagem19,
                           user_image19='static/downloads/graf_categ_gr2019.png',

                           tables18=[tabela_GR18.to_html(classes='data')],
                           titles18=tabela_GR18.columns.values,

                           tables18_n1=[tabela18_g_n1.to_html(classes='data')],
                           titles18_n1=tabela18_g_n1.columns.values,
                           tables18_n2=[tabela18_g_n2.to_html(classes='data')],
                           titles18_n2=tabela18_g_n2.columns.values,

                           tables19=[tabela_GR19.to_html(classes='data')],
                           titles19=tabela_GR19.columns.values,

                           tables19_n1=[tabela19_g_n1.to_html(classes='data')],
                           titles19_n1=tabela19_g_n1.columns.values,
                           tables19_n2=[tabela19_g_n2.to_html(classes='data')],
                           titles19_n2=tabela19_g_n2.columns.values,
                           header="true", table_id="table")


#tabela_GR19 = ver_GR_cth(2019)
#Graf_AC19 = graf_Accurac(tabela_GR19, 2019)
# print(Graf_AC19)

#tabela_MC19 = ver_GR_cth(2019)
# print(tabela_MC19)
#print("tabela mc19 acima -----------")
#Matriz_Confusao_2019 = Conf_matrix(tabela_MC19, 2019)


@app.route('/accuracy', methods=['GET'])
def accuracy():

    # Verificação se tem dados no ano
    fpg = 'static/uploads/Dados_graficos_base_teste.csv'
    file_path_graf = pd.read_csv(fpg)

    TabelaVazia = pd.DataFrame(columns=['Sem dados'], dtype=object)

    # Verificação se tem dados em 2018
    file_path_graf_2018 = file_path_graf[
        (file_path_graf['ANO'] == 2018) &
        (file_path_graf['MES'] == 12) &
        (file_path_graf['ORC_REAL'] == 'PREDITO')]

    if len(file_path_graf_2018) == 0:
        tabela_MC18 = TabelaVazia
        acuracia_modelo_18 = ""
        ImagemMC18 = 'static/downloads/vazio.jpg',
    else:
        tabela_MC18 = ver_GR_cth(2018)
        Matriz_Confusao_18 = Conf_matrix(tabela_MC18, 2018)
        acuracia_modelo_18 = "A acurácia do modelo é " + \
            str(Acuracia_MC(tabela_MC18, 2018)) + " %"
        ImagemMC18 = 'static/downloads/MatConfDez2018.png',

    # Verificação se tem dados em 2019
    file_path_graf_2019 = file_path_graf[
        (file_path_graf['ANO'] == 2019) &
        (file_path_graf['MES'] == 12) &
        (file_path_graf['ORC_REAL'] == 'PREDITO')]

    if len(file_path_graf_2019) == 0:
        tabela_MC19 = TabelaVazia
        acuracia_modelo_19 = ""
        ImagemMC19 = 'static/downloads/vazio.jpg',
    else:
        tabela_MC19 = ver_GR_cth(2019)
        Matriz_Confusao_19 = Conf_matrix(tabela_MC19, 2019)
        acuracia_modelo_19 = "A acurácia do modelo é " + \
            str(Acuracia_MC(tabela_MC19, 2019)) + " %"
        ImagemMC19 = 'static/downloads/MatConfDez2019.png',

    return render_template('accuracy.html',
                           # user_image18=Imagem18,
                           # user_image19=Imagem19,
                           user_imageMC18='static/downloads/MatConfDez2018.png',
                           user_imageMC19='static/downloads/MatConfDez2019.png',


                           ac_model_18=acuracia_modelo_18,
                           ac_model_19=acuracia_modelo_19,

                           header="true", table_id="table")


#filepath = 'static/uploads/Dados_graficos_base_teste.csv'
#arquivo = pd.read_csv(filepath)
#ano = 2019
#arquivo_ano = arquivo[(arquivo['ANO'] == ano) & (arquivo['MES'] == 12)]
#nome_lojas = arquivo_ano.NOME_LOJA_COMPLETO.unique()
# print(arquivo)
#print("arquivo acima-----")

#dados = ver_GR_cth(2019)
# print(dados)
#print("dados gr acima ------------")

#acuracia_modelo = Acuracia_MC(dados, 2019)
#print("acuracia do modelo", acuracia_modelo)

#tabela_GR19 = ver_GR_cth(2019)
#Matriz_Confusao = Conf_matrix(tabela_GR19, 2019)
# print(Matriz_Confusao)
# print(tabela_GR19)
#print("tabela 19 acima-----")


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run()
