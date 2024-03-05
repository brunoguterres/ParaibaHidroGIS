def criar_campos(matriz):
    for linha in matriz:
        linha.append(0)
        linha.append(0)
        linha.append(0)
    return matriz

def calcular_balanco(matriz):
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == 'True':
            matriz[i][campo_vazao_jusante] = float(matriz[i][campo_disponibilidade])-float(matriz[i][campo_captacao])
        else:
            for j in range(i-1,-1,-1):
                contador_montante = 0
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus] :
                    matriz[i][campo_vazao_montante] += float(matriz[j][campo_vazao_jusante])
                    vazao_jusante = float(matriz[i][campo_vazao_montante])+float(matriz[i][campo_disponibilidade])-float(matriz[i][campo_captacao])
                    if vazao_jusante < 0:
                        matriz[i][campo_vazao_jusante] = 0
                        matriz[i][campo_deficit] = vazao_jusante*-1
                    else:
                        matriz[i][campo_vazao_jusante] = vazao_jusante
                    contador_montante += 1
                    if contador_montante == 2:
                        break
    return matriz

def print_matriz(matriz):
    for row in matriz:
        print(" ".join(map(str, row)))

def print_matriz_2(matriz):
    for row in matriz:
        for item in row:
            print(f"{item} ({type(item).__name__})", end=" ")
        print()

def criar_camada_resultado():
    query = '?query= SELECT camada_ottobacias.cobacia, camada_ottobacias.geometry FROM camada_ottobacias;'
    resultado_balanco = QgsVectorLayer(query, 'uniao_trecho_disp_cap', 'virtual')
    QgsProject.instance().addMapLayer(resultado_balanco)
    return resultado_balanco

### EXECUÇÃO ###

matriz = []
campos = trecho_disponibilidade_captacao.fields()
matriz.append([campo.name() for campo in campos])
for feicao in trecho_disponibilidade_captacao.getFeatures():
    matriz.append([feicao[campo.name()] for campo in campos])

matriz.pop(0)
matriz = criar_campos(matriz)

campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_cabeceira = 3
campo_disponibilidade = 4
campo_captacao = 5
campo_vazao_montante = 6
campo_vazao_jusante = 7
campo_deficit = 8

matriz_resultado = calcular_balanco(matriz)



print('--> Cálculo do balanço hídrico realizado.')






from qgis.core import QgsVectorLayer, QgsVectorDataProvider, QgsField, QgsFeature, QgsGeometry

# Suponha que você já tem uma camada de destino existente chamada "camada_destino"
# Se necessário, substitua "caminho_para_camada_destino" pelo caminho para a sua camada destino
caminho_para_camada_destino = "caminho_para_camada_destino"

# Carregue a camada destino existente
camada_destino = QgsVectorLayer(caminho_para_camada_destino, "nome_camada_destino", "ogr")

# Crie um provedor de dados para a camada destino
provedor_camada_destino = camada_destino.dataProvider()

# Suponha que você já tenha sua matriz de resultados
matriz_resultados = []

# Adicione os campos à camada destino, se necessário
campos = matriz_resultados[0]  # Os campos são a primeira linha da matriz
for nome_campo in campos:
    campo = QgsField(nome_campo, QVariant.String)  # Suponha que todos os campos sejam strings
    provedor_camada_destino.addAttributes([campo])

# Informe à camada destino para atualizar os campos
camada_destino.updateFields()

# Agora, vamos adicionar as feições à camada destino
# Suponha que cada linha da matriz, a partir da segunda, represente uma feição
for linha in matriz_resultados[1:]:
    # Crie uma feição
    feicao = QgsFeature()

    # Crie a geometria da feição, se necessário
    # Suponha que você tenha uma geometria específica para cada feição, como um ponto ou uma linha
    # Substitua QgsGeometry(QgsPoint(...)) pela sua geometria desejada
    geometria = QgsGeometry(QgsPoint(0, 0))  # Exemplo com ponto em (0, 0)
    feicao.setGeometry(geometria)

    # Adicione os atributos à feição
    for indice, valor in enumerate(linha):
        nome_campo = campos[indice]
        feicao.setAttribute(nome_campo, valor)

    # Adicione a feição à camada destino
    provedor_camada_destino.addFeatures([feicao])

# Informe ao QGIS que a camada destino foi alterada
camada_destino.updateExtents()

# Atualize a interface do usuário do QGIS
iface.layerTreeView().refreshLayerSymbology(camada_destino.id())
