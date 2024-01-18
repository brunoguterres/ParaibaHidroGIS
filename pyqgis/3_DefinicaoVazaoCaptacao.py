from qgis.core import QgsExpressionContext, QgsExpressionContextUtils
from qgis import processing

def agregacao_vazao_captacao(outorgas, ottobacias):
    # método que realiza operações para obter o valor da vazão nas ottobacias a montante da bacia de interesse
    processo_bacias_outorgas = processing.run("native:intersection",{
                                                    'INPUT': outorgas,
                                                    'OVERLAY':ottobacias,
                                                    'OUTPUT':'memory:outorgas_e_ottobacias'})
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
                               'input': '"vazao_horaria_m3h"',
                               'length': 0,
                               'name': 'vazao_horaria_m3h',
                               'precision': 0,
                               'sub_type': 0,
                               'type': 6,
                               'type_name': 'double precision'}],
		        'OUTPUT':'memory:outorgas_agregadas'})
    agrupamento_por_ottobacias = processo_de_agrupamento_por_ottobacias['OUTPUT']
    QgsProject.instance().addMapLayer(agrupamento_por_ottobacias, True)
    return intersecao_bacias_outorgas, agrupamento_por_ottobacias

### EXECUÇÃO ###

# IMPORTAÇÃO DE CAMADAS DE OUTORGAS #
outorgas = importar_captacoes(parametros_conexao, nome_camada_outorgas)

# INTERSEÇÃO DE OTTOBACIAS E OUTORGAS DE CAPTAÇÃO, AGREGAÇÃO DAS VAZÕES DE CAPTAÇÃO #
intersecao_bacias_outorgas, agrupamento_por_ottobacias = agregacao_vazao_captacao(outorgas, ottobacias)
print('\n''-> Insterseção de ottobacias e outorgas de captação e agregação das vazões realizada.')