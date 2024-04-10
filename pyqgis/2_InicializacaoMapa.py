import requests

def limpeza_residuos():
    camada_residual = QgsProject.instance().mapLayers().values()
    lista_camadas_residuais = [l for l in camada_residual]
    if len(lista_camadas_residuais) > 0:
        for camada in lista_camadas_residuais:
            QgsProject.instance().removeMapLayer(camada)
        mensagem_saida_limpeza = '--> Limpeza de camadas residuais de execuções anteriores realizada!'
    else:
        mensagem_saida_limpeza = '--> Não existem camadas residuais de execuções anteriores.'
    canvas = qgis.utils.iface.mapCanvas()
    canvas.refresh()
    print(mensagem_saida_limpeza)

def importar_camada_bdg(nome_tabela_bdg, nome_schema_bdg, nome_camada):
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(nome_schema_bdg, nome_tabela_bdg, 'geom') # Atenção para 2 parâmetros que faltam nesta declaração (vide etapa 6)
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

limpeza_residuos()
nome_tabela_ottobacias = 'ottobacias_pb_5k'
nome_tabela_ottotrechos = 'ottotrechos_pb_5k'
ottobacias = importar_camada_bdg(nome_tabela_bdg=nome_tabela_ottobacias, nome_schema_bdg=basemap, nome_camada='camada_ottobacias')
ottotrechos = importar_camada_bdg(nome_tabela_bdg=nome_tabela_ottotrechos, nome_schema_bdg=basemap, nome_camada='camada_ottotrechos')
simbologia_ottobacias = {'r':200, 'g':200, 'b':200, 'a':10}
simbologia_ottotrechos = {'r':0, 'g':150, 'b':255, 'a':255}
importar_camada_fundo()
carregar_camada(ottobacias, simbologia_ottobacias)
carregar_camada(ottotrechos, simbologia_ottotrechos)