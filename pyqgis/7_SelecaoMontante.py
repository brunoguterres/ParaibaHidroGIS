class MapToolIdentify(QgsMapToolIdentifyFeature):
    def __init__(self, canvas, ottobacias_icr):
        super().__init__(canvas)
        self.layer = ottobacias_icr

    def canvasReleaseEvent(self, event):
        super().canvasReleaseEvent(event)
        feicao = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentifyFeature.TopDownAll)[0].mFeature
        bacia_selecionada = feicao.attribute('cobacia')
        canvas.setMapTool(QgsMapToolPan(canvas))
        print('--> Bacia selecionada. Código cobacia:', bacia_selecionada)

def limpeza_camadas_extras():
    QgsProject.instance().removeMapLayer(ottobacias)
    QgsProject.instance().removeMapLayer(disponibilidade)
    QgsProject.instance().removeMapLayer(captacao_ottobacia)
    QgsProject.instance().removeMapLayer(trecho_disponibilidade_captacao)
    print('Camadas extras removidas!')

def selecionar_montante():
    pass

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


### EXECUÇÃO ###

canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, ottobacias_icr)
canvas.setMapTool(map_tool)
limpeza_camadas_extras()
selecionar_montante()
ottobacias = importar_camada_bdg(nome_tabela_bdg=nome_tabela_ottobacias, nome_camada='camada_ottobacias')
carregar_camada(ottobacias, simbologia_ottobacias)
