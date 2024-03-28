import csv
import psycopg2

def ler_arquivo_csv(nome_arquivo):
    matriz = []
    with open(nome_arquivo, newline='') as csvfile:
        leitor_csv = csv.reader(csvfile, delimiter=',')
        for linha in leitor_csv:
            matriz.append(linha)
    matriz.pop(0)
    return matriz

def operacao(matriz):
    for i in range(len(matriz)):
    #for i in range(7):
        #print('-'*20)
        #print('i:', i)
        if matriz[i][campo_cabeceira] == 'True':
            matriz[i][campo_q_nat] = matriz[i][campo_q_inc]
            #print('cabeceira!')
            #print('campo_q_nat:',  matriz[i][campo_q_nat])
        else:
            #print('NÃO é cabeceira!!!')
            valor_q_nat = float(matriz[i][campo_q_inc])
            #print('valor_inicial_q_nat:', valor_q_nat)
            for j in range(i-1,-1,-1):
                #print('j:', j)
                contador_montante = 0
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus] :
                    valor_q_nat += float(matriz[j][campo_q_nat])
                    matriz[i][campo_q_nat] = valor_q_nat
                    #print('campo_q_nat:',  valor_q_nat)
                    contador_montante += 1
                    if contador_montante == 2:
                        #print('valor_final_q_nat:', matriz[i][campo_q_nat])
                        #print('finalizou cálculo NAT!')
                        break
            
    return matriz

def salvar_resultado(matriz_resultado):
    conexao = psycopg2.connect(
        dbname='bdg_prh_rpb',
        user='postgres',
        password='guterres',
        host='localhost',
        port='5432')
    cursor = conexao.cursor()
    campos = ['cobacia',
              'cotrecho',
              'trechojus',
              'curso_dagua',
              'q_inc',
              'q_nat',
              'cabeceira']

    try:
        cursor.execute("""
            DROP VIEW IF EXISTS cenario_0.resultado CASCADE;
            CREATE VIEW cenario_0.resultado AS
            SELECT {}
            FROM (
                VALUES {}
            ) AS data({})
            ORDER BY cobacia DESC;
        """.format(
            ', '.join(['"' + campo + '"' for campo in campos]),  # Coloca os nomes dos campos entre aspas duplas
            ', '.join([str(tuple(row)) for row in matriz_resultado]),  # Converte cada linha da matriz em uma tupla para VALUES
            ', '.join(['"' + campo + '"' for campo in campos])  # Coloca os nomes dos campos entre aspas duplas para a parte AS data
        ))
        conexao.commit()
        print("Resultado salvo com sucesso!")
    except psycopg2.Error as e:
        print(f"Erro ao salvar o resultado: {e}")

    cursor.close()
    conexao.close()

### EXECUÇÃO ###

campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_curso_dagua = 3
campo_q_inc = 4
campo_q_nat = 5
campo_cabeceira = 6

nome_do_arquivo = 'teste.csv'
matriz = ler_arquivo_csv(nome_do_arquivo)

matriz_resultado = operacao(matriz)
salvar_resultado(matriz_resultado)
