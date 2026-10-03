# %%
# IMPORTANDO PANDAS

import pandas as pd

#%%
# IMPORTANDO O DATASET 
from extracao import extract_data

# %%
# IMPORTANDO DATASET CONSOLIDADO
from tratamento import transform_data

# %%
df = extract_data()

# %%
df = transform_data(df)

#%%
df['state'].unique()

# %%

# CRIANDO TABELA FATO VENDAS
def tabela_fato_vendas(df):
    fato_vendas = df[[
        'order_id',
        'order_date',
        'customer_id',
        'product_id',
        'customer_segment',
        'state',
        'sales_channel',
        'promotion',
        'promotion_type',
        'quantity',
        'unit_price',
        'discount_pct',
        'gross_sales',
        'net_revenue',
        'product_cost',
        'shipping_cost',
        'shipping_charged_customer',
        'channel_commission',
        'returned',
        'return_cost',
        'delivery_days',
        'customer_rating',
        'profit',
        'profit_margin'
    ]].copy()
    return fato_vendas

# %%
fato_vendas = tabela_fato_vendas(df)

# %%

# CRIANDO TABELA DIMENSÃO PRODUTO
def tabela_dim_produtos(df):
    dim_produtos = df[[
        'product_id',
        'category',
        'subcategory'
    ]].drop_duplicates().copy()
    return dim_produtos

# %%
dim_produtos = tabela_dim_produtos(df)

# %%

# CRIANDO TABELA DIMENSÃO LOCALIZAÇÃO
def tabela_dim_localizacao(df):
    dim_localizacao = df[[
        'state',
        'region'
    ]].drop_duplicates().copy()
    return dim_localizacao

# %%
dim_localizacao = tabela_dim_localizacao(df)

# %%

# CRIANDO TABELA DIMENSÃO DATA
def tabela_dim_data(df):

    dim_data = df[['order_date']].drop_duplicates().copy()

    meses = {
        'January': 'Janeiro',
        'February': 'Fevereiro',
        'March': 'Março',
        'April': 'Abril',
        'May': 'Maio',
        'June': 'Junho',
        'July': 'Julho',
        'August': 'Agosto',
        'September': 'Setembro',
        'October': 'Outubro',
        'November': 'Novembro',
        'December': 'Dezembro',

    }
    
    dim_data['ano'] = dim_data['order_date'].dt.year
    dim_data['mes'] = dim_data['order_date'].dt.month
    dim_data['nome_mes'] = dim_data['order_date'].dt.month_name()
    dim_data['trimestre'] = dim_data['order_date'].dt.quarter

    dim_data['nome_mes'] = dim_data['nome_mes'].map(meses)
    return dim_data

# %%
dim_data = tabela_dim_data(df)

# %%

# SALVANDO TABELAS MODELADAS
fato_vendas.to_csv('../data/processed/fato_vendas.csv', index= False)
dim_produtos.to_csv('../data/processed/dim_produtos.csv', index= False)
dim_localizacao.to_csv('../data/processed/dim_localizacao.csv', index= False)
dim_data.to_csv('../data/processed/dim_data.csv', index= False)
# %%
