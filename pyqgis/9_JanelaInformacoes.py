import psycopg2

conexao = psycopg2.connect(
dbname = str(parametros_conexao['nome_bd']),
user = str(parametros_conexao['usuario_bd']),
password = str(parametros_conexao['senha_bd']),
host = str(parametros_conexao['host_bd']),
port = str(parametros_conexao['porta_bd']))
cursor = conexao.cursor()

cursor.execute(f'''SELECT cobacia FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
cod_otto_bacia = cursor.fetchone()[0]

def apresenta_informacoes(informacoes_selecao):
    janela_informacoes = QMessageBox()
    janela_informacoes.setWindowTitle('Resultado')
    janela_informacoes.setText('Informações sobre a área selecionado'
                           '\n'
                           '\n Cobacai: ' + str(informacoes_selecao['cobacia']) +
                           '\n Nome do rio: ' + str(informacoes_selecao['nome_rio']) +
                           '\n Área à montante: ' + str(informacoes_selecao['area_mont']) +
                           '\n Número de trechos à montante: ' + str(informacoes_selecao['n_trechos_mont']) +
                           '\n ISR da ottobacias: ' + str(informacoes_selecao['isr_otto']) +
                           '\n Vazão captada à montante: ' + str(informacoes_selecao['q_cap_mont']) +
                           '\n Disponibilidade à montante: ' + str(informacoes_selecao['disp_acum']))
    #verifica_postgis.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return_value = janela_informacoes.exec()
    print(return_value)


def obter_informacoes():
    informacoes_selecao = {'cobacia':'COBACIA',
                           'nome_rio':'-----',
                           'area_mont':'-----',
                           'n_trechos_mont':9999,
                           'isr_otto':'X',
                           'q_cap_mont':9999,
                           'disp_acum':9999}
    
    # Cobacia
    cursor.execute(f'''SELECT cobacia FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
    informacoes_selecao['cobacia'] = cursor.fetchone()[0]

    # Numero trechos montante
    cursor.execute(f'''SELECT COUNT(*) FROM {parametros_conexao['schema_cenario']}.ottobacias_montante''')
    informacoes_selecao['n_trechos_mont'] = cursor.fetchone()[0]

    
    # ISR da otto
    cursor.execute(f'''SELECT classe_isr FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
    print(cursor.fetchone()[0], type(cursor.fetchone()[0]))
    if cursor.fetchone()[0] == '1':
        isr = 'Sem criticidade'
    elif cursor.fetchone()[0] == '2':
        isr = 'Baixo potencial de comprometimento'
    elif cursor.fetchone()[0] == '3':
        isr = 'Médio potencial de comprometimento'
    elif cursor.fetchone()[0] == '4':
        isr = 'Alto potencial de comprometimento'
    elif cursor.fetchone()[0] == '6':
        isr = 'Déficit de atendimento às demandas'
    informacoes_selecao['isr_otto'] = isr
    

    # captacao acumulada
    cursor.execute(f'''SELECT captacao_acumulada FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
    informacoes_selecao['q_cap_mont'] = cursor.fetchone()[0]

    # disponibilidade montante
    cursor.execute(f'''SELECT vazao_natural FROM {parametros_conexao['schema_cenario']}.ottobacia_selecionada''')
    informacoes_selecao['disp_acum'] = cursor.fetchone()[0]

    return informacoes_selecao


### EXECUÇÃO ###

informacoes_selecao = obter_informacoes()
apresenta_informacoes(informacoes_selecao)