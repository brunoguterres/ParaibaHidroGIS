import psycopg2

def carregar_camada(camada, simbologia):
    tipo_geometria = camada.geometryType()
    if tipo_geometria == QgsWkbTypes.PointGeometry:
        symbol = QgsSimpleMarkerSymbolLayer.create({
            'color': simbologia['cor'],
            'size': simbologia['tamanho']
        })
    elif tipo_geometria == QgsWkbTypes.LineGeometry:
        symbol = QgsLineSymbol.createSimple({
            'color': simbologia['cor'],
            'width': simbologia['espessura']
        })
    elif tipo_geometria == QgsWkbTypes.PolygonGeometry:
        symbol = QgsFillSymbol.createSimple({
            'color': simbologia['cor_preenchimento'],
            'color_border': simbologia['cor_contorno'],
            'width_border': simbologia['espessura_contorno']
        })
    renderer = QgsSingleSymbolRenderer(symbol)
    camada.setRenderer(renderer)
    QgsProject.instance().addMapLayer(camada)
    print(f'--> Carregamento de "{camada.name()}" realizado.')


### EXECUÇÃO ###

conexao = psycopg2.connect(
dbname = str(parametros_conexao['nome_bd']),
user = str(parametros_conexao['usuario_bd']),
password = str(parametros_conexao['senha_bd']),
host = str(parametros_conexao['host_bd']),
port = str(parametros_conexao['porta_bd']))
cursor = conexao.cursor()

if (int(cod_otto_bacia) % 2) == 0:
    cod_otto_e = cod_otto_bacia
else:
    for letra in range(len(cod_otto_bacia)):
        index = (letra + 1) * -1
        conv_num = int(cod_otto_bacia[index])
        resto = conv_num % 2
        if resto == 0:
            cod_otto_e = cod_otto_bacia[:(index + 1)]
            break

ottobacias_isr_montante = QgsVectorLayer(f'''VirtualLayer?query=
                                                SELECT *
                                                FROM camada_ottobacias_isr
                                                WHERE camada_ottobacias_isr.cobacia LIKE '{cod_otto_e}%' AND camada_ottobacias_isr.cobacia >= '{cod_otto_bacia}';''',
                                            'camada_ottobacias_isr_montante',
                                            'virtual')

if QgsProject.instance().mapLayersByName('camada_ottobacias_isr_montante'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ottobacias_isr_montante')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
QgsProject.instance().addMapLayer(ottobacias_isr_montante, False)
print(f'--> Carregamento de "{ottobacias_isr_montante.name()}" realizado.')

bacia_montante = QgsVectorLayer(f'''VirtualLayer?query=
                                    SELECT ST_UNION(geometry)
                                    FROM camada_ottobacias_isr_montante''',
                                'camada_bacia_montante',
                                'virtual')

# inicio da plotagem do trecho de jusante - apenas o jusante 1 no estilo antigo
# calculo dos rios que estão a jusante
# variáveis para o trecho de jusante - estão sendo definidas aqui para não dar erro
rio = ['','','','','','']
rios = 0
compri= 4
# seleção dos rios a jusante
for valor in range(len(cod_otto_bacia)):
    index = (valor + 1) * -1
    algarismo = int(cod_otto_bacia[index])
    impar = algarismo % 2
    codf = cod_otto_bacia[:(len(cod_otto_bacia)-valor)]
    if impar == 0:
        codfim = cod_otto_bacia[:(len(cod_otto_bacia)-valor)]
        rio[rios] = codfim
        rios = rios + 1
        compri = len(codfim)
# adição do shape do trechos de jusante
selecao = ""
for elementos in rio:
    if elementos != '':
        selecao = selecao + "camada_ottotrechos.curso_dagua LIKE '"+ elementos +"' OR "
    else:
        break
comp = len(selecao)
comp2 = comp - 3
sele2 = selecao [:comp2]

ottotrechos_jusante = QgsVectorLayer(f'''VirtualLayer?query=
                                            SELECT
                                                camada_ottotrechos.cobacia,
                                                camada_ottotrechos.curso_dagua,
                                                camada_ottotrechos.nome_rio,
                                                camada_ottotrechos.geometry
                                            FROM camada_ottotrechos
                                            WHERE ({sele2}) AND camada_ottotrechos.cobacia < '{cod_otto_bacia}';''',
                                        'camada_ottotrechos_jusante',
                                        'virtual')

# desta linha até a 151 são os comandos para consertar o rabicho do Paraiba
sele2 =f"({sele2}) AND camada_ottotrechos.cobacia >= '{cod_otto_bacia}'"
# precisa verificar se o ponto selecionado esta na bacia do 7588 ou na região abaixo ou acima dele. Cada caso é uma regra
paraiba= '7588'
foz = '75891'
#verificar em que região está o ponto selecinado e completar o sele2 extendido na linha 142
if cod_otto_bacia < paraiba:
    sele2 += f" AND camada_ottotrechos.cobacia < '{foz}' OR camada_ottotrechos.curso_dagua LIKE '{paraiba}'"
elif cod_otto_bacia >= foz:
    sele2 += f" OR camada_ottotrechos.curso_dagua LIKE '{paraiba}'"
else:
    sele2 += f" AND camada_ottotrechos.cobacia < '{foz}'"
# aqui acaba a mudança o sele2 esta completo, não precisa mais nada na lina 164 ( o AND foi posto na linha 142)

print(f'sele2:{sele2}')

ottotrechos_jusante_2 = QgsVectorLayer(f'''VirtualLayer?query=
                                            SELECT
                                                camada_ottotrechos.cobacia,
                                                camada_ottotrechos.curso_dagua,
                                                camada_ottotrechos.nome_rio,
                                                camada_ottotrechos.geometry
                                            FROM camada_ottotrechos
                                            WHERE {sele2};''',
                                        'camada_ottotrechos_jusante_2',
                                        'virtual')

if QgsProject.instance().mapLayersByName('camada_bacia_montante'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_bacia_montante')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
simbologia_bacia_montante = {'cor_preenchimento': QColor(0, 0, 0, 0),
                            'cor_contorno': QColor(255, 0, 0, 255),
                            'espessura_contorno': 1}
carregar_camada(bacia_montante, simbologia_bacia_montante)
print(f'--> Carregamento de "{bacia_montante.name()}" realizado.')

if QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
simbologia_ottotrechos_jusante = {'cor': QColor(0, 85, 230, 255),
                                  'espessura': 1.5}
carregar_camada(ottotrechos_jusante, simbologia_ottotrechos_jusante)
print(f'--> Carregamento de "{ottotrechos_jusante.name()}" realizado.')

if QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante_2'):
    remover_camada = QgsProject.instance().mapLayersByName('camada_ottotrechos_jusante_2')[0]
    QgsProject.instance().removeMapLayer(remover_camada)
simbologia_ottotrechos_jusante_2 = {'cor': QColor(20, 0, 220, 255),
                                  'espessura': 0.5}
carregar_camada(ottotrechos_jusante_2, simbologia_ottotrechos_jusante_2)
print(f'--> Carregamento de "{ottotrechos_jusante_2.name()}" realizado.')
