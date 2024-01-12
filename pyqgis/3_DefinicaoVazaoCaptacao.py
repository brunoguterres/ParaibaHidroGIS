def agregacao_vazao_captacao(outorgas, ottobacias_montante):
    # método que realiza operações para obter o valor da vazão nas ottobacias a montante da bacia de interesse
    processo_bacias_outorgas = processing.run("native:intersection",{
                                                    'INPUT': outorgas,
                                                    'OVERLAY':ottobacias_montante,
                                                    'OUTPUT':'memory: outorgas_e_ottobacias_montante'})
    intersecao_bacias_outorgas = processo_bacias_outorgas['OUTPUT']
        
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(intersecao_bacias_outorgas))
        
    processo_de_agrupamento_por_ottobacias = processing.run("native:aggregate", {
                'INPUT': intersecao_bacias_outorgas,
		        'GROUP_BY':'"cobacia"',
		        'AGGREGATES':[{'aggregate': 'first_value','delimiter': ',','input': '"cobacia"','length': 0,'name': 'cobacia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
                            {'aggregate': 'sum','delimiter': ',','input': '"vazao"','length': 0,'name': 'vazao','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],
		        'OUTPUT':'memory: ottobacias_montante_vazao'})
    agrupamento_por_ottobacias = processo_de_agrupamento_por_ottobacias['OUTPUT']
    return intersecao_bacias_outorgas, agrupamento_por_ottobacias

### EXECUÇÃO ###

# IMPORTAÇÃO DE CAMADAS DE OUTORGAS #
outorgas = importar_outorgas(nome_bd, senha_bd)

# INTERSEÇÃO DE OTTOBACIAS E OUTORGAS DE CAPTAÇÃO, AGREGAÇÃO DAS VAZÕES DE CAPTAÇÃO #
intersecao_bacias_outorgas, agrupamento_por_ottobacias = agregacao_vazao_captacao(outorgas, ottobacias_montante)
print('\n''-> Insterseção de ottobacias e outorgas de captação e agregação das vazões realizada.')
