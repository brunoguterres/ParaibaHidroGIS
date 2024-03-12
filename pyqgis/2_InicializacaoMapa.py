import requests

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


def importar_camada_fundo():
    # função de carregamento da camada de plano de fundo
    service_url = 'mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    service_uri = 'type=xyz&zmin=0&zmax=21&url=https://'+requests.utils.quote(service_url)
    iface.addRasterLayer(service_uri, 'Google_Road', 'wms')
    print('--> Carregamento de camada basemap realizado.')


### EXECUÇÃO ###

nome_tabela_ottobacias = 'ottobacias_pb_5k'
nome_tabela_ottotrechos = 'ottotrechos_pb_5k'
ottobacias = importar_camada_bdg(nome_tabela_bdg=nome_tabela_ottobacias, nome_camada='camada_ottobacias')
ottotrechos = importar_camada_bdg(nome_tabela_bdg=nome_tabela_ottotrechos, nome_camada='camada_ottotrechos')
simbologia_ottobacias = {'r':200, 'g':200, 'b':200, 'a':10}
simbologia_ottotrechos = {'r':0, 'g':150, 'b':255, 'a':255}
importar_camada_fundo()
carregar_camada(ottobacias, simbologia_ottobacias)
carregar_camada(ottotrechos, simbologia_ottotrechos)