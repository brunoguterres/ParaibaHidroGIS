def criar_campos(matriz):
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

def print_matriz(matriz):
    for row in matriz:
        print(" ".join(map(str, row)))

def print_matriz_2(matriz):
    for row in matriz:
        for item in row:
            print(f"{item} ({type(item).__name__})", end=" ")
        print()



### EXECUÇÃO ###

matriz = []

campos = trecho_disponibilidade_captacao.fields()
matriz.append([campo.name() for campo in campos])
for feicao in trecho_disponibilidade_captacao.getFeatures():
    matriz.append([feicao[campo.name()] for campo in campos])

matriz.pop(0)
matriz = criar_campos(matriz)
#print_matriz_2(matriz)

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
#print_matriz(resultado_balanco)

print('--> Cálculo do balanço hídrico realizado.')