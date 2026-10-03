import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

# CARREGANDO VARIÁVEIS DO .ENV
load_dotenv('.env')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = (
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}'
    f'@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

engine = create_engine(DATABASE_URL)

with engine.connect() as conexao:
    resultado = conexao.execute(text('SELECT 1'))
    print(resultado.fetchone())


# CARREGANDO DADOS PROCESSADOS

fato_vendas = pd.read_csv('data/processed/fato_vendas.csv', 
                          parse_dates = ['order_date']
                          )

dim_localizacao = pd.read_csv('data/processed/dim_localizacao.csv')

dim_produtos = pd.read_csv('data/processed/dim_produtos.csv')

dim_data = pd.read_csv('data/processed/dim_data.csv',
                       parse_dates = ['order_date']
                       )

def load_tabela(df, nome_tabela):
    df.to_sql(
        name = nome_tabela,
        con = engine,
        if_exists = 'replace',
        index = False
    )

    print(f'Tabel {nome_tabela} carregada com sucesso!')

load_tabela(dim_data, 'dim_data')
load_tabela(dim_localizacao, 'dim_localizacao')
load_tabela(dim_produtos, 'dim_produtos')
load_tabela(fato_vendas, 'fato_vendas')