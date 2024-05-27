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
        
        conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
        cursor = conexao.cursor()

        cursor.execute(f'''
            DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottobacia_selecionada CASCADE;
            CREATE VIEW {parametros_conexao['schema_cenario']}.ottobacia_selecionada AS
            SELECT {basemap}.ottobacias_pb_5k.*
            FROM {basemap}.ottobacias_pb_5k
            WHERE ST_Contains({basemap}.ottobacias_pb_5k.geom, ST_SetSRID(ST_MakePoint({long_ponto}, {lat_ponto}), 4674));
        ''')
        conexao.commit()

        cursor.execute(f'''SELECT cobacia FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
        cod_otto_bacia = cursor.fetchone()[0]

        cursor.close()
        conexao.close()

        print(f'Código otto da bacia: {cod_otto_bacia}')

        # trecho adicionado para teste de visualização de resultado
        '''
        uri = QgsDataSourceUri()
        uri.setConnection(parametros_conexao['host_bd'],
                            parametros_conexao['porta_bd'],
                            parametros_conexao['nome_bd'],
                            parametros_conexao['usuario_bd'],
                            parametros_conexao['senha_bd'])
        uri.setDataSource(parametros_conexao['schema_cenario'], 'ottobacia_selecionada', 'geom', '', 'cobacia')
        ottobacia_selecionada = QgsVectorLayer(uri.uri(), 'camada_ottobacia_selecionada', 'postgres')
        ottobacia_selecionada.renderer().symbol().setColor(QColor(255, 255, 0))
        QgsProject.instance().addMapLayer(ottobacia_selecionada)
        print(f'--> Carregamento de "{ottobacia_selecionada.name()}" realizado.')
        '''

        
        
        QgsProject.instance().addMapLayer(ponto_interesse)
        print(f'--> Carregamento de "{ponto_interesse.name()}" realizado.')


### EXECUÇÃO ###

if QgsProject.instance().mapLayersByName('camada_ponto_interesse'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ponto_interesse')[0]
    QgsProject.instance().removeMapLayer(remover_camada)

point_tool = PointTool(iface.mapCanvas())
iface.mapCanvas().setMapTool(point_tool)
