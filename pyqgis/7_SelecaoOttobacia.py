import os
import psycopg2

class MapToolIdentify(QgsMapToolIdentifyFeature):
    
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(basemap, 'ottotrechos_pb_5k', 'geom', '', 'cobacia')
    ottotrechos_sob = QgsVectorLayer(uri.uri(), 'camada_ottotrechos', 'postgres')
    ottotrechos_sob.renderer().symbol().setColor(QColor(0, 150, 255))
    QgsProject.instance().addMapLayer(ottotrechos_sob)

    def __init__(self, canvas, ottobacias):
        super().__init__(canvas)
        self.layer = ottobacias

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
exec(open('C:/Users/brunoguterres/Desktop/GitHubFiles/ParaibaHidroGIS/pyqgis/2_InicializacaoMapa.py').read())
canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, ottobacias)
canvas.setMapTool(map_tool)