import psycopg2

class PointTool(QgsMapToolEmitPoint):
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(basemap, 'ottotrechos_pb_5k', 'geom', '', 'cobacia')
    ottotrechos = QgsVectorLayer(uri.uri(), 'camada_ottotrechos', 'postgres')
    ottotrechos.renderer().symbol().setColor(QColor(70, 70, 255))
    QgsProject.instance().addMapLayer(ottotrechos)
    print(f'--> Carregamento de "{ottotrechos.name()}" realizado.')

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.disconnect_signal = False

    def canvasPressEvent(self, event):
        if not self.disconnect_signal:
            point = self.toMapCoordinates(event.pos())
            lat_ponto = point.y()
            long_ponto = point.x()
            #print("Coordenadas do ponto clicado:", lat_ponto, ",", long_ponto)
            self.disconnect_signal = True
            self.deactivate()
            self.canvas.setCursor(Qt.ArrowCursor)
        
        ponto_interesse = QgsVectorLayer(f'VirtualLayer?query=SELECT MakePoint({long_ponto}, {lat_ponto}, 4674)','camada_ponto_interesse', 'virtual')

        ottobacia_selecionada = QgsVectorLayer(f'''VirtualLayer?query=
                                            SELECT *
                                            FROM camada_ottobacias_isr
                                            WHERE ST_Contains(camada_ottobacias_isr.geometry, ST_Point({long_ponto}, {lat_ponto}));''',
                                        'camada_ottobacia_selecionada',
                                        'virtual')
        QgsProject.instance().addMapLayer(ottobacia_selecionada, False)
        global cod_otto_bacia
        cod_otto_bacia = next(ottobacia_selecionada.getFeatures())['cobacia']
        print(f'Código otto da bacia: {cod_otto_bacia}')
        
        QgsProject.instance().addMapLayer(ponto_interesse)
        print(f'--> Carregamento de "{ponto_interesse.name()}" realizado.')
        

### EXECUÇÃO ###

if QgsProject.instance().mapLayersByName('camada_ponto_interesse'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ponto_interesse')[0]
    QgsProject.instance().removeMapLayer(remover_camada)

point_tool = PointTool(iface.mapCanvas())
iface.mapCanvas().setMapTool(point_tool)
