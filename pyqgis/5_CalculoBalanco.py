def balanco():
    pass







### EXECUÇÃO ###

matriz_atributos = []
campos = disponibilidade_captacao.fields()

matriz_atributos.append([campo.name() for campo in campos])

for feicao in disponibilidade_captacao.getFeatures():
    matriz_atributos.append([feicao[campo.name()] for campo in campos])

print('\n''-> Cálculo do balanço hídrico realizado.')
