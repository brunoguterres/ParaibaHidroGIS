import psycopg2

def uniao_disp_cap():
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()

    cursor.execute("""
        DROP VIEW IF EXISTS cenario_0.dados_balanco CASCADE;
        CREATE VIEW cenario_0.dados_balanco AS
        SELECT
            basemap.ottotrechos_pb_5k.cobacia,
            basemap.ottotrechos_pb_5k.cotrecho,
            basemap.ottotrechos_pb_5k.trechojus,
            basemap.ottotrechos_pb_5k.cabeceira,
            cenario_0.disponibilidade.vazao_incremental,
            cenario_0.disponibilidade.vazao_naturalizada,
            COALESCE(cenario_0.captacoes_ottobacias.captacao_solicitada, 0) AS captacao_solicitada
        FROM basemap.ottotrechos_pb_5k
        LEFT JOIN cenario_0.disponibilidade ON basemap.ottotrechos_pb_5k.cobacia = cenario_0.disponibilidade.cobacia
        LEFT JOIN cenario_0.captacoes_ottobacias ON basemap.ottotrechos_pb_5k.cobacia = cenario_0.captacoes_ottobacias.cobacia
        ORDER BY basemap.ottotrechos_pb_5k.cobacia DESC;
        """)
    
    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

#trecho_disponibilidade_captacao = uniao_trecho_disp_cap()

uniao_disp_cap()

print('--> União de dados realizada.')