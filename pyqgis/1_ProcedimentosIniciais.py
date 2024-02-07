def parametros_padrao_bd():
# função que define os parâmetros padrão de conexão com banco de dados
    parametros_conexao = {'host_bd': 'localhost',
                          'nome_bd': 'bdg_prh_rpb',
                          'usuario_bd': 'postgres',
                          'senha_bd': 'cobrape',
                          'porta_bd': '5432',
                          'schema_bd': 'public'}
    status = '-> Parâmetros PADRÃO de conexão definidos.'
    return parametros_conexao, status

def verifica_parametros_bd(parametros_conexao, status):
#função que apresenta os parâmetros de conexão com banco de dados
    verifica_postgis = QMessageBox()
    verifica_postgis.setText('Deseja continuar com os parâmetros de conexão abaixo?'
                           '\n'
                           '\n''host: ' + str(parametros_conexao['host_bd']) +
                           '\n''nome: ' + str(parametros_conexao['nome_bd']) +
                           '\n''usuario: ' + str(parametros_conexao['usuario_bd']) +
                           '\n''senha: ' + str(parametros_conexao['senha_bd']) +
                           '\n''porta: ' + str(parametros_conexao['porta_bd']) +
                           '\n''schema: ' + str(parametros_conexao['schema_bd']))
    verifica_postgis.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return_value = verifica_postgis.exec()
    if return_value == QMessageBox.No:
        parametros_conexao, status = parametros_personalizados_bd(parametros_conexao)
    print(status)
    return parametros_conexao

def parametros_personalizados_bd(parametros_conexao):
# função de personalização dos parâmetros de conexão com banco de dados 
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
    status = '-> Parâmetros PERSONALIZADOS de conexão definidos.'
    verifica_parametros_bd(parametros_conexao, status)
    return parametros_conexao, status

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
    print(mensagem_saida_limpeza)

### EXECUÇÃO ###

parametros_conexao, status = parametros_padrao_bd()
parametros_conexao = verifica_parametros_bd(parametros_conexao, status)
limpeza_residuos()