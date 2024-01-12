# Documentação - COB_HIDRO_001

## Resumo da ferramenta

Esta ferramenta esta sendo desenvolvida com o propósito de servir para o auxílio nos trabalhos de projetos de Recursos Hídricos, sendo um facilitador nos procedimentos de cálculo do balanço hídrico.

O desenvolvimento é realizado no contexto do projeto do **Plano de Recursos Hídricos da Bacia do Rio Paraíba(PRH-BPB)**.

Baseado na liguagem de programação python incorporada ao software QGIS.

## Objetivos da documentação

Esta documentação tem por objetivo primordial orientar a equipe de desenvolvimento de modo a detalhar todas as etapas e processos de execução da ferramenta. Deve ser utilizada também como material de consulta para utilização por profissionais envovidos nas etapas de testes e validação de suas funcionalidades.

## Estrutura

A estrutura funcional da ferramenta foi criada de forma hierarquica de modo a propiciar melhor entendimento sobre todo os detalhes das etapas envolvidas no processo de execução da ferramenta. Para isto forma definidos os conceitos de **Etapas**, **Processos** e **Funções**.

- **ETAPAS:** O primeiro nível de organização estrutural. Neste nível abstrai-se qualquer tipo de detalhamento, sendo apenas descritos de forma geral o processo do iinício ao fim.

- **PROCESSOS:** O segundo nível de organização estrutural. Neste nível apresenta-se um detalhamento maior das etapas, a fim de que se possa diminuir o nível de abastração e identificar melhor as funcionalidades.

- **FUNÇÕES:** O terceiro nível de organização estrutural. Neste nível são detalhadas todas as funções executadas em cada processo, de modo individual. É o nível com menor grau de abstração, sendo possível identificar todas as estruturas funcionais da ferramenta.

## Fluxograma de etapas

```mermaid
    flowchart TD
    A(INÍCIO) --> B[Procedimentos iniciais];
    B --> C[Inicialização do mapa];
    C --> D[Definir vazão de capatação por ottobacias];
    D --> E[Preparação de dados para balanço hídrico];
    E --> F[Cálculo do balanço hídrico];
    F --> G(FIM);    
```

## Descrição detalhada das etapas

Esta seção destina-se a descrição detalhada de todas as etapas apresentadas no fluxograma anterior, mostrando seus processos e explicando as respectivas funções.

### 1.Procedimentos iniciais

#### Fluxograma de processos

```mermaid
    flowchart TD    
    subgraph A[Procedimentos Iniciais]
        B[Definição dos parâmetros de conexão com o Banco de Dados] --> C[Limpeza de Camadas Residuais];
    end
```
***
```mermaid
    flowchart TD
    subgraph A[Inicialização do Mapa]
        B[Importação de camadas da bacia] --> C[Carregamento de camada de ottotrechos no mapa];
        C --> D[Carregamento de camada de fundo no mapa]
    end
```
---
```mermaid
    flowchart TD
    subgraph A[Definir vazão de captação por ottobacias]
        B[Carregamento de camada de outorgas]
        B --> D[Interseção de outorgas com ottobacias]
        D --> E[Agregação de vazões por ottobacias]
    end
```
---
```mermaid
    flowchart TD
    subgraph A[Preparação de dados para o balanço hídrico]
        B[União de atributos de disponibilidade e captações]
    end
```
---
```mermaid
    flowchart TD
    subgraph A[Cálculo do balanço hídrico]
        B[Ordenar tabela consolidada] --> C[Definir ottobacias de cabeceira]
        C --> D[Calcular balanço hídrico]
    end
```