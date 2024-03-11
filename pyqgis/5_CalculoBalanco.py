import psycopg2
import numpy as np

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
    return matriz

def calcular_balanco(matriz):
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == 'True':
            matriz[i][campo_vazao_jusante] = float(matriz[i][campo_disponibilidade])-float(matriz[i][campo_captacao])
        else:
            for j in range(i-1,-1,-1):
                contador_montante = 0
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus] :
                    matriz[i][campo_vazao_montante] += float(matriz[j][campo_vazao_jusante])
                    vazao_jusante = float(matriz[i][campo_vazao_montante])+float(matriz[i][campo_disponibilidade])-float(matriz[i][campo_captacao])
                    if vazao_jusante < 0:
                        matriz[i][campo_vazao_jusante] = 0
                        matriz[i][campo_deficit] = vazao_jusante*-1
                    else:
                        matriz[i][campo_vazao_jusante] = vazao_jusante
                    contador_montante += 1
                    if contador_montante == 2:
                        break
    return matriz

def criar_resultado(matriz_balanco):
    conexao = psycopg2.connect(
        dbname = str(parametros_conexao['nome_bd']),
        user = str(parametros_conexao['usuario_bd']),
        password = str(parametros_conexao['senha_bd']),
        host = str(parametros_conexao['host_bd']),
        port = str(parametros_conexao['porta_bd']))
    cursor = conexao.cursor()

    # Adicione campos à camada
    campos =   ['cobacia',
                'cotrecho',
                'trechojus',
                'cabeceira',
                'disponibilidade',
                'captacao',
                'vazao_montante',
                'vazao_jusante',
                'deficit']
    
    # Criar uma view a partir da matriz
    cursor.execute(f"""
        DROP VIEW IF EXISTS resultado_balanco;
        CREATE VIEW resultado_balanco AS
        SELECT {', '.join(campos)}
        FROM (
            VALUES {', '.join([f"('{row[0]}', {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]})" for row in matriz_balanco])}
        ) AS data({', '.join(campos)})
    """)

    # Commitar as operações
    conexao.commit()

    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()


### EXECUÇÃO ###

campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_cabeceira = 3
campo_disponibilidade = 4
campo_captacao = 5
campo_vazao_montante = 6
campo_vazao_jusante = 7
campo_deficit = 8

matriz = criar_matriz_balanco()
matriz_balanco = calcular_balanco(matriz)
criar_resultado(matriz_balanco)

print('--> Cálculo do balanço hídrico realizado.')