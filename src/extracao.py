# %%

# IMPORTANDO PANDAS
import pandas as pd

# %%

# CARREGANDO DATASET
def extract_data():
    df = pd.read_csv('../data/raw/novamart_vendas.csv')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 150)
    return df

# %%

# EXECUTANDO EXTRAÇÃO
df = extract_data()

# %%

# CONHECENDO DATA SET
df.head(n = 5)

# %%

# VERIFCANDO COLUNAS
df.columns

# %%

# VERIFICANDO DIMENSÃO DO DATASET
print(f'Quantidade de linhas: {df.shape[0]}' 
      f'\nQuanidade de Colunas: {df.shape[1]}')

# %%

# VERIFICANDO DTYPES E MEMORY USAGE
df.info()

# %%
df[['channel_commission', 
    'returned', 
    'return_cost', 
    'delivery_days', 
    'customer_rating', 
    'profit', 
    'profit_margin']].info()