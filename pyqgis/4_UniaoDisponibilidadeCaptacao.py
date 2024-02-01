
def uniao_disponibilidade_captacoes():
    query_uniao =    '?query=SELECT camada_ottotrechos.cobacia, camada_ottotrechos.cotrecho, camada_ottotrechos.nutrjus, camada_disp_hid.cobacia_2, camada_disp_hid.disp_x '\
                        'FROM camada_ottotrechos '\
                        'LEFT JOIN camada_disp_hid ON camada_ottotrechos.cobacia = camada_disp_hid.cobacia_2;'
    disponibilidade_captacao = QgsVectorLayer(query_uniao, 'uniao_disp_cap', 'virtual')
    QgsProject.instance().addMapLayer(disponibilidade_captacao)
    return disponibilidade_captacao

### EXECUÇÃO ###

disponibilidade_captacao = uniao_disponibilidade_captacoes()
print('\n''-> União de disponibilidades com captações.')