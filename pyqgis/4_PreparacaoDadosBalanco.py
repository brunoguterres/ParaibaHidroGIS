import psycopg2

def uniao_disp_cap():
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()

    cursor.execute(f'''
        DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.dados_balanco CASCADE;
        CREATE VIEW {parametros_conexao['schema_cenario']}.dados_balanco AS
        SELECT
            {basemap}.ottotrechos_pb_5k.cobacia,
            {basemap}.ottotrechos_pb_5k.cotrecho,
            {basemap}.ottotrechos_pb_5k.trechojus,
            {basemap}.ottotrechos_pb_5k.cabeceira,
            {parametros_conexao['schema_cenario']}.disponibilidade_hidrica.vazao_incremental,
            {parametros_conexao['schema_cenario']}.disponibilidade_hidrica.vazao_natural,
            COALESCE({parametros_conexao['schema_cenario']}.captacoes_ottobacias.captacao_solicitada, 0) AS captacao_solicitada
        FROM {basemap}.ottotrechos_pb_5k
        LEFT JOIN {parametros_conexao['schema_cenario']}.disponibilidade_hidrica
            ON {basemap}.ottotrechos_pb_5k.cobacia = {parametros_conexao['schema_cenario']}.disponibilidade_hidrica.cobacia
        LEFT JOIN {parametros_conexao['schema_cenario']}.captacoes_ottobacias
            ON {basemap}.ottotrechos_pb_5k.cobacia = {parametros_conexao['schema_cenario']}.captacoes_ottobacias.cobacia
        ORDER BY {basemap}.ottotrechos_pb_5k.cobacia DESC;
        ''')
    
    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

uniao_disp_cap()
print('--> Preparação de dados para balanço realizada.')