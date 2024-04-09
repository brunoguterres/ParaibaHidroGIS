import psycopg2

def processamento_captacoes():
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()

    cursor.execute(f'''
        DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.captacoes_ottobacias CASCADE;
        CREATE VIEW {parametros_conexao['schema_cenario']}.captacoes_ottobacias AS
        SELECT
	        {basemap}.ottobacias_pb_5k.cobacia,
	        SUM({parametros_conexao['schema_cenario']}.outorgas.captacao_solicitada) AS captacao_solicitada
        FROM {parametros_conexao['schema_cenario']}.outorgas
        JOIN {basemap}.ottobacias_pb_5k
        ON ST_Intersects({parametros_conexao['schema_cenario']}.outorgas.geom, {basemap}.ottobacias_pb_5k.geom)
        GROUP BY {basemap}.ottobacias_pb_5k.cobacia
        ORDER BY {basemap}.ottobacias_pb_5k.cobacia DESC;
        ''')

    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

processamento_captacoes()
print('--> Processamento de captações realizado.')