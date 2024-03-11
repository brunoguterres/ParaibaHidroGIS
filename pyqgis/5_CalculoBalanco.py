import psycopg2
#from PyQt5.QtGui import QColor

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

def calcular_balanco(matriz):
    for i in range(len(matriz)):
        if matriz[i][campo_cabeceira] == 'True':
            matriz[i][campo_vazao_jusante] = float(matriz[i][campo_disponibilidade])-float(matriz[i][campo_captacao])
            if matriz[i][campo_vazao_jusante] < 0:
                matriz[i][campo_vazao_jusante] = 0
                matriz[i][campo_deficit] = vazao_jusante*-1
            
            if matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=0.20:
                matriz[i][campo_icr] = 1
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>0.20 and matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=0.40:
                matriz[i][campo_icr] = 2
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>0.40 and matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=0.70:
                matriz[i][campo_icr] = 3
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>0.70 and matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]<=1:
                matriz[i][campo_icr] = 4
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>1:
                matriz[i][campo_icr] = 5
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
            
            disp_total = matriz[i][campo_vazao_montante]+matriz[i][campo_disponibilidade]            
            if matriz[i][campo_captacao]/disp_total<=0.20:
                matriz[i][campo_icr] = 1
            elif matriz[i][campo_captacao]/disp_total>0.20 and matriz[i][campo_captacao]/disp_total<=0.40:
                matriz[i][campo_icr] = 2
            elif matriz[i][campo_captacao]/disp_total>0.40 and matriz[i][campo_captacao]/disp_total<=0.70:
                matriz[i][campo_icr] = 3
            elif matriz[i][campo_captacao]/disp_total>0.70 and matriz[i][campo_captacao]/disp_total<=1:
                matriz[i][campo_icr] = 4
            elif matriz[i][campo_captacao]/matriz[i][campo_disponibilidade]>1:
                matriz[i][campo_icr] = 5
            
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
                'deficit',
                'icr']
    
    # Criar uma view a partir da matriz
    cursor.execute(f"""
        DROP VIEW IF EXISTS resultado_balanco CASCADE;
        CREATE VIEW resultado_balanco AS
        SELECT {', '.join(campos)}
        FROM (
            VALUES {', '.join([f"('{row[0]}', {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]})" for row in matriz_balanco])}
        ) AS data({', '.join(campos)})
    """)

    conexao.commit()

    cursor.execute(f"""
        DROP VIEW IF EXISTS ottobacias_icr CASCADE;
        CREATE VIEW ottobacias_icr AS
        SELECT 
            ottobacias_pb_5k.cobacia,
            ottobacias_pb_5k.geom,
            resultado_balanco.icr
        FROM 
            ottobacias_pb_5k
        LEFT JOIN resultado_balanco
            ON ottobacias_pb_5k.cobacia = resultado_balanco.cobacia;
    """)

    # Commitar as operações
    conexao.commit()

    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()

def carregar_camada_balanco():

    # Configuração da conexão com o banco de dados PostGIS
    uri = QgsDataSourceUri()
    uri.setConnection("localhost", "5432", "bdg_prh_rpb", "postgres", "cobrape")
    view_name = "ottobacias_icr"
    uri.setDataSource("", "ottobacias_icr", "geom", "", "cobacia")
    layer = QgsVectorLayer(uri.uri(), view_name, "postgres")
    if not layer.isValid():
        print("Erro ao carregar camada")
    else:
        # Adicione a camada ao projeto
        QgsProject.instance().addMapLayer(layer)
        print("Camada carregada com sucesso")
    
    layer = QgsProject.instance().mapLayersByName('ottobacias_icr')[0]

    field_name = 'icr'
    field_index = layer.fields().indexFromName(field_name)
    unique_values = layer.uniqueValues(field_index)

    # Define cores específicas para cada classe
    color_dict = {
        '1': QColor('#FF0000'),  # Vermelho para classe 1
        '2': QColor('#00FF00'),  # Verde para classe 2
        '5': QColor('#0000FF')   # Azul para classe 5
    }

    # create category list
    category_list = []
    for value in unique_values:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        category = QgsRendererCategory(value, symbol, str(value))
        
        # Define cor específica para cada categoria
        if str(value) in color_dict:
            symbol.setColor(color_dict[str(value)])
            
        category_list.append(category)

    # create renderer by specifying category list
    renderer = QgsCategorizedSymbolRenderer(field_name, category_list)
    layer.setRenderer(renderer)

    # trigger repaint
    layer.triggerRepaint()



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
campo_icr = 9

matriz = criar_matriz_balanco()
matriz_balanco = calcular_balanco(matriz)
criar_resultado(matriz_balanco)

carregar_camada_balanco()

print('--> Cálculo do balanço hídrico realizado.')