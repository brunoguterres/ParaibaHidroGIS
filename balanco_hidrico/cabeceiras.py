import pandas as pd

# Carregar o arquivo CSV
arquivo = pd.read_csv('C:/Users/bruno/OneDrive/Área de Trabalho/ottotrechos_pb_5k.csv')

# Inicializar a nova coluna 'cabeceira' com valor 'false'
arquivo['cabeceira'] = True

# Verificar cada linha
for index, row in arquivo.iterrows():
    cotrecho = row['cotrecho']
    if cotrecho in arquivo['nutrjus'].values:
        arquivo.at[index, 'cabeceira'] = False

# Salvar o DataFrame atualizado em um novo arquivo CSV
arquivo.to_csv('C:/Users/bruno/OneDrive/Área de Trabalho/ottotrechos_pb_5k_cabeceira.csv', index=False)
