def parametros_padrao_bd():
    parametros_conexao = {'nome_bd': 'bdg_prh_rpb',
                          'usuario_bd': 'paraiba',
                          'senha_bd': 'paraiba2024',
                          'host_bd': 'postgre-cwb.postgres.database.azure.com',
                          'porta_bd': '5432',
                          'schema_cenario': 'cenario_2'}
    return parametros_conexao

def verifica_parametros_bd(parametros_conexao):
    verifica_postgis = QMessageBox()
    verifica_postgis.setWindowTitle('Conexão com Banco de Dados')
    verifica_postgis.setText('Deseja continuar com os parâmetros de conexão abaixo?'
                           '\n'
                           '\n NOME: ' + str(parametros_conexao['nome_bd']) +
                           '\n USUÁRIO: ' + str(parametros_conexao['usuario_bd']) +
                           '\n SENHA: ' + str(parametros_conexao['senha_bd']) +
                           '\n HOST: ' + str(parametros_conexao['host_bd']) +
                           '\n PORTA: ' + str(parametros_conexao['porta_bd']))
    verifica_postgis.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return_value = verifica_postgis.exec()
    if return_value == QMessageBox.No:
        parametros_conexao = parametros_personalizados_bd(parametros_conexao)
    return parametros_conexao

def parametros_personalizados_bd(parametros_conexao):
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
    verifica_parametros_bd(parametros_conexao)
    return parametros_conexao

def definir_cenario(parametros_conexao):
    escolha_cenario = QMessageBox()
    escolha_cenario.setWindowTitle('Definição de cenário')
    escolha_cenario.setText('O cenário definido é:\n'
                            '\n'
                            '< ' + parametros_conexao['schema_cenario'] + ' >\n'
                            '\n'
                            'Deseja manter o cenário?')
    escolha_cenario.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return_value = escolha_cenario.exec()
    if return_value == QMessageBox.No:
        novo_cenario = QInputDialog().getText(None,
                                               'Escolha um cenário',
                                               'Digite o nome do cenário:')
        if novo_cenario[0] != '':
            parametros_conexao['schema_cenario'] = novo_cenario[0]
            confirmacao_cenario = QMessageBox()
            confirmacao_cenario.setWindowTitle('Definição de cenário')
            confirmacao_cenario.setText('O novo cenário escolhido é:\n'
                                        '\n'
                                        '< ' + parametros_conexao['schema_cenario'] + ' >')
            confirmacao_cenario.exec()
    return parametros_conexao

### EXECUÇÃO ###

basemap = 'basemap'
parametros_conexao = parametros_padrao_bd()
parametros_conexao = verifica_parametros_bd(parametros_conexao)
parametros_conexao = definir_cenario(parametros_conexao)
print('--> Parâmetros de conexão definidos.')
