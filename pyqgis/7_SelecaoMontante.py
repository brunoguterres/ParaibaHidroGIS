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

    def __init__(self, canvas, ottobacias_isr):
        super().__init__(canvas)
        self.layer = ottobacias_isr

    def canvasReleaseEvent(self, event):
        super().canvasReleaseEvent(event)
        feicao = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentifyFeature.TopDownAll)[0].mFeature
        cod_otto_bacia = feicao.attribute('cobacia')
        canvas.setMapTool(QgsMapToolPan(canvas))
        print('--> Bacia selecionada. Código cobacia:', cod_otto_bacia)

        QgsProject.instance().removeMapLayer(ottobacias_isr)

        uri = QgsDataSourceUri()
        uri.setConnection(parametros_conexao['host_bd'],
                          parametros_conexao['porta_bd'],
                          parametros_conexao['nome_bd'],
                          parametros_conexao['usuario_bd'],
                          parametros_conexao['senha_bd'])
        uri.setDataSource(parametros_conexao['schema_cenario'], 'ottobacias_isr', 'geom', '', 'cobacia')
        ottobacias_isr_sob = QgsVectorLayer(uri.uri(), 'camada_ottobacias_isr', 'postgres')
        QgsProject.instance().addMapLayer(ottobacias_isr_sob)
        campo = 'isr'
        indice = ottobacias_isr_sob.fields().indexFromName(campo)
        unique_values = ottobacias_isr_sob.uniqueValues(indice)
        cores_classes = {   '1': QColor(80, 150, 162, 50),
                            '2': QColor(105, 217, 114, 50),
                            '3': QColor(255, 255, 116, 50),
                            '4': QColor(253, 144, 64, 50),
                            '5': QColor(215, 61, 125, 50)}
        rotulos_classes = { '1': 'Sem criticidade',
                            '2': 'Baixo potencial de comprometimento',
                            '3': 'Médio potencial de comprometimento',
                            '4': 'Alto potencial de comprometimento',
                            '5': 'Déficit de atendimento às demandas'}
        categorias = []
        for value in unique_values:
            simbologia = QgsSymbol.defaultSymbol(ottobacias_isr_sob.geometryType())
            categoria = QgsRendererCategory(value, simbologia, str(value))
            if str(value) in cores_classes:
                simbologia.setColor(cores_classes[str(value)])
            if str(value) in rotulos_classes:
                categoria.setLabel(rotulos_classes[str(value)])
            categorias.append(categoria)
        renderer = QgsCategorizedSymbolRenderer(campo, categorias)
        ottobacias_isr_sob.setRenderer(renderer)
        ottobacias_isr_sob.triggerRepaint()
        
        if (int(cod_otto_bacia) % 2) == 0:
            cod_otto_e = cod_otto_bacia
            print('código_bacia:', cod_otto_e)
            
        else:
            for letra in range(len(cod_otto_bacia)):
                
                index = (letra + 1) * -1

                conv_num = int(cod_otto_bacia[index])
                resto = conv_num % 2
                
                if resto == 0:
                    cod_otto_e = cod_otto_bacia[:(index + 1)]
                    print('código_bacia:', cod_otto_e)
                    break

        conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
        cursor = conexao.cursor()

        cursor.execute(f'''
            DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottobacias_montante CASCADE;
            CREATE VIEW {parametros_conexao['schema_cenario']}.ottobacias_montante AS
            SELECT *
            FROM {parametros_conexao['schema_cenario']}.ottobacias_isr
            WHERE {parametros_conexao['schema_cenario']}.ottobacias_isr.cobacia LIKE '{cod_otto_e}%' AND ottobacias_isr.cobacia >= '{cod_otto_bacia}';
        ''')
        conexao.commit()
        cursor.close()
        conexao.close()

        #ATENÇÃO: Revisar, pois somente copiei da etapa 6
        uri = QgsDataSourceUri()
        uri.setConnection(parametros_conexao['host_bd'],
                          parametros_conexao['porta_bd'],
                          parametros_conexao['nome_bd'],
                          parametros_conexao['usuario_bd'],
                          parametros_conexao['senha_bd'])
        uri.setDataSource(parametros_conexao['schema_cenario'], 'ottobacias_montante', 'geom', '', 'cobacia')
        ottobacias_montante = QgsVectorLayer(uri.uri(), 'camada_ottobacias_montante', 'postgres')
        QgsProject.instance().addMapLayer(ottobacias_montante)
        
        campo = 'isr'
        indice = ottobacias_montante.fields().indexFromName(campo)
        unique_values = ottobacias_montante.uniqueValues(indice)
        cores_classes = {   '1': QColor(80, 150, 162),
                            '2': QColor(105, 217, 114),
                            '3': QColor(255, 255, 116),
                            '4': QColor(253, 144, 64),
                            '5': QColor(215, 61, 125)}
        rotulos_classes = { '1': 'Sem criticidade',
                            '2': 'Baixo potencial de comprometimento',
                            '3': 'Médio potencial de comprometimento',
                            '4': 'Alto potencial de comprometimento',
                            '5': 'Déficit de atendimento às demandas'}
        categorias = []
        for value in unique_values:
            simbologia = QgsSymbol.defaultSymbol(ottobacias_montante.geometryType())
            categoria = QgsRendererCategory(value, simbologia, str(value))
            if str(value) in cores_classes:
                simbologia.setColor(cores_classes[str(value)])
            if str(value) in rotulos_classes:
                categoria.setLabel(rotulos_classes[str(value)])
            categorias.append(categoria)

        renderer = QgsCategorizedSymbolRenderer(campo, categorias)
        ottobacias_montante.setRenderer(renderer)
        ottobacias_montante.triggerRepaint()

def limpeza_camadas_extras():
    QgsProject.instance().removeMapLayer(ottobacias)
    QgsProject.instance().removeMapLayer(ottotrechos)
    print('Camadas extras removidas!')


### EXECUÇÃO ###

canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, ottobacias_isr)
canvas.setMapTool(map_tool)
limpeza_camadas_extras()
