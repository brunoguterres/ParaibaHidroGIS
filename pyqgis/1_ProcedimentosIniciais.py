def parametros_BDG():
# função que define os parâmetros de entrada do banco de dados 
    parametros_conexao = {'host_bd': 'localhost',
                          'nome_bd': 'bdg_prh_rpb',
                          'usuario_bd': 'postgres',
                          'senha_bd': 'cobrape',
                          'porta_bd': '5432',
                          'schema_bd': 'public'}

    verify_postgis = QMessageBox()
    verify_postgis.setText('Deseja continuar com os parâmetros de conexão padrão?'
                           '\n'
                           '\n''host: ' + str(parametros_conexao['host_bd']) +
                           '\n''nome: ' + str(parametros_conexao['nome_bd']) +
                           '\n''usuario: ' + str(parametros_conexao['usuario_bd']) +
                           '\n''senha: ' + str(parametros_conexao['senha_bd']) +
                           '\n''porta: ' + str(parametros_conexao['porta_bd']) +
                           '\n''schema: ' + str(parametros_conexao['schema_bd']))
    verify_postgis.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
 
    if verify_postgis.exec() == QMessageBox.Yes:
        pass
    elif verify_postgis.exec() == QMessageBox.No:
        parametro_entrada = QInputDialog().getText(None,
                                                   'Parâmetro de conexão',
                                                   'Digite o host:')
        if parametro_entrada[0] != '':
            parametros_conexao['host_bd'] = parametro_entrada[0]
        
        parametro_entrada = QInputDialog().getText(None,
                                                   'Parâmetro de conexão',
                                                   'Digite o nome do banco:')
        if parametro_entrada[0] != '':
            parametros_conexao['nome_bd'] = parametro_entrada[0]
        
        parametro_entrada = QInputDialog().getText(None,
                                                   'Parâmetro de conexão',
                                                   'Digite o usuário:')
        if parametro_entrada[0] != '':
            parametros_conexao['usuario_bd'] = parametro_entrada[0]
        
        parametro_entrada = QInputDialog().getText(None,
                                                   'Parâmetro de conexão',
                                                   'Digite a senha:')
        if parametro_entrada[0] != '':
            parametros_conexao['senha_bd'] = parametro_entrada[0]
        
        parametro_entrada = QInputDialog().getText(None,
                                                   'Parâmetro de conexão',
                                                   'Digite o número da porta:')
        if parametro_entrada[0] != '':
            parametros_conexao['porta_bd'] = parametro_entrada[0]
        
        parametro_entrada = QInputDialog().getText(None,
                                                   'Parâmetro de conexão',
                                                   'Digite o schema:')
        if parametro_entrada[0] != '':
            parametros_conexao['schema_bd'] = parametro_entrada[0]
    
    print(parametros_conexao)
    print('-> Parâmetros de entrada definidos.')
    return parametros_conexao

def limpeza_residuos():
    #   função de exclusao de camadas residuais do projeto
    camada_residual = QgsProject.instance().mapLayers().values()
    lista_camadas_residuais = [l for l in camada_residual]
    if len(lista_camadas_residuais) > 0:
        for camada in lista_camadas_residuais:
            QgsProject.instance().removeMapLayer(camada)
        mensagem_saida_limpeza = '--> Limpeza de camadas residuais de execuções anteriores realizada!'
    else:
        mensagem_saida_limpeza = '--> Não existem camadas residuais de execuções anteriores.'
        canvas = qgis.utils.iface.mapCanvas()
        canvas.refresh()
        print('\n''-> Limpeza de camadas realizada.')
        return mensagem_saida_limpeza

### EXECUÇÃO ###

parametros_conexao = parametros_BDG()
#limpeza_residuos()