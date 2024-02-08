def uniao_trecho_disp_cap():
    query_uniao =   '?query=SELECT  camada_ottotrechos.cobacia, '\
                                    'camada_ottotrechos.cotrecho, '\
                                    'camada_ottotrechos.nutrjus, '\
                                    'camada_ottotrechos.cabeceira, '\
                                    'camada_disponibilidade.disp_x, '\
                                    'COALESCE(camada_captacao_ottobacia.cap_x, 0) AS captacao '\
                    'FROM camada_ottotrechos '\
                    'LEFT JOIN camada_disponibilidade ON camada_ottotrechos.cobacia = camada_disponibilidade.cobacia_2 '\
                    'LEFT JOIN camada_captacao_ottobacia ON camada_ottotrechos.cobacia = camada_captacao_ottobacia.cobacia_2 '\
                    'ORDER BY camada_ottotrechos.cobacia DESC;'
    trecho_disponibilidade_captacao = QgsVectorLayer(query_uniao, 'uniao_trecho_disp_cap', 'virtual')
    QgsProject.instance().addMapLayer(trecho_disponibilidade_captacao)
    return trecho_disponibilidade_captacao

### EXECUÇÃO ###

trecho_disponibilidade_captacao = uniao_trecho_disp_cap()
print('--> União de dados realizada.')