import pandas as pd

# Carregar a camada de pontos de monitoramento
pontos_monitoramento = QgsProject.instance().mapLayersByName('intersecao_pontos_monitoramento_ottobacias')[0]

dados = []

# Iterar sobre os pontos de monitoramento
for ponto in pontos_monitoramento.getFeatures():
    cod_otto = ponto['cobacia']
    id = ponto['fid']
    
    # Determinar o código otto adequado
    if (int(cod_otto) % 2) == 0:
        cod_otto_e = cod_otto
    else:
        for letra in range(len(cod_otto)):
            index = (letra + 1) * -1
            conv_num = int(cod_otto[index])
            resto = conv_num % 2        
            if resto == 0:
                cod_otto_e = cod_otto[:(index + 1)]
                break

    # Montar a consulta SQL
    sql = f'''
            SELECT COUNT(NumProcess) AS numero_outorgas, SUM(volume_anual) AS volume_anual
            FROM intersecao_outorgas_usuarios_ottobacias
            WHERE cobacia LIKE '{cod_otto_e}%' AND cobacia >= '{cod_otto}';
            '''
    
    # Criar a camada virtual
    camada_virtual = QgsVectorLayer("?query={}".format(sql), "selecao_montante_outorgas_" + str(cod_otto), "virtual")
    
    # Verificar se a camada virtual foi criada com sucesso
    if not camada_virtual.isValid():
        print(f"Falha ao criar camada virtual para o código otto: {cod_otto}")
        continue

    # Obter os resultados da camada virtual
    features = camada_virtual.getFeatures()
    for feature in features:
        numero_outorgas = feature['numero_outorgas']
        volume_anual = feature['volume_anual']
        dados.append([id, cod_otto, numero_outorgas, volume_anual])

# Converter os dados para um DataFrame do pandas
df = pd.DataFrame(dados, columns=['id_ponto_monit', 'cod_otto', 'numero_outorgas', 'volume_anual'])

# Salvar o DataFrame em um arquivo Excel
df.to_excel('C:/Users/brunoguterres/Desktop/analises_william/resultados/outorgas_usuarios/outorgas_usuarios_montante.xlsx', index=False)

print('OPERAÇÃO FINALIZADA!!!')

# Atualizar o canvas do mapa
iface.mapCanvas().refresh()
