import psycopg2

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
        JOIN basemap.ottobacias_pb_5k
        ON ST_Intersects(cenario_0.outorgas.geom, cenario_0.ottobacias_5k.geom)
        GROUP BY basemap.ottobacias_pb_5k.cobacia
        ORDER BY basemap.ottobacias_pb_5k.cobacia DESC;
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