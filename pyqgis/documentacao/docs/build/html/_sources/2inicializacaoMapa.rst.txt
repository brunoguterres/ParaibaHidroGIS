2. Inicialização do Mapa
========================

O fluxograma de processos desta etapa é apresentado a seguir:

.. image:: imagens/DiagramaEtapa2.png
    :align: center

O **import requests** faz a importação da biblioteca Requests, a qual é utilizada para fazer requisições HTTP em python de forma simples e eficiente.

2.1. Limpeza das camadas residuais
----------------------------------

A função **limpeza_residuos** realiza a limpeza de camadas residuais do projeto no QGIS. 

A variável **camada_residual** utiliza o **QgsProject.instance** para obter um dicionário de todas as camadas do projeto usando o método mapLayers() da instância do projeto e, em seguida, obtém os valores desse dicionário, resultando em uma lista de todas as camadas no projeto.

.. note::
    
    O **QgsProject** é uma classe central no QGIS que representa o projeto em si. Ele armazena informações sobre camadas, configurações do projeto, sistemas de coordenadas e outros elementos relacionados ao ambiente de trabalho no QGIS. 

Após a criação da lista com as camadas do projeto, é feita a verificação da existência de camadas residuais, caso haja qualquer camada residual é feita a remoção da mesma. Caso contrário, será apenas obtido e atualizado o canvas do mapa do projeto utilizando o **qgis.utils.iface.mapCanvas()** e o **canvas.refresh()**.

.. note::
    
    O **iface** é uma instância da classe QgisInterface que fornece acesso às interfaces do QGIS para plugins. O *mapCanvas* é o método utilizado para obter a referência à tela de visualização do mapa atual no QGIS.

2.2. Importação de camadas da bacia
-----------------------------------

Nesse processo será feita a importação das camadas do banco de dados.

A função **importar_camada_bdg** recebe informações sobre o banco de dados (nome, schema, nome da camada) para importar a camada vetorial correspondente.

A variável *uri* utiliza o **QgsDataSourceUri** para armazenar informações sobre a fonte de dados da camada vetorial, e, posteriormente, configura as informações de conexão com o banco de dados na URI. 

.. note::
    
    O **QgsDataSourceUri** é uma classe na biblioteca QGIS que é usada para representar e manipular informações de conexão com fontes de dados, como bancos de dados espaciais, arquivos shapefile, serviços da web, entre outros. Essa classe permite que você construa e manipule de forma pragmática URIs (Uniform Resource Identifiers) que especificam a fonte de dados que será utilizada em um projeto QGIS.

A variável *camada_importada* cria um objeto **QgsVectorLayer** usando a URI configurada e define o nome da camada. 

.. note::
    
    O **QgsVectorLayer** é uma classe na biblioteca QGIS que representa uma camada vetorial dentro do ambiente QGIS. Essa classe é parte da API do QGIS e é usada para manipular dados vetoriais, como pontos, linhas e polígonos. 

2.3. Carregamento de camadas da bacia no mapa
---------------------------------------------

A função **carregar_camada** é responsável por configurar a simbologia de uma camada. Para isso, a variável **tipo_geometria** obtém o tipo de geometria da camada fornecida como parâmetro e depois é verificado se é um ponto. A classe **QgsWkbTypes** é usada para verificação do tipo de geometria, enquanto as classes **QgsSimpleMarkerSymbolLayer**, **QgsLineSymbol** e **QgsFillSymbol** são utilizadas para representar a simbologia das camadas.

* Se for um ponto, é criado um símbolo de marcador simples com base nos parâmetros de cor e tamanho fornecidos na simbologia. Se não for ponto, verifica se é uma linha. Os parâmetros de simbologia que podem ser modificados são a cor e o tamanho.

* Se for uma linha, cria um símbolo de linha simples com base nos parâmetros de cor e espessura fornecidos na simbologia. Se não for uma linha, verifica se é uma geometria de polígono. Os parâmetros de simbologia que podem ser modificados são a cor e a espessura.

* Se for um polígono, cria um símbolo de preenchimento simples com base nos parâmetros de cor de preenchimento, cor de contorno e espessura do contorno fornecidos na simbologia. Os parâmetros de simbologia que podem ser modificados são a cor do preenchimento, a cor da borda e a espessura da borda.

Então é criado um renderizador de símbolo único (**QgsSingleSymbolRenderer**) usando o símbolo definido anteriormente. E por fim, a camada é adicionada ao projeto QGIS.

.. note::
    
    - A classe **QgsWkbTypes** é usada para lidar com tipos Well-Known Binary, que é um formato binário usado para representar objetos geométricos. A classe fornece enumerações e funções para trabalhar com esses tipos WKB.
    - A classe **QgsSimpleMarkerSymbolLayer** é utilizada para representar uma camada de símbolo de marcador simples.
    - A classe **QgsLineSymbol** é utilizada para representar símbolos de linha em camadas vetoriais.
    - A classe **QgsFillSymbol** é utilizada para representar símbolos de preenchimento em camadas vetoriais.

2.3.1. Guia RGBA
~~~~~~~~~~~~~~~~

A simbologia RGBA (Red, Green, Blue, Alpha) é um modelo de cor usado para definir cores em gráficos, imagens e mapas. Cada componente representa a intensidade de uma cor primária (Red, Green, Blue), enquanto o componente Alpha representa a transparência da cor.

A intensidade varia de 0 a 255 para todos, sendo que quanto maior o valor, mais próximo da saturação e luminosidade da cor estará aquele componente. Para a transparência, quanto maior o valor, menor é a transparência. Os valores também podem ser normalizados de 0 a 1. O preto é representado pelo 0 em todos os componentes.

.. table::
    :align: center

    +---------------------------------------------+ 
    |**Exemplo**:                                 |
    +=============================================+
    |azul = (0, 0, 1, 1)                          |
    |                                             |
    |vermelho semi-transparente = (1, 0, 0, 0.5)  |
    +---------------------------------------------+


2.4.  Carregamento de basemap
-----------------------------

A função **importar_camada_fundo** tem como objetivo carregar uma camada de plano de fundo usando a biblioteca QGIS. 

A variável **service_url** contém uma URL para um serviço de mapas do Google. Os placeholders {x}, {y} e {z} são utilizados para representar os valores de latitude, longitude e zoom.

A variável **serivce_uri** contém a URI do serviço de mapas, formatada com os parâmetros necessários. A função **requests.utilis.quote** é usada para garantir que a URL seja codificada corretamente.

A função **iface.addRasterLayer** da interface do QGIS é utilizada para adicionar uma camada raster com os argumentos:

* **service_uri**: a URI do serviço de mapas
* **Google_Road**: nome da camada a ser adicionada
* **wms**: tipo de serviço, indicando que é um Web Map Service