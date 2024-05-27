import psycopg2


def carregar_camada(camada, simbologia):
    tipo_geometria = camada.geometryType()
    if tipo_geometria == QgsWkbTypes.PointGeometry:
        symbol = QgsSimpleMarkerSymbolLayer.create({
            'color': simbologia['cor'],
            'size': simbologia['tamanho']
        })
    elif tipo_geometria == QgsWkbTypes.LineGeometry:
        symbol = QgsLineSymbol.createSimple({
            'color': simbologia['cor'],
            'width': simbologia['espessura']
        })
    elif tipo_geometria == QgsWkbTypes.PolygonGeometry:
        symbol = QgsFillSymbol.createSimple({
            'color': simbologia['cor_preenchimento'],
            'color_border': simbologia['cor_contorno'],
            'width_border': simbologia['espessura_contorno']
        })
    renderer = QgsSingleSymbolRenderer(symbol)
    camada.setRenderer(renderer)
    QgsProject.instance().addMapLayer(camada)
    print(f'--> Carregamento de "{camada.name()}" realizado.')


### EXECUÇÃO ###

conexao = psycopg2.connect(
dbname = str(parametros_conexao['nome_bd']),
user = str(parametros_conexao['usuario_bd']),
password = str(parametros_conexao['senha_bd']),
host = str(parametros_conexao['host_bd']),
port = str(parametros_conexao['porta_bd']))
cursor = conexao.cursor()

cursor.execute(f'''SELECT cobacia FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
cod_otto_bacia = cursor.fetchone()[0]

if QgsProject.instance().mapLayersByName('camada_ottotrechos'):
    ottotrechos = QgsProject.instance().mapLayersByName('camada_ottotrechos')[0]
    print(f'--> Camada {ottotrechos.name()} existe!!!')
    #QgsProject.instance().removeMapLayer(ottotrechos)
    #print('--> Camada "camada_ottotrechos" REMOVIDA.')

if (int(cod_otto_bacia) % 2) == 0:
    cod_otto_e = cod_otto_bacia
else:
    for letra in range(len(cod_otto_bacia)):
        index = (letra + 1) * -1
        conv_num = int(cod_otto_bacia[index])
        resto = conv_num % 2
        if resto == 0:
            cod_otto_e = cod_otto_bacia[:(index + 1)]
            break

cursor.execute(f'''
    DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottobacias_isr_montante CASCADE;
    CREATE VIEW {parametros_conexao['schema_cenario']}.ottobacias_isr_montante AS
    SELECT *
    FROM {parametros_conexao['schema_cenario']}.ottobacias_isr
    WHERE {parametros_conexao['schema_cenario']}.ottobacias_isr.cobacia LIKE '{cod_otto_e}%' AND ottobacias_isr.cobacia >= '{cod_otto_bacia}';
''')
conexao.commit()



cursor.execute(f'''
    DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.bacia_montante CASCADE;
    CREATE VIEW {parametros_conexao['schema_cenario']}.bacia_montante AS
    SELECT ST_UNION(geom) as geom
    FROM {parametros_conexao['schema_cenario']}.ottobacias_isr_montante;
''')
conexao.commit()
cursor.close()
conexao.close()


# solução provisória
uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                    parametros_conexao['porta_bd'],
                    parametros_conexao['nome_bd'],
                    parametros_conexao['usuario_bd'],
                    parametros_conexao['senha_bd'])
uri.setDataSource(parametros_conexao['schema_cenario'], 'ottobacias_isr_montante', 'geom', '', 'cobacia')
ottobacias_isr_montante = QgsVectorLayer(uri.uri(False), 'camada_ottobacias_isr_montante', 'postgres')
QgsProject.instance().addMapLayer(ottobacias_isr_montante)
simbologia_ottobacias_isr_montante = {'cor_preenchimento': QColor(0, 0, 0, 0),
                                        'cor_contorno': QColor(0, 0, 0, 0),
                                        'espessura_contorno': 1}
carregar_camada(ottobacias_isr_montante, simbologia_ottobacias_isr_montante)
print(f'--> Importação da camada "{ottobacias_isr_montante.name()}" realizada.')

bacia_montante = QgsVectorLayer(f'''VirtualLayer?query=
                                    SELECT ST_UNION(geometry)
                                    FROM camada_ottobacias_isr_montante''',
                                'camada_bacia_montante',
                                'virtual')

# inicio da plotagem do trecho de jusante - apenas o jusante 1 no estilo antigo
# calculo dos rios que estão a jusante
# variáveis para o trecho de jusante - estão sendo definidas aqui para não dar erro
rio = ['','','','','','']
rios = 0
compri= 4
# seleção dos rios a jusante
for valor in range(len(cod_otto_bacia)):
    index = (valor + 1) * -1
    algarismo = int(cod_otto_bacia[index])
    impar = algarismo % 2
    codf = cod_otto_bacia[:(len(cod_otto_bacia)-valor)]
    if impar == 0:
        codfim = cod_otto_bacia[:(len(cod_otto_bacia)-valor)]
        rio[rios] = codfim
        rios = rios + 1
        compri = len(codfim)
# adição do shape do trechos de jusante
selecao = ""
for elementos in rio:
    if elementos != '':
        selecao = selecao + "camada_ottotrechos.curso_dagua LIKE '"+ elementos +"' OR "
    else:
        break
comp = len(selecao)
comp2 = comp - 3
sele2 = selecao [:comp2]

ottotrechos_jusante = QgsVectorLayer(f'''VirtualLayer?query=
                                            SELECT
                                                camada_ottotrechos.cobacia,
                                                camada_ottotrechos.curso_dagua,
                                                camada_ottotrechos.nome_rio,
                                                camada_ottotrechos.geometry
                                            FROM camada_ottotrechos
                                            WHERE ({sele2}) AND camada_ottotrechos.cobacia < '{cod_otto_bacia}';''',
                                        'camada_ottotrechos_jusante',
                                        'virtual')

ottotrechos_jusante_2 = QgsVectorLayer(f'''VirtualLayer?query=
                                            SELECT
                                                camada_ottotrechos.cobacia,
                                                camada_ottotrechos.curso_dagua,
                                                camada_ottotrechos.nome_rio,
                                                camada_ottotrechos.geometry
                                            FROM camada_ottotrechos
                                            WHERE ({sele2}) AND camada_ottotrechos.cobacia >= '{cod_otto_bacia}';''',
                                        'camada_ottotrechos_jusante_2',
                                        'virtual')

if QgsProject.instance().mapLayersByName('camada_bacia_montante'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_bacia_montante')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
simbologia_bacia_montante = {'cor_preenchimento': QColor(0, 0, 0, 0),
                            'cor_contorno': QColor(255, 0, 0, 255),
                            'espessura_contorno': 1}
carregar_camada(bacia_montante, simbologia_bacia_montante)
print(f'--> Carregamento de "{bacia_montante.name()}" realizado.')

if QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
simbologia_ottotrechos_jusante = {'cor': QColor(0, 85, 230, 255),
                                  'espessura': 1.5}
carregar_camada(ottotrechos_jusante, simbologia_ottotrechos_jusante)
print(f'--> Carregamento de "{ottotrechos_jusante.name()}" realizado.')

if QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante_2'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante_2')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
simbologia_ottotrechos_jusante_2 = {'cor': QColor(20, 0, 220, 255),
                                  'espessura': 0.5}
carregar_camada(ottotrechos_jusante_2, simbologia_ottotrechos_jusante_2)
print(f'--> Carregamento de "{ottotrechos_jusante_2.name()}" realizado.')
