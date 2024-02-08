def criar_campos(matriz):
    for linha in matriz:
        linha.append(0)
        linha.append(0)
        linha.append(0)
    return matriz

def calcular_balanco(matriz):
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == True:
            pass
        else:
            for j in range(i-1,0,-1):
                contador_montante = 0
                if matriz[i][campo_cotrecho] == matriz[j][campo_trechojus] :
                    a = float(matriz[i][campo_vazao_montante])
                    a += float(matriz[j][campo_vazao_jusante])
                    contador_montante += 1
                    if contador_montante == 2:
                        break
        matriz[i][campo_vazao_jusante] = float(matriz[i][campo_vazao_montante]) + float(matriz[i][campo_disponibilidade])
    return matriz

def print_matriz(matriz):
    for row in matriz:
        print(" ".join(map(str, row)))


### EXECUÇÃO ###

matriz = []
for feicao in trecho_disponibilidade_captacao.getFeatures():
    matriz.append([feicao[campo.name()] for campo in campos])

matriz = criar_campos(matriz)

campo_cobacia = 0
campo_cotrecho = 1
campo_trechojus = 2
campo_cabeceira = 3
campo_disponibilidade = 4
campo_captacao = 5
campo_vazao_montante = 6
campo_vazao_jusante = 7
campo_deficit = 8

resultado_balanco = calcular_balanco(matriz)

print_matriz(resultado_balanco)

print('\n''-> Cálculo do balanço hídrico realizado.')
