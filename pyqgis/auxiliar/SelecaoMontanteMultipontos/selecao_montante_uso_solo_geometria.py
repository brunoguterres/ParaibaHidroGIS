pontos_monitoramento = QgsProject.instance().mapLayersByName('intersecao_pontos_monitoramento_ottobacias')[0]

for ponto in pontos_monitoramento.getFeatures():
    cod_otto = ponto['cobacia']
    #print('cod_otto:', cod_otto)

    if (int(cod_otto) % 2) == 0:
        cod_otto_e = cod_otto
        #print('cod_otto_e:', cod_otto_e)
    else:
        for letra in range(len(cod_otto)):
            index = (letra + 1) * -1
            conv_num = int(cod_otto[index])
            resto = conv_num % 2        
            if resto == 0:
                cod_otto_e = cod_otto[:(index + 1)]
                print('cod_otto_e:', cod_otto_e)
                break

    sql = f'''
            SELECT classe, geometry
            FROM intersecao_uso_solo_ottobacias
            WHERE cobacia LIKE '{cod_otto_e}%' AND cobacia >= '{cod_otto}';
            '''
    camada_virtual = QgsVectorLayer("?query={}".format(sql), "selecao_montante_" + str(cod_otto), "virtual")
    #QgsProject.instance().addMapLayer(camada_virtual)

    caminho_saida = f'C:/Users/brunoguterres/Desktop/analises_william/resultados/uso_solo/geometria/selecao_montante_{cod_otto}.shp'
    QgsVectorFileWriter.writeAsVectorFormat(camada_virtual, caminho_saida, "UTF-8", camada_virtual.crs(), "ESRI Shapefile")

print('OPERAÇÃO FINALIZADA!!!')

iface.mapCanvas().refresh()
