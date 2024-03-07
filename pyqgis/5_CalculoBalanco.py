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

def criar_camada_resultado():
    query = '?query= SELECT camada_ottobacias.cobacia, camada_ottobacias.geometry FROM camada_ottobacias;'
    resultado_balanco = QgsVectorLayer(query, 'resultado_balanco', 'virtual')
    QgsProject.instance().addMapLayer(resultado_balanco)
    return resultado_balanco

def criar_camada_resultado():
    #MUDAR PARA CRIAÇÃO DE UMA CAMADA TEMPORÁRIA.
    query = '?query= SELECT camada_ottobacias.geometry, '\
                           'camada_ottobacias.cobacia '\
                     'FROM camada_ottobacias;'
    camada_resultado = QgsVectorLayer(query, 'resultado_balanco', 'virtual')
    resultado_balanco = editar_camada_resultado(camada_resultado)
    return resultado_balanco

def editar_camada_resultado(camada_edicao):
    provedor = camada_edicao.dataProvider()
    campos = [('cobacia', QVariant.String),
              ('cotrecho', QVariant.String),
              ('trechojus', QVariant.String),
              ('cabeceira', QVariant.String),
              ('disponibilidade', QVariant.Double),
              ('captacao', QVariant.Double),
              ('vazao_montante', QVariant.Double),
              ('vazao_jusante', QVariant.Double),
              ('deficit',QVariant.Double)]
    
    for nome_campo, tipo_campo in campos:
        campo = QgsField(nome_campo, tipo_campo)
        provedor.addAttributes([campo])
    
    camada_edicao.updateFields()
    return camada_edicao

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

matriz_balanco = calcular_balanco(matriz)
resultado_balanco = criar_camada_resultado()
QgsProject.instance().addMapLayer(resultado_balanco)

print('--> Cálculo do balanço hídrico realizado.')






'''
# Crie um provedor de dados para a camada destino
provedor_camada_destino = camada_destino.dataProvider()

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
'''