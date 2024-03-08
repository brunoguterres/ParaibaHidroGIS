import psycopg2

# Conectar ao banco de dados
conn = psycopg2.connect(
    dbname="bdg_prh_rpb",
    user="postgres",
    password="cobrape",
    host="localhost"
)

# Abrir um cursor para executar operações no banco de dados
cur = conn.cursor()

# Definir os nomes das colunas e seus tipos
columns_info = [
    '"nome VARCHAR(100)"',
    '"idade INTEGER"'
]

# Definir os dados da matriz (lista de listas)
data = [
    ['João', 30],
    ['Maria', 28],
    ['Pedro', 22]
]

# Criar uma view a partir da matriz
cur.execute(f"""
    CREATE OR REPLACE VIEW view_exemplo AS
    SELECT {', '.join(columns_info)}
    FROM (
        VALUES {', '.join([f"('{row[0]}', {row[1]})" for row in data])}
    ) AS data({', '.join(columns_info)})
""")

# Commitar as operações
conn.commit()

# Fechar o cursor e a conexão com o banco de dados
cur.close()
conn.close()
