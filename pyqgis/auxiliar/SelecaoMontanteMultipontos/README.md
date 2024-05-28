# DESCRIÇÃO

Os arquivos deste diretório foram criados no contexto de uma demanda específica do William Cantos Corrêa, para análise de porcentagem de área de diferentes tipos de usos do solo para a região à montante de cada ponto de monitoramento de qualidade de água. Foram também selecionados pontos de ETAS e Outorgas à montante de cada ponto de monitoramento. Para cada tipo de seleção foi criado um arquivo python individual.

:warning: Para a execução destes códigos, faz-se necessário ter as camadas de entrada adicionadas no painel de camadas do QGIS.

## Característica dos dados utilizados

Os dados de uso do solo utilizados provém da coleção 8 do MapBiomas Brasil do ano de 2022. Eles foram vetorizados e reclassificados, de modo que algumas classe foram agrupadas. A reclassificação não interfere no processamentos de nenhum código python abaixo.

## Breve descritivo dos códigos

> **selecao_montante_uso_solo_geometria.py**: Este código faz a seleção das feições de uso do solo que estão contidas nas ottobacias à montante de cada ponto de monitoramento.
>> *RESULTADO:* Este código exporta as geometrias selecionadas no formato shapefile (.shp, .dbf, .shx).

> **selecao_montante_uso_solo_area.py**: Este código calcula a área das feições de uso do solo que estão contidas nas ottobacias à montante de cada ponto de monitoramento. O resultado é agrupado na soma do valor de área por tipo de uso.
>> *RESULTADO:* Este código exporta uma tabela no formato excel (.xlsx).

> **selecao_montante_etas.py**: Este código faz a seleção das ETAS, representadas por pontos, que estão contidas nas ottobacias à montante de cada ponto de monitoramento.
>> *RESULTADO:* Este código exporta uma tabela no formato excel (.xlsx) com o número total de ETAS contidas à montante de cada ponto de monitoramento.

> **selecao_montante_outorgas_usuarios.py**: Este código faz a seleção de pontos de outorgas que estão contidas nas ottobacias à montante de cada ponto de monitoramento.
>> *RESULTADO:* Este código exporta uma tabela no formato excel (.xlsx) com o número total de outorgas contidas à montante de cada ponto de monitoramento.