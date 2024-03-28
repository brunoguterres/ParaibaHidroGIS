import psycopg2

def uniao_trecho_disp_cap():
    query_uniao =   '?query=SELECT  camada_ottotrechos.cobacia, '\
                                    'camada_ottotrechos.cotrecho, '\
                                    'camada_ottotrechos.nutrjus, '\
                                    'camada_ottotrechos.cabeceira, '\
                                    'camada_disponibilidade.disp_x, '\
                                    'COALESCE(camada_captacao_ottobacia.cap_x2, 0) AS captacao '\
                    'FROM camada_ottotrechos '\
                    'LEFT JOIN camada_disponibilidade ON camada_ottotrechos.cobacia = camada_disponibilidade.cobacia_2 '\
                    'LEFT JOIN camada_captacao_ottobacia ON camada_ottotrechos.cobacia = camada_captacao_ottobacia.cobacia_2 '\
                    'ORDER BY camada_ottotrechos.cobacia DESC;'
    trecho_disponibilidade_captacao = QgsVectorLayer(query_uniao, 'uniao_trecho_disp_cap', 'virtual')
    QgsProject.instance().addMapLayer(trecho_disponibilidade_captacao)
    return trecho_disponibilidade_captacao

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
            cenario_0.ottotrechos_5k.cobacia,
            cenario_0.ottotrechos_5k.cotrecho,
            cenario_0.ottotrechos_5k.trechojus,
            cenario_0.ottotrechos_5k.cabeceira,
            cenario_0.disponibilidade.vazao_incremental,
            cenario_0.disponibilidade.vazao_naturalizada,
            COALESCE(cenario_0.captacoes_ottobacias.captacao_solicitada, 0) AS captacao_solicitada
        FROM cenario_0.ottotrechos_5k
        LEFT JOIN cenario_0.disponibilidade ON cenario_0.ottotrechos_5k.cobacia = cenario_0.disponibilidade.cobacia
        LEFT JOIN cenario_0.captacoes_ottobacias ON cenario_0.ottotrechos_5k.cobacia = cenario_0.captacoes_ottobacias.cobacia
        ORDER BY cenario_0.ottotrechos_5k.cobacia DESC;
        """)
    
    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

#trecho_disponibilidade_captacao = uniao_trecho_disp_cap()

uniao_disp_cap()

print('--> União de dados realizada.')