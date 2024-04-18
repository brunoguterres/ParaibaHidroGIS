import psycopg2

conexao = psycopg2.connect(
dbname = str(parametros_conexao['nome_bd']),
user = str(parametros_conexao['usuario_bd']),
password = str(parametros_conexao['senha_bd']),
host = str(parametros_conexao['host_bd']),
port = str(parametros_conexao['porta_bd']))
cursor = conexao.cursor()

QgsProject.instance().removeMapLayer(ottobacias_isr)

uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                  parametros_conexao['porta_bd'],
                  parametros_conexao['nome_bd'],
                  parametros_conexao['usuario_bd'],
                  parametros_conexao['senha_bd'])
uri.setDataSource(parametros_conexao['schema_cenario'], 'ottobacias_isr', 'geom', '', 'cobacia')
ottobacias_isr_sob = QgsVectorLayer(uri.uri(), 'camada_ottobacias_isr', 'postgres')
QgsProject.instance().addMapLayer(ottobacias_isr_sob)
campo = 'classe_isr'
indice = ottobacias_isr_sob.fields().indexFromName(campo)
unique_values = ottobacias_isr_sob.uniqueValues(indice)
cores_classes = {'1': QColor(80, 150, 162, 50),
                 '2': QColor(105, 217, 114, 50),
                 '3': QColor(255, 255, 116, 50),
                 '4': QColor(253, 144, 64, 50),
                 '5': QColor(215, 61, 125, 50)}
rotulos_classes = {'1': 'Sem criticidade',
                   '2': 'Baixo potencial de comprometimento',
                   '3': 'Médio potencial de comprometimento',
                   '4': 'Alto potencial de comprometimento',
                   '5': 'Déficit de atendimento às demandas'}
categorias = []
for value in unique_values:
    simbologia = QgsSymbol.defaultSymbol(ottobacias_isr_sob.geometryType())
    categoria = QgsRendererCategory(value, simbologia, str(value))
    if str(value) in cores_classes:
        simbologia.setColor(cores_classes[str(value)])
    if str(value) in rotulos_classes:
        categoria.setLabel(rotulos_classes[str(value)])
    categorias.append(categoria)
renderer = QgsCategorizedSymbolRenderer(campo, categorias)
ottobacias_isr_sob.setRenderer(renderer)
ottobacias_isr_sob.triggerRepaint()
        
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
    WHERE {sele2} AND ottotrechos_pb_5k.cobacia <= '{cod_otto_bacia}';
''')
conexao.commit()
cursor.close()
conexao.close()

#ATENÇÃO: Revisar, pois somente copiei da etapa 6
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
cores_classes = {'1': QColor(80, 150, 162),
                 '2': QColor(105, 217, 114),
                 '3': QColor(255, 255, 116),
                 '4': QColor(253, 144, 64),
                 '5': QColor(215, 61, 125)}
rotulos_classes = { '1': 'Sem criticidade',
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
    
uri = QgsDataSourceUri()
uri.setConnection(parametros_conexao['host_bd'],
                  parametros_conexao['porta_bd'],
                  parametros_conexao['nome_bd'],
                  parametros_conexao['usuario_bd'],parametros_conexao['senha_bd'])
uri.setDataSource(parametros_conexao['schema_cenario'], 'ottotrechos_jusante', 'geom', '', 'cobacia')
camada_ottrechos_jusante = QgsVectorLayer(uri.uri(False), 'camada_ottotrechos_jusante', 'postgres')
print('--> Importação da camada "'+camada_ottrechos_jusante.name()+'" realizada.')
simbologia = {'r':20, 'g':0, 'b':255, 'a':255}
camada_ottrechos_jusante.renderer().symbol().setColor(QColor(simbologia['r'],
                                                             simbologia['g'],
                                                             simbologia['b'],
                                                             simbologia['a']))
QgsProject.instance().addMapLayer(camada_ottrechos_jusante)
print('--> Carregamento de "'+camada_ottrechos_jusante.name()+'" realizado.')