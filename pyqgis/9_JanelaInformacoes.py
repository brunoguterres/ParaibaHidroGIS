def apresenta_informacoes(informacoes_selecao):
    verifica_postgis = QMessageBox()
    verifica_postgis.setWindowTitle('Resultado')
    verifica_postgis.setText('Informações sobre a área selecionado'
                           '\n'
                           '\n NOME DO RIO: ' + str(informacoes_selecao['nome_rio']) +
                           '\n ÁREA À MONTANTE: ' + str(informacoes_selecao['area_mont']) +
                           '\n NÚMERO DE TRECHOS À MONTANTE: ' + str(informacoes_selecao['n_trechos_mont']) +
                           '\n ISR DA OTTOBACIA: ' + str(informacoes_selecao['isr_otto']) +
                           '\n VAZÃO CAPTADA À MONTANTE: ' + str(informacoes_selecao['q_cap_mont']) +
                           '\n DISPONIBILIDADE À MONTANTE: ' + str(informacoes_selecao['disp_acum']))
    verifica_postgis.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return_value = verifica_postgis.exec()
    if return_value == QMessageBox.No:
        parametros_conexao = parametros_personalizados_bd(parametros_conexao)
    return parametros_conexao

def obter_informacoes():
    informacoes_selecao = {'nome_rio':'RIO',
                           'area_montante':9999,
                           'n_trechos_mont':9999,
                           'isr_otto':'X',
                           'q_cap_mont':9999,
                           'disp_acum':9999}
    return informacoes_selecao


### EXECUÇÃO ###

informacoes_selecao = obter_informacoes()
apresenta_informacoes(informacoes_selecao)