# separação das séries em treino e teste
def split(serie, treino):
    tamanho = len(serie)
    tam_treino = int(round(tamanho*treino, 0)) 
    tam_teste  = int(tamanho - tam_treino)

    treino = serie.iloc[:tam_treino]
    teste  = serie.iloc[-tam_teste:]  
    return treino, teste