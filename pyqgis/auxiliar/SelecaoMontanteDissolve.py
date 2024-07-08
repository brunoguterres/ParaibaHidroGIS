#   seleção das sub bacias a montante e depois um dissolve
    consulta_bacias = "?query=SELECT base_otto_bacias.cobacia, base_otto_bacias.geometry FROM base_otto_bacias WHERE base_otto_bacias.cobacia LIKE '"+ cod_otto_e +"%' AND base_otto_bacias.cobacia >= '"+ cod_otto +"'"
    sub_bacia_montante = QgsVectorLayer(consulta_bacias, "sub_bacias_montante", "virtual")
    outputDissolve = 'C:/Gis/shp/Tipai/disso_bacia.shp'
    parametersDissolve ={'INPUT':sub_bacia_montante,'OUTPUT':outputDissolve}
    processing.run("qgis:dissolve",parametersDissolve)
 
    
    bacia = QgsVectorLayer(outputDissolve, 'bacia', 'ogr')
    symbol = QgsFillSymbol.createSimple({'color': '0,0,0,0',
                                     'outline_color': '255,0, 0, 255',
                                     'outline_width': '1'})
    bacia.renderer().setSymbol(symbol)
 
    QgsProject.instance().addMapLayer(bacia)  