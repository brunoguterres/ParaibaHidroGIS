import psycopg2

def criar_matriz_balanco():
    matriz = []
    campos = trecho_disponibilidade_captacao.fields()
    matriz.append([campo.name() for campo in campos])
    for feicao in trecho_disponibilidade_captacao.getFeatures():
        matriz.append([feicao[campo.name()] for campo in campos])
    matriz.pop(0)
    for linha in matriz:
        linha.append(0)
        linha.append(0)
        linha.append(0)
        linha.append(0)
    return matriz

def criar_matriz():
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM cenario_0.dados_balanco;")
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
    return matriz

def calcular_balanco(matriz):
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == 'True':
            matriz[i][campo_vazao_jusante] = float(matriz[i][campo_vazao_incremental])-float(matriz[i][campo_captacao_solicitada])
            if matriz[i][campo_vazao_jusante] < 0:
                matriz[i][campo_deficit] = matriz[i][campo_vazao_jusante]*-1
                matriz[i][campo_vazao_jusante] = 0
               
            '''
            if matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=0.20:
                matriz[i][campo_isr] = 1
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>0.20 and matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=0.40:
                matriz[i][campo_isr] = 2
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>0.40 and matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=0.70:
                matriz[i][campo_isr] = 3
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>0.70 and matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=1:
                matriz[i][campo_isr] = 4
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>1:
                matriz[i][campo_isr] = 5
            '''

        else:
            for j in range(i-1,-1,-1):
                contador_montante = 0
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus] :
                    matriz[i][campo_vazao_montante] += float(matriz[j][campo_vazao_jusante])
                    vazao_jusante = float(matriz[i][campo_vazao_montante])+float(matriz[i][campo_vazao_incremental])-float(matriz[i][campo_captacao_solicitada])
                    if vazao_jusante < 0:
                        matriz[i][campo_vazao_jusante] = 0
                        matriz[i][campo_deficit] = vazao_jusante*-1
                    else:
                        matriz[i][campo_vazao_jusante] = vazao_jusante
                    contador_montante += 1
                    if contador_montante == 2:
                        break
            '''
            disp_total = matriz[i][campo_vazao_montante]+matriz[i][campo_disponibilidade]            
            if matriz[i][campo_captacao]/disp_total<=0.20:
                matriz[i][campo_isr] = 1
            elif matriz[i][campo_captacao]/disp_total>0.20 and matriz[i][campo_captacao]/disp_total<=0.40:
                matriz[i][campo_isr] = 2
            elif matriz[i][campo_captacao]/disp_total>0.40 and matriz[i][campo_captacao]/disp_total<=0.70:
                matriz[i][campo_isr] = 3
            elif matriz[i][campo_captacao]/disp_total>0.70 and matriz[i][campo_captacao]/disp_total<=1:
                matriz[i][campo_isr] = 4
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>1:
                matriz[i][campo_isr] = 5
            '''
            
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
                'vazao_naturalizada',
                'captacao_solicitada',
                'campo_vazao_montante',
                'campo_vazao_jusante',
                'campo_captacao_atendida',
                'campo_captacao_acumulada',
                'campo_deficit',
                'isr']
    
    cursor.execute(f"""
        DROP VIEW IF EXISTS resultado_balanco CASCADE;
        CREATE VIEW resultado_balanco AS
        SELECT {', '.join(campos)}
        FROM (
            VALUES {', '.join([f"('{row[0]}', {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9], {row[8]}})" for row in matriz_balanco])}
        ) AS data({', '.join(campos)})
    """)

    conexao.commit()
    cursor.execute(f"""
        DROP VIEW IF EXISTS ottobacias_isr CASCADE;
        CREATE VIEW ottobacias_isr AS
        SELECT 
            ottobacias_pb_5k.cobacia,
            ottobacias_pb_5k.geom,
            resultado_balanco.isr
        FROM 
            ottobacias_pb_5k
        LEFT JOIN resultado_balanco
            ON ottobacias_pb_5k.cobacia = resultado_balanco.cobacia;
    """)
    conexao.commit()
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_cabeceira = 3
campo_vazao_incremental = 4
campo_vazao_naturalizada = 5
campo_captacao_solicitada = 6
campo_vazao_montante = 7
campo_vazao_jusante = 8
campo_captacao_atendida = 9
campo_captacao_acumulada = 10
campo_deficit = 11
campo_isr = 12

matriz = criar_matriz()
matriz_balanco = calcular_balanco(matriz)
salvar_resultado(matriz_balanco)

print('--> Cálculo do balanço hídrico realizado.')