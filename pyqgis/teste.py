import psycopg2

# Conectar ao banco de dados
conn = psycopg2.connect(
    dbname="bdg_prh_rpb",
    user="postgres",
    password="guterres",
    host="localhost"
)

# Abrir um cursor para executar operações no banco de dados
cur = conn.cursor()

# Definir os nomes das colunas e seus tipos
campos = [
    'nome',
    'idade',
    'altura'
]

# Definir os dados da matriz (lista de listas)
dados = [
    ['João', 30, 1.75],
    ['Maria', 28, 1.80],
    ['Pedro', 22, 1.85]
]

# Criar uma view a partir da matriz
cur.execute(f"""
    DROP VIEW IF EXISTS view_exemplo
    CREATE VIEW view_exemplo AS
    SELECT {', '.join(campos)}
    FROM (
        VALUES {', '.join([f"('{row[0]}', {row[1]}, {row[2]})" for row in dados])}
    ) AS data({', '.join(campos)})
""")

# Commitar as operações
conn.commit()

# Fechar o cursor e a conexão com o banco de dados
cur.close()
conn.close()
