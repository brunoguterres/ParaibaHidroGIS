def importar_camada_bdg(nome_tabela_bdg, nome_camada):
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_cenario'], nome_tabela_bdg, 'geom', '', 'cobacia')
    camada_importada = QgsVectorLayer(uri.uri(False), nome_camada, 'postgres')
    print('--> Importação da camada "'+camada_importada.name()+'" realizada.')
    return camada_importada

def carregar_camada_balanco(ottobacias_isr):
    QgsProject.instance().addMapLayer(ottobacias_isr)
    
    campo = 'classe_isr'
    indice = ottobacias_isr.fields().indexFromName(campo)
    unique_values = ottobacias_isr.uniqueValues(indice)
    cores_classes = {'1': QColor(10, 204, 23),
                     '2': QColor(247, 210, 24),
                     '3': QColor(247, 98, 24),
                     '4': QColor(230, 23, 26),
                     '5': QColor(161, 23, 230)}
    rotulos_classes = {'1': 'Sem criticidade',
                       '2': 'Baixo potencial de comprometimento',
                       '3': 'Médio potencial de comprometimento',
                       '4': 'Alto potencial de comprometimento',
                       '5': 'Déficit de atendimento às demandas'}
    categorias = []
    for value in unique_values:
        simbologia = QgsSymbol.defaultSymbol(ottobacias_isr.geometryType())
        categoria = QgsRendererCategory(value, simbologia, str(value))
        if str(value) in cores_classes:
            simbologia.setColor(cores_classes[str(value)])
        
        if str(value) in rotulos_classes:
            categoria.setLabel(rotulos_classes[str(value)])
        categorias.append(categoria)
    renderer = QgsCategorizedSymbolRenderer(campo, categorias)
    ottobacias_isr.setRenderer(renderer)
    ottobacias_isr.triggerRepaint()
    print('--> Carregamento de camada "'+ottobacias_isr.name()+'" realizado.')

def limpeza_camadas_extras():
    QgsProject.instance().removeMapLayer(ottobacias)
    QgsProject.instance().removeMapLayer(ottotrechos)
    print('Camadas extras removidas!')


### EXECUÇÃO ###

limpeza_camadas_extras()
nome_consulta_ottobacias_isr = 'ottobacias_isr'
ottobacias_isr = importar_camada_bdg(nome_tabela_bdg=nome_consulta_ottobacias_isr, nome_camada='camada_ottobacias_isr')
carregar_camada_balanco(ottobacias_isr)