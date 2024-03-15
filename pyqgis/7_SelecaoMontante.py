import psycopg2

class MapToolIdentify(QgsMapToolIdentifyFeature):

    uri = QgsDataSourceUri()
    uri.setConnection("localhost", "5432", "bdg_prh_rpb", "postgres", "cobrape")
    uri.setDataSource("", "ottotrechos_pb_5k", "geom", "", "cobacia")
    ottotrechos_sob = QgsVectorLayer(uri.uri(), 'camada_ottotrechos', "postgres")
    ottotrechos_sob.renderer().symbol().setColor(QColor(0, 150, 255))
    QgsProject.instance().addMapLayer(ottotrechos_sob)
    
    def __init__(self, canvas, ottobacias_icr):
        super().__init__(canvas)
        self.layer = ottobacias_icr

    def canvasReleaseEvent(self, event):
        super().canvasReleaseEvent(event)
        feicao = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentifyFeature.TopDownAll)[0].mFeature
        cod_otto_bacia = feicao.attribute('cobacia')
        canvas.setMapTool(QgsMapToolPan(canvas))
        print('--> Bacia selecionada. Código cobacia:', cod_otto_bacia)

        QgsProject.instance().removeMapLayer(ottobacias_icr)
        

        uri = QgsDataSourceUri()
        uri.setConnection("localhost", "5432", "bdg_prh_rpb", "postgres", "cobrape")
        uri.setDataSource("", "ottobacias_icr", "geom", "", "cobacia")
        ottobacias_icr_sob = QgsVectorLayer(uri.uri(), 'camada_ottobacias_icr', "postgres")
        QgsProject.instance().addMapLayer(ottobacias_icr_sob)
        campo = 'icr'
        indice = ottobacias_icr_sob.fields().indexFromName(campo)
        unique_values = ottobacias_icr_sob.uniqueValues(indice)
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
            simbologia = QgsSymbol.defaultSymbol(ottobacias_icr_sob.geometryType())
            categoria = QgsRendererCategory(value, simbologia, str(value))
            if str(value) in cores_classes:
                simbologia.setColor(cores_classes[str(value)])
            if str(value) in rotulos_classes:
                categoria.setLabel(rotulos_classes[str(value)])
            categorias.append(categoria)
        renderer = QgsCategorizedSymbolRenderer(campo, categorias)
        ottobacias_icr_sob.setRenderer(renderer)
        ottobacias_icr_sob.triggerRepaint()
        
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

        cursor.execute("DROP VIEW IF EXISTS selecao_montante CASCADE;"\
            "CREATE VIEW selecao_montante AS "\
            "SELECT * "\
            "FROM ottobacias_icr "\
            "WHERE ottobacias_icr.cobacia LIKE '"+cod_otto_e+"%' AND ottobacias_icr.cobacia >= '"+cod_otto_bacia+"'")

        conexao.commit()
        cursor.close()
        conexao.close()

        #ATENÇÃO: Revisar, pois somente copiei da etapa 6
        uri = QgsDataSourceUri()
        uri.setConnection("localhost", "5432", "bdg_prh_rpb", "postgres", "cobrape")
        uri.setDataSource("", "selecao_montante", "geom", "", "cobacia")
        selecao_montante = QgsVectorLayer(uri.uri(), 'camada_selelcao_montante', "postgres")
        QgsProject.instance().addMapLayer(selecao_montante)
        
        campo = 'icr'
        indice = selecao_montante.fields().indexFromName(campo)
        unique_values = selecao_montante.uniqueValues(indice)
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
            simbologia = QgsSymbol.defaultSymbol(selecao_montante.geometryType())
            categoria = QgsRendererCategory(value, simbologia, str(value))
            if str(value) in cores_classes:
                simbologia.setColor(cores_classes[str(value)])
            if str(value) in rotulos_classes:
                categoria.setLabel(rotulos_classes[str(value)])
            categorias.append(categoria)

        renderer = QgsCategorizedSymbolRenderer(campo, categorias)
        selecao_montante.setRenderer(renderer)
        selecao_montante.triggerRepaint()

def limpeza_camadas_extras():
    QgsProject.instance().removeMapLayer(ottobacias)
    QgsProject.instance().removeMapLayer(ottotrechos)
    QgsProject.instance().removeMapLayer(disponibilidade)
    QgsProject.instance().removeMapLayer(captacao_ottobacia)
    QgsProject.instance().removeMapLayer(trecho_disponibilidade_captacao)
    print('Camadas extras removidas!')


### EXECUÇÃO ###

canvas = iface.mapCanvas()
map_tool = MapToolIdentify(canvas, ottobacias_icr)
canvas.setMapTool(map_tool)
limpeza_camadas_extras()
