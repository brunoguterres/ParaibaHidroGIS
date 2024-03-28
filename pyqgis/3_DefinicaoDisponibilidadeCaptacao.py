import psycopg2

def importar_camada_bdg(nome_tabela_bdg, nome_camada):
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_tabela_bdg, 'geom')
    camada_importada = QgsVectorLayer(uri.uri(False), nome_camada, 'postgres')
    print('--> Importação da camada "'+camada_importada.name()+'" realizada.')
    return camada_importada

def carregar_camada(camada, simbologia):
    camada.renderer().symbol().setColor(QColor(simbologia['r'],
                                               simbologia['g'],
                                               simbologia['b'],
                                               simbologia['a']))
    QgsProject.instance().addMapLayer(camada)
    print('--> Carregamento de "'+camada.name()+'" realizado.')

def processamento_captacao(captacoes, ottobacias):
    # método que realiza operações para obter o valor da vazão nas ottobacias a montante da bacia de interesse
    processo_bacias_outorgas = processing.run("native:intersection",{
                                                    'INPUT': captacoes,
                                                    'OVERLAY':ottobacias,
                                                    'OUTPUT':'memory: outorgas_e_ottobacias'})
    intersecao_bacias_outorgas = processo_bacias_outorgas['OUTPUT']
        
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(intersecao_bacias_outorgas))
        
    processo_de_agrupamento_por_ottobacias = processing.run("native:aggregate", {
                'INPUT': intersecao_bacias_outorgas,
		        'GROUP_BY':'"cobacia"',
		        'AGGREGATES':[{'aggregate': 'first_value',
                               'delimiter': ',',
                               'input': '"cobacia"',
                               'length': 0,
                               'name': 'cobacia',
                               'precision': 0,
                               'sub_type': 0,
                               'type': 10,
                               'type_name': 'text'},
                              {'aggregate': 'sum',
                               'delimiter': ',',
                               'input': '"vazão horária (m³/h)"',
                               'length': 0,
                               'name': 'vazão horária (m³/h)',
                               'precision': 0,
                               'sub_type': 0,
                               'type': 6,
                               'type_name': 'double precision'}],
		        'OUTPUT':'memory: captacao_ottobacia'})
    captacao_ottobacia = processo_de_agrupamento_por_ottobacias['OUTPUT']
    return captacao_ottobacia

def processamento_captacoes():
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()

    cursor.execute("""
        DROP VIEW IF EXISTS cenario_0.captacoes_ottobacias CASCADE;
        CREATE VIEW cenario_0.captacoes_ottobacias AS
        SELECT
	        cenario_0.ottobacias_5k.cobacia,
	        SUM(cenario_0.outorgas.captacao_solicitada) AS captacao_solicitada
        FROM cenario_0.outorgas
        JOIN cenario_0.ottobacias_5k
        ON ST_Intersects(cenario_0.outorgas.geom, cenario_0.ottobacias_5k.geom)
        GROUP BY cenario_0.ottobacias_5k.cobacia
        ORDER BY cenario_0.ottobacias_5k.cobacia DESC;
    """)

    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

'''
nome_tabela_captacoes = 'outorgas'
nome_tabela_captacao_ottobacia = 'captacao_ottobacia'
nome_tabela_disponibilidade = 'disp_hid_pb_5k'
captacao_ottobacia = importar_camada_bdg(nome_tabela_bdg=nome_tabela_captacao_ottobacia, nome_camada='camada_captacao_ottobacia')
disponibilidade = importar_camada_bdg(nome_tabela_bdg=nome_tabela_disponibilidade, nome_camada='camada_disponibilidade')
simbologia_disponibilidade = {'r':0, 'g':255, 'b':0, 'a':255}
simbologia_captacao_ottobacia = {'r':255, 'g':180, 'b':0, 'a':255}
carregar_camada(disponibilidade, simbologia_disponibilidade)
carregar_camada(captacao_ottobacia, simbologia_captacao_ottobacia)
'''

processamento_captacoes()

print('--> Definições de disponibilidades e captações realizada.')