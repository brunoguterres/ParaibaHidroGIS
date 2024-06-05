10. Códigos Auxiliares
======================

Este diretório contém arquivos antigos, que foram descontinuados no processo de desenvolvimento do aplicativo principal, ou arquivos que foram criados para atividades específicas relacionadas ao projeto mas que não fazem parte do desenvolvimento do aplicativo principal.

10.1. Códigos Descontinuados
----------------------------

**a) geral.py**: Este arquivo é uma versão antiga que já foi o código principal do aplicativo em algum momento do desenvolvimento. Ele foi descontinuado, mas possui alguns códigos de processamentos que podem ser úteis.

.. note::
    
    Possui processamentos que executam o cálculo de população dentro de ottobacias utilizando código python (PyQGIS).

**b) 7_SelecaoOttobacia.py**: Este arquivo é uma versão antiga da etapa 7 do aplicativo, com outras ferramentas para seleção da ottobacia, utilizando o QgsMapToolIdentify para identificar feições e obter informações detalhadas da camada, enquanto a nova versão faz a seleção pela coordenada com outra funcionalidade.

**c) 8_RepresentacaoSelecao.py**: Este arquivo é uma versão antiga da etapa 8 do aplicativo. Nessa versão são criadas views no banco de dados, enquanto no código novo são utilizadas camadas virtuais. É uma versão mais robusta para a representação da seleção.


10.2. Comandos Úteis
--------------------

**comando_uteis.py**: Neste arquivo são apresentados alguns comandos que possam ser utilizados em algum momento do desenvolvimento. 

10.3. Códigos Extras
--------------------

10.3.1. Seleção Montante Multipontos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Os arquivos deste diretório (SelecaoMontanteMultipontos) foram criados no contexto de uma demanda específica do William Cantos Corrêa, para análise de porcentagem de área de diferentes tipos de usos do solo para a região à montante de cada ponto de monitoramento de qualidade de água. Foram também selecionados pontos de ETAS e Outorgas à montante de cada ponto de monitoramento. Para cada tipo de seleção foi criado um arquivo python individual.

.. note::
    
    Para a execução destes códigos, faz-se necessário ter as camadas de entrada adicionadas no painel de camadas do QGIS.

**Característica dos dados utilizados**:

Os dados de uso do solo utilizados provém da coleção 8 do MapBiomas Brasil do ano de 2022. Eles foram vetorizados e reclassificados, de modo que algumas classe foram agrupadas. A reclassificação não interfere no processamentos de nenhum código python abaixo.

**Breve descritivo dos códigos**:

    **a) selecao_montante_uso_solo_geometria.py**: Este código faz a seleção das feições de uso do solo que estão contidas nas ottobacias à montante de cada ponto de monitoramento.

*RESULTADO*: Este código exporta as geometrias selecionadas no formato shapefile (.shp, .dbf, .shx).

    **b) selecao_montante_uso_solo_area.py**: Este código calcula a área das feições de uso do solo que estão contidas nas ottobacias à montante de cada ponto de monitoramento. O resultado é agrupado na soma do valor de área por tipo de uso.

*RESULTADO*: Este código exporta uma tabela no formato excel (.xlsx).

    **c) selecao_montante_etas.py**: Este código faz a seleção das ETAS, representadas por pontos, que estão contidas nas ottobacias à montante de cada ponto de monitoramento.

*RESULTADO*: Este código exporta uma tabela no formato excel (.xlsx) com o número total de ETAS contidas à montante de cada ponto de monitoramento.

    **d) selecao_montante_outorgas_usuarios.py**: Este código faz a seleção de pontos de outorgas que estão contidas nas ottobacias à montante de cada ponto de monitoramento.

*RESULTADO*: Este código exporta uma tabela no formato excel (.xlsx) com o número total de outorgas contidas à montante de cada ponto de monitoramento.