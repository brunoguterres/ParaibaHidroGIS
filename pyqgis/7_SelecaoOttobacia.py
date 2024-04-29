import psycopg2

class MapToolIdentify(QgsMapToolIdentifyFeature):
    if QgsProject.instance().mapLayersByName('camada_ottotrechos'):
        print(f'Camada {ottotrechos.name()} existe!!!')
        QgsProject.instance().removeMapLayer(ottotrechos)

    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(basemap, 'ottotrechos_pb_5k', 'geom', '', 'cobacia')
    ottotrechos = QgsVectorLayer(uri.uri(), 'camada_ottotrechos', 'postgres')
    ottotrechos.renderer().symbol().setColor(QColor(0, 150, 255))
    QgsProject.instance().addMapLayer(ottotrechos)

    def __init__(self, canvas, ottobacias_isr):
        super().__init__(canvas)
        self.layer = ottobacias_isr

    def canvasReleaseEvent(self, event):
        super().canvasReleaseEvent(event)
        feicao = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentifyFeature.TopDownAll)[0].mFeature
        cod_otto_bacia = feicao.attribute('cobacia')
        canvas.setMapTool(QgsMapToolPan(canvas))
        print('--> Bacia selecionada. Código cobacia:', cod_otto_bacia)
    
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
            SELECT
                {parametros_conexao['schema_cenario']}.resultado_balanco.*,
                {basemap}.ottobacias_pb_5k.geom
            FROM {parametros_conexao['schema_cenario']}.resultado_balanco
            LEFT JOIN {basemap}.ottobacias_pb_5k
                ON {parametros_conexao['schema_cenario']}.resultado_balanco.cobacia = {basemap}.ottobacias_pb_5k.cobacia
            WHERE {parametros_conexao['schema_cenario']}.resultado_balanco.cobacia = '{cod_otto_bacia}';
        ''')
        conexao.commit()
        cursor.close()
        conexao.close()


### EXECUÇÃO ###
canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, ottobacias_isr)
canvas.setMapTool(map_tool)