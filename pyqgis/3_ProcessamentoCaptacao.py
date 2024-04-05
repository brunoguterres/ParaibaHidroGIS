import psycopg2

def processamento_captacoes(schema_cenario, basemap):
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()

    cursor.execute('''
        DROP VIEW IF EXISTS {schema_cenario}.captacoes_ottobacias CASCADE;
        CREATE VIEW {schema_cenario}.captacoes_ottobacias AS
        SELECT
	        {schema_base}.ottobacias_pb_5k.cobacia,
	        SUM({schema_cenario}.outorgas.captacao_solicitada) AS captacao_solicitada
        FROM {schema_cenario}.outorgas
        JOIN {schema_base}.ottobacias_pb_5k
        ON ST_Intersects({schema_cenario}.outorgas.geom, {schema_base}.ottobacias_pb_5k.geom)
        GROUP BY {schema_base}.ottobacias_pb_5k.cobacia
        ORDER BY {schema_base}.ottobacias_pb_5k.cobacia DESC;
        '''.format(schema_cenario=schema_cenario, schema_base=basemap))

    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

processamento_captacoes(parametros_conexao['schema_cenario'], basemap)
print('--> Processamento de captações realizado.')