def criar_campos(matriz):   # esta função cria campos novos na matriz que serão necessários no cálculo do balanço
    for linha in matriz:
        linha.append(0)  # adiciona um atributo "0" no final de cada linha da linha - campo_vazao_montante
        linha.append(0)  # adiciona um atributo "0" no final de cada linha da linha - campo_vazao_jusante
    return matriz

def calculo_balanco(matriz): #esta função realiza o cálculo do balanço
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == '1':
            pass
        else:
            for j in range(i-1,-1,-1):
                contador_montante = 0
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus] :
                    a = float(matriz[i][campo_vazao_montante])
                    a += float(matriz[j][campo_vazao_jusante])
                    contador_montante += 1
                    if contador_montante == 2:
                        break
        matriz[i][campo_vazao_jusante] = float(matriz[i][campo_vazao_montante]) + float(matriz[i][campo_disponibilidade])
    return matriz.tolist()


### EXECUÇÃO ###

matriz = []
campos = trecho_disponibilidade_captacao.fields()
matriz.append([campo.name() for campo in campos])

for feicao in trecho_disponibilidade_captacao.getFeatures():
    matriz.append([feicao[campo.name()] for campo in campos])

matriz = criar_campos(matriz)
print(matriz)


campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_cabeceira = 3
campo_disponibilidade = 4
campo_captacao = 5
campo_vazao_montante = 6
campo_vazao_jusante = 7
campo_deficit = 8

'''
resultado_balanco = calculo_balanco(matriz)
'''
print('\n''-> Cálculo do balanço hídrico realizado.')
