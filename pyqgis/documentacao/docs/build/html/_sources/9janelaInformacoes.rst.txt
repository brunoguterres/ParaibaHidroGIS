9. Janela de informações
========================

O fluxograma de processos desta etapa é apresentado a seguir:

(ADICIONAR FLUXOGRAMA)

Primeiramente é importado o módulo **psycopg2**.

É feita a conexão com o banco de dados PostgreSQL usando o **psycopg2**. 

Então é executada uma consulta inicial para obter o código da bacia (cod_otto_bacia) usando consulta. O valor é selecionado a partir da coluna *cobacia* da tabela *ottobacia_selecionada*.

A função **apresenta_informacoes** cria uma janela de mensagem (QMessageBox) para exibir as informações sobre a área selecionada. As informações são passadas através do dicionário **informacoes_selecao**.

A função **obter_informacoes** inicializa um dicionário **informacoes_selecao** com os valores de cobacia, nome_rio, area_mont, n_trechos_mont, isr_otto, q_cap_mont, disp_acum. Para obter esses valores, são realizadas consultas SQL.