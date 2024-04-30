import psycopg2

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
    print(f'Camada {ottotrechos.name()} existe!!!')
    QgsProject.instance().removeMapLayer(ottotrechos)
    print('Camada "camada_ottotrechos" REMOVIDA.')

campo = 'classe_isr'
indice = ottobacias_isr.fields().indexFromName(campo)
unique_values = ottobacias_isr.uniqueValues(indice)
cores_classes = {'1': QColor(6, 128, 14),
                 '2': QColor(153, 130, 15),
                 '3': QColor(153, 59, 15),
                 '4': QColor(153, 15, 61),
                 '5': QColor(107, 15, 153)}
rotulos_classes = {'1': 'Sem criticidade',
                   '2': 'Baixo potencial de comprometimento',
                   '3': 'Médio potencial de comprometimento',
                   '4': 'Alto potencial de comprometimento',
                   '5': 'Déficit de atendimento às demandas'}
categorias = []
for value in unique_values:
    simbologia = QgsSymbol.defaultSymbol(ottobacias_isr.geometryType())
    categoria = QgsRendererCategory(value, simbologia, str(value))
    if str(value) in cores_classes:
        simbologia.setColor(cores_classes[str(value)])
    if str(value) in rotulos_classes:
        categoria.setLabel(rotulos_classes[str(value)])
    categorias.append(categoria)
renderer = QgsCategorizedSymbolRenderer(campo, categorias)
ottobacias_isr.setRenderer(renderer)
ottobacias_isr.triggerRepaint()
        
if (int(cod_otto_bacia) % 2) == 0:
    cod_otto_e = cod_otto_bacia
    print('código_bacia:', cod_otto_e)
            
else:
    for letra in range(len(cod_otto_bacia)):
        index = (letra + 1) * -1
        conv_num = int(cod_otto_bacia[index])
        resto = conv_num % 2        
        if resto == 0:
            cod_otto_e = cod_otto_bacia[:(index + 1)]
            print('código_bacia:', cod_otto_e)
            break

cursor.execute(f'''
    DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottobacias_montante CASCADE;
    CREATE VIEW {parametros_conexao['schema_cenario']}.ottobacias_montante AS
    SELECT *
    FROM {parametros_conexao['schema_cenario']}.ottobacias_isr
    WHERE {parametros_conexao['schema_cenario']}.ottobacias_isr.cobacia LIKE '{cod_otto_e}%' AND ottobacias_isr.cobacia >= '{cod_otto_bacia}';
''')
conexao.commit()

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
        selecao = selecao + "basemap.ottotrechos_pb_5k.curso_dagua LIKE '"+ elementos +"' OR "
    else:
        break
comp = len(selecao)
comp2 = comp - 3
sele2 = selecao [:comp2]
print('selecao:', sele2)

cursor.execute(f'''
    DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottotrechos_jusante CASCADE;
    CREATE VIEW {parametros_conexao['schema_cenario']}.ottotrechos_jusante AS
    SELECT
        ottotrechos_pb_5k.cobacia,
        ottotrechos_pb_5k.curso_dagua,
        ottotrechos_pb_5k.nome_rio,
        ottotrechos_pb_5k.geom
    FROM {basemap}.ottotrechos_pb_5k
    WHERE ({sele2}) AND ottotrechos_pb_5k.cobacia < '{cod_otto_bacia}';
''')
conexao.commit()

cursor.execute(f'''
    DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottotrechos_jusante_2 CASCADE;
    CREATE VIEW {parametros_conexao['schema_cenario']}.ottotrechos_jusante_2 AS
    SELECT
        ottotrechos_pb_5k.cobacia,
        ottotrechos_pb_5k.curso_dagua,
        ottotrechos_pb_5k.nome_rio,
        ottotrechos_pb_5k.geom
    FROM {basemap}.ottotrechos_pb_5k
    WHERE ({sele2}) AND ottotrechos_pb_5k.cobacia >= '{cod_otto_bacia}';
''')
conexao.commit()
cursor.close()
conexao.close()

if QgsProject.instance().mapLayersByName('camada_ottobacias_montante'):
    QgsProject.instance().removeMapLayer(ottobacias_montante)

uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                    parametros_conexao['porta_bd'],
                    parametros_conexao['nome_bd'],
                    parametros_conexao['usuario_bd'],
                    parametros_conexao['senha_bd'])
uri.setDataSource(parametros_conexao['schema_cenario'], 'ottobacias_montante', 'geom', '', 'cobacia')
ottobacias_montante = QgsVectorLayer(uri.uri(), 'camada_ottobacias_montante', 'postgres')
QgsProject.instance().addMapLayer(ottobacias_montante)
            
campo = 'classe_isr'
indice = ottobacias_montante.fields().indexFromName(campo)
unique_values = ottobacias_montante.uniqueValues(indice)
cores_classes = {'1': QColor(10, 204, 23),
                    '2': QColor(247, 210, 24),
                    '3': QColor(247, 98, 24),
                    '4': QColor(230, 23, 26),
                    '5': QColor(161, 23, 230)}
rotulos_classes = {'1': 'Sem criticidade',
                    '2': 'Baixo potencial de comprometimento',
                    '3': 'Médio potencial de comprometimento',
                    '4': 'Alto potencial de comprometimento',
                    '5': 'Déficit de atendimento às demandas'}
categorias = []
for value in unique_values:
    simbologia = QgsSymbol.defaultSymbol(ottobacias_montante.geometryType())
    categoria = QgsRendererCategory(value, simbologia, str(value))
    if str(value) in cores_classes:
        simbologia.setColor(cores_classes[str(value)])
    if str(value) in rotulos_classes:
        categoria.setLabel(rotulos_classes[str(value)])
    categorias.append(categoria)

renderer = QgsCategorizedSymbolRenderer(campo, categorias)
ottobacias_montante.setRenderer(renderer)
ottobacias_montante.triggerRepaint()

if QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante'):
    QgsProject.instance().removeMapLayer(ottotrechos_jusante)

uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                  parametros_conexao['porta_bd'],
                  parametros_conexao['nome_bd'],
                  parametros_conexao['usuario_bd'],
                  parametros_conexao['senha_bd'])
uri.setDataSource(parametros_conexao['schema_cenario'], 'ottotrechos_jusante', 'geom', '', 'cobacia')
ottotrechos_jusante = QgsVectorLayer(uri.uri(False), 'camada_ottotrechos_jusante', 'postgres')
print('--> Importação da camada "'+ottotrechos_jusante.name()+'" realizada.')
simbologia = {'r':20, 'g':0, 'b':255, 'a':255, 'width':1.2}
ottotrechos_jusante.renderer().symbol().setColor(QColor(simbologia['r'],
                                                                simbologia['g'],
                                                                simbologia['b'],
                                                                simbologia['a']))
ottotrechos_jusante.renderer().symbol().setWidth(simbologia['width'])
QgsProject.instance().addMapLayer(ottotrechos_jusante)
print('--> Carregamento de "'+ottotrechos_jusante.name()+'" realizado.')

if QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante_2'):
    QgsProject.instance().removeMapLayer(ottotrechos_jusante_2)

uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                  parametros_conexao['porta_bd'],
                  parametros_conexao['nome_bd'],
                  parametros_conexao['usuario_bd'],
                  parametros_conexao['senha_bd'])
uri.setDataSource(parametros_conexao['schema_cenario'], 'ottotrechos_jusante_2', 'geom', '', 'cobacia')
ottotrechos_jusante_2 = QgsVectorLayer(uri.uri(False), 'camada_ottotrechos_jusante_2', 'postgres')
print('--> Importação da camada "'+ottotrechos_jusante_2.name()+'" realizada.')
simbologia = {'r':20, 'g':0, 'b':220, 'a':220, 'width':0.5}
ottotrechos_jusante_2.renderer().symbol().setColor(QColor(simbologia['r'],
                                                                simbologia['g'],
                                                                simbologia['b'],
                                                                simbologia['a']))
ottotrechos_jusante_2.renderer().symbol().setWidth(simbologia['width'])
QgsProject.instance().addMapLayer(ottotrechos_jusante_2)
print('--> Carregamento de "'+ottotrechos_jusante_2.name()+'" realizado.')

uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
uri.setDataSource(basemap, 'ottotrechos_pb_5k', 'geom', '', 'cobacia')
ottotrechos = QgsVectorLayer(uri.uri(), 'camada_ottotrechos', 'postgres')
ottotrechos.renderer().symbol().setColor(QColor(0, 150, 255))
QgsProject.instance().addMapLayer(ottotrechos)
print('--> Carregamento de "'+ottotrechos.name()+'" realizado.')
