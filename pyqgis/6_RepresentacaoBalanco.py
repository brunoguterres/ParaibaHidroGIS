def carregar_camada_balanco():
    #ATENÇÃO TENTAR USAR FUNÇÃO "importar_camada_bdg" E "carregar_camada" da etapa 2
    uri = QgsDataSourceUri()
    uri.setConnection("localhost", "5432", "bdg_prh_rpb", "postgres", "cobrape")
    uri.setDataSource("", "ottobacias_icr", "geom", "", "cobacia")
    ottobacias_icr = QgsVectorLayer(uri.uri(), 'camada_ottobacias_icr', "postgres")
    if not ottobacias_icr.isValid():
        print("Erro ao carregar camada")
    else:
        QgsProject.instance().addMapLayer(ottobacias_icr)
        print("Camada carregada com sucesso")
    
    campo = 'icr'
    indice = ottobacias_icr.fields().indexFromName(campo)
    unique_values = ottobacias_icr.uniqueValues(indice)
    cores_classes = {   '1': QColor(0, 150, 0, 150),
                        '2': QColor(0, 0, 150, 150),
                        '3': QColor(0, 0, 150, 150),
                        '4': QColor(0, 0, 150, 150),
                        '5': QColor(150, 0, 0, 150)}
    rotulos_classes = { '1': 'Sem criticidade',
                        '2': 'Baixo potencial de comprometimento',
                        '3': 'Médio potencial de comprometimento',
                        '4': 'Alto potencial de comprometimento',
                        '5': 'Déficit de atendimento às demandas'}
    categorias = []
    for value in unique_values:
        simbologia = QgsSymbol.defaultSymbol(ottobacias_icr.geometryType())
        categoria = QgsRendererCategory(value, simbologia, str(value))
        if str(value) in cores_classes:
            simbologia.setColor(cores_classes[str(value)])
        if str(value) in rotulos_classes:
            categoria.setLabel(rotulos_classes[str(value)])
        categorias.append(categoria)

    renderer = QgsCategorizedSymbolRenderer(campo, categorias)
    ottobacias_icr.setRenderer(renderer)
    ottobacias_icr.triggerRepaint()
    return ottobacias_icr


### EXECUÇÃO ###

ottobacias_icr = carregar_camada_balanco()
print('--> Carregamento de camada "'+ottobacias_icr.name()+'" Realizado.')