import psycopg2, time

def criar_matriz():
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()
    cursor.execute(f'''SELECT *
                   FROM {parametros_conexao['schema_cenario']}.dados_balanco
                   ORDER BY cobacia DESC;''')   # Garantir a ordenação de montante para jusante
    rows = cursor.fetchall()
    matriz = []
    for row in rows:
        row_as_list = [str(value) for value in row]  # Converter todos os valores para string
        matriz.append(row_as_list)
    cursor.close()
    conexao.close()
    for linha in matriz:
        linha.append(0)
        linha.append(0)
        linha.append(0)
        linha.append(0)
        linha.append(0)
        linha.append(0)
        linha.append(0)
    return matriz

def calcular_balanco(matriz):
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == 'True':
            matriz[i][campo_vazao_jusante] = float(matriz[i][campo_vazao_incremental])-float(matriz[i][campo_captacao_solicitada])
            if matriz[i][campo_vazao_jusante] < 0:
                matriz[i][campo_deficit] = matriz[i][campo_vazao_jusante] * -1
                matriz[i][campo_vazao_jusante] = 0
                matriz[i][campo_captacao_atendida] = float(matriz[i][campo_captacao_solicitada]) - matriz[i][campo_deficit]
            else:
                matriz[i][campo_captacao_atendida] = float(matriz[i][campo_captacao_solicitada])
                matriz[i][campo_deficit] = 0
            matriz[i][campo_captacao_acumulada] = matriz[i][campo_captacao_atendida]
        else:
            contador_montante = 0
            for j in range(i-1,-1,-1):
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus]:
                    matriz[i][campo_vazao_montante] += float(matriz[j][campo_vazao_jusante])
                    matriz[i][campo_vazao_jusante] = float(matriz[i][campo_vazao_montante])+float(matriz[i][campo_vazao_incremental])-float(matriz[i][campo_captacao_solicitada])
                    if matriz[i][campo_vazao_jusante] < 0:
                        matriz[i][campo_deficit] = matriz[i][campo_vazao_jusante] * -1
                        matriz[i][campo_vazao_jusante] = 0
                        matriz[i][campo_captacao_atendida] = float(matriz[i][campo_captacao_solicitada]) - matriz[i][campo_deficit]
                    else:
                        matriz[i][campo_captacao_atendida] = float(matriz[i][campo_captacao_solicitada])
                        matriz[i][campo_deficit] = 0
                    matriz[i][campo_captacao_acumulada] = float(matriz[i][campo_captacao_acumulada])
                    matriz[i][campo_captacao_acumulada] += matriz[j][campo_captacao_acumulada]
                    contador_montante += 1
                    if contador_montante == 2:
                        matriz[i][campo_captacao_acumulada] += matriz[i][campo_captacao_atendida]
                        break
        matriz[i][campo_isr] = (matriz[i][campo_captacao_acumulada]+float(matriz[i][campo_deficit]))/float(matriz[i][campo_vazao_natural])
        if matriz[i][campo_isr] <= 0.2:
            matriz[i][campo_classe_isr] = '1'
        elif matriz[i][campo_isr] > 0.2 and matriz[i][campo_isr] <= 0.4:
            matriz[i][campo_classe_isr] = '2'
        elif matriz[i][campo_isr] > 0.4 and matriz[i][campo_isr] <= 0.7:
            matriz[i][campo_classe_isr] = '3'
        elif matriz[i][campo_isr] > 0.7 and matriz[i][campo_isr] <= 1:
            matriz[i][campo_classe_isr] = '4'
        elif matriz[i][campo_isr] > 1:
            matriz[i][campo_classe_isr] = '5'
    return matriz

def salvar_resultado(matriz_balanco):
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()
    campos =   ['cobacia',
                'cotrecho',
                'trechojus',
                'cabeceira',
                'vazao_incremental',
                'vazao_natural',
                'captacao_solicitada',
                'vazao_montante',
                'vazao_jusante',
                'captacao_atendida',
                'captacao_acumulada',
                'deficit',
                'isr',
                'classe_isr']
    
    cursor.execute(f'''
        DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.resultado_balanco CASCADE;
        CREATE VIEW {parametros_conexao['schema_cenario']}.resultado_balanco AS
        SELECT {', '.join(campos)}
        FROM (
            VALUES {', '.join([f"('{campo[0]}', {campo[1]}, {campo[2]}, {campo[3]}, {campo[4]}, {campo[5]}, {campo[6]}, {campo[7]}, {campo[8]}, {campo[9]}, {campo[10]}, {campo[11]}, {campo[12]}, '{campo[13]}')" for campo in matriz_balanco])}
        ) AS data({', '.join(campos)})
        ORDER BY cobacia DESC;
    ''')
    conexao.commit()

    cursor.execute(f'''
        DROP VIEW IF EXISTS {parametros_conexao['schema_cenario']}.ottobacias_isr CASCADE;
        CREATE VIEW {parametros_conexao['schema_cenario']}.ottobacias_isr AS
        SELECT 
            {basemap}.ottobacias_pb_5k.cobacia,
            {basemap}.ottobacias_pb_5k.geom,
            {parametros_conexao['schema_cenario']}.resultado_balanco.isr,
            {parametros_conexao['schema_cenario']}.resultado_balanco.classe_isr
        FROM {basemap}.ottobacias_pb_5k
        LEFT JOIN {parametros_conexao['schema_cenario']}.resultado_balanco
            ON {basemap}.ottobacias_pb_5k.cobacia = {parametros_conexao['schema_cenario']}.resultado_balanco.cobacia;
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

tempo_inicial = time.time() # Apenas para finalidade de apresentação do tempo

campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_cabeceira = 3
campo_vazao_incremental = 4
campo_vazao_natural = 5
campo_captacao_solicitada = 6
campo_vazao_montante = 7
campo_vazao_jusante = 8
campo_captacao_atendida = 9
campo_captacao_acumulada = 10
campo_deficit = 11
campo_isr = 12
campo_classe_isr = 13

matriz = criar_matriz()
tempo_matriz = time.time()              # Apenas para finalidade de apresentação do tempo
matriz_balanco = calcular_balanco(matriz)
tempo_balanco = time.time()             # Apenas para finalidade de apresentação do tempo
salvar_resultado(matriz_balanco)
tempo_salvar_resultado = time.time()    # Apenas para finalidade de apresentação do tempo
print('--> Cálculo do balanço hídrico realizado.')
print('>>> TEMPOS <<<:\n'
      '> Criação da matriz:', round(tempo_matriz - tempo_inicial, 2), 'segundos\n'
      '> Cálculo do balanço:', round(tempo_balanco - tempo_matriz, 2), 'segundos\n'
      '> Salvar resultado:', round(tempo_salvar_resultado - tempo_balanco, 2), 'segundos\n'
      '> TOTAL da execução:', round(time.time() - tempo_inicial, 2), 'segundos')
