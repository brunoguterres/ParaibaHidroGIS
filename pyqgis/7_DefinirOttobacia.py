import psycopg2

class PointTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.disconnect_signal = False

    def canvasPressEvent(self, event):
        if not self.disconnect_signal:
            point = self.toMapCoordinates(event.pos())
            lat_ponto = point.y()
            long_ponto = point.x()
            print("Coordenadas do ponto clicado:", lat_ponto, ",", long_ponto)
            self.disconnect_signal = True
            self.deactivate()
            self.canvas.setCursor(Qt.ArrowCursor)
        
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
        cursor.close()
        conexao.close()

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


### EXECUÇÃO ###

point_tool = PointTool(iface.mapCanvas())
iface.mapCanvas().setMapTool(point_tool)
