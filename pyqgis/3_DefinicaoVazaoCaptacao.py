from qgis.core import QgsExpressionContext, QgsExpressionContextUtils
from qgis import processing

def importar_disponibilidade_hidrica(parametros_conexao, nome_camada_disp):
#   função de carregamento de camadas vetorial de disponibilidade hídrica do banco
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_camada_disp, 'geom')
    disponibilidade_hidrica = QgsVectorLayer(uri.uri(False), 'camada_disp_hid', 'postgres')
    QgsProject.instance().addMapLayer(disponibilidade_hidrica)
    print('\n''-> Importação da camada de disponibilidade hídrica realizada.')
    return disponibilidade_hidrica

def importar_captacoes(parametros_conexao, nome_camada_outorgas):
#   função de carregamento de camadas vetorial de outorgas de captação do banco
    uri = QgsDataSourceUri()
    uri.setConnection(parametros_conexao['host_bd'],
                      parametros_conexao['porta_bd'],
                      parametros_conexao['nome_bd'],
                      parametros_conexao['usuario_bd'],
                      parametros_conexao['senha_bd'])
    uri.setDataSource(parametros_conexao['schema_bd'], nome_camada_outorgas, 'geom')
    outorgas = QgsVectorLayer(uri.uri(False), 'camada_outorgas', 'postgres')
    QgsProject.instance().addMapLayer(outorgas, False) 
    print('\n''-> Importação da camada de captações realizada.')
    return outorgas

def agregacao_vazao_captacao(outorgas, ottobacias):
    # método que realiza operações para obter o valor da vazão nas ottobacias a montante da bacia de interesse
    processo_bacias_outorgas = processing.run("native:intersection",{
                                                    'INPUT': outorgas,
                                                    'OVERLAY':ottobacias,
                                                    'OUTPUT':'memory: outorgas_e_ottobacias'})
    intersecao_bacias_outorgas = processo_bacias_outorgas['OUTPUT']
        
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(intersecao_bacias_outorgas))
        
    processo_de_agrupamento_por_ottobacias = processing.run("native:aggregate", {
                'INPUT': intersecao_bacias_outorgas,
		        'GROUP_BY':'"cobacia"',
		        'AGGREGATES':[{'aggregate': 'first_value',
                               'delimiter': ',',
                               'input': '"cobacia"',
                               'length': 0,
                               'name': 'cobacia',
                               'precision': 0,
                               'sub_type': 0,
                               'type': 10,
                               'type_name': 'text'},
                              {'aggregate': 'sum',
                               'delimiter': ',',
                               'input': '"vazão horária (m³/h)"',
                               'length': 0,
                               'name': 'vazão horária (m³/h)',
                               'precision': 0,
                               'sub_type': 0,
                               'type': 6,
                               'type_name': 'double precision'}],
		        'OUTPUT':'memory: outorgas_agregadas'})
    agrupamento_por_ottobacias = processo_de_agrupamento_por_ottobacias['OUTPUT']
    QgsProject.instance().addMapLayer(agrupamento_por_ottobacias, True)
    return intersecao_bacias_outorgas, agrupamento_por_ottobacias

### EXECUÇÃO ###

# IMPORTAÇÃO DE CAMADAS DE OUTORGAS #
outorgas = importar_captacoes(parametros_conexao, nome_camada_outorgas)

# INTERSEÇÃO DE OTTOBACIAS E OUTORGAS DE CAPTAÇÃO, AGREGAÇÃO DAS VAZÕES DE CAPTAÇÃO #
intersecao_bacias_outorgas, agrupamento_por_ottobacias = agregacao_vazao_captacao(outorgas, ottobacias)
print('\n''-> Insterseção de ottobacias e outorgas de captação e agregação das vazões realizada.')