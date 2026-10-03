# %%

# IMPORTANDO PANDAS
import pandas as pd

# IMPORTANDO EXTRAÇÃO
from extracao import extract_data

# %%

# CARREGANDO DATASET
df = extract_data()

# %%

# CONVERSÃO DE STR PARA DATETIME, COLUNA "ORDER_DATE"
df['order_date'] = pd.to_datetime(
    df['order_date'],
    format= '%Y-%m-%d'
)

# %%

# VERIFICANDO ESTATÍSTICAS
df.describe()

# %%

# VERIFICANDO CARDINALIDADE
df.nunique()

# %%

# VERIFICANDO REGISTROS NULOS
df.isna().sum()

# %%

# VISUALIZANDO REGISTROS NULOS
df[df.isna().any(axis= 1)]

# %%

# QUANTIDADE DE NULOS SIMULTÂNEAMENTE
(
    df['customer_segment'].isna() &
    df['customer_rating'].isna()
).sum()

# %%

# QUANTIDADE DE SEGUIMENTOS (INCLUINDO NULO)
df['customer_segment'].value_counts(dropna= False)

# %%

# PREENCHENDO REGISTROS NULOS
df['customer_segment'] = df['customer_segment'].fillna('Não Informado')
df['customer_segment'].value_counts(dropna= False)

# %%

# QUANTIDADE DE AVALIÇÕES NULAS
df['customer_rating'].value_counts(dropna= False)

#--- DECISÃO: MANTER REGISTROS NULOS DE AVALIAÇÃO DE CLIENTES ---#

# %%

# VERIFICANDO DUPLICADAS
df.duplicated().sum()

# %%

# VALIDANDO REGISTROS DUPLICADOS
df[df.duplicated(subset= 'order_id', keep= False)].sort_values('order_id').head(10)

# %%

# EXCLUINDO LINHAS DUPLICADAS
df.drop_duplicates(inplace= True)
print(f'Quantidade de linhas duplicadas: {df.duplicated().sum()}')


# %%

# VERIFICANDO SE EXISTEM QUANTIDADES < 0
(df['quantity'] <= 0).sum()

# %% 

# VERIFICANDO SE EXISTE TAXA DE DEVOLUÇÃO EM PEDIDOS NÃO DEVOLVIDOS
df[
    (df['returned'] == False) &
    (df['return_cost'] > 0)
]

# %%

# VERIFICANDO SE EXISTE PROMOÇÃO EM PRODUTOS SEM DESCONTO
df[
    (df['promotion'] == False) &
    (df['discount_pct'] > 0)
]

# %%

# VERIFICANDO SE EXISTE RECEITA LÍQUIDA MAIOR DO QUE VALOR BRUTO
(
    df['net_revenue'] > df['gross_sales']
).sum()

# %%

# VERIFICANDO VALOR BRUTO DE VENDAS
valor_bruto_venda = df['gross_sales'].sum()
print(valor_bruto_venda)

#
# %%

# VALIDANDO VALOR BRUTO DE VENDAS
df['gross_sales_calculado'] = df['unit_price'] * df['quantity']
print(f'Valor bruto calculado: {df['gross_sales_calculado'].sum()}' 
      f'\nValor bruto: {df['gross_sales'].sum()}')

# %%

# VALOR BRUTO CALCULADO X VALOR BRUTO 
df['diferenca_gross_sales'] = (
    df['gross_sales_calculado'] - df['gross_sales']
)

# %%

# DIFERENÇA ENTRE REGISTROS
df.loc[df['diferenca_gross_sales'].abs() > 0.01,
       [
           'order_id',
           'unit_price',
           'quantity',
           'gross_sales',
           'gross_sales_calculado',
           'diferenca_gross_sales'
           
       ]
]

# %%

# VERIFICANDO LUCRO
df['profit'].sum()

# %%

# VERIFICANDO COMISSÃO DE CANAL
df['channel_commission'].sum()

# %%

# VERIFICANDO CUSTO DE ENVIO
df['shipping_cost'].sum()

# %%

# VERIFICANDO FRETE COBRADO DO CLIENTE
df['shipping_charged_customer'].sum()

# %%

# VERIFICANDO DIFERENÇA DE CUSTO DE FRETE X FRETE COBRADO
(df['shipping_cost'] - df['shipping_charged_customer']).sum()

# %%

# VERIFICANDO O CUSTO DE DEVOLUÇÃO
df['return_cost'].sum()

# %%

# VALIDANDO LUCRO A PARTIR DAS ANÁLISES 
df['profit_calculado'] = (
    df['net_revenue']
    + df['shipping_charged_customer']
    - df['channel_commission']
    - df['shipping_cost']
    - df['return_cost']
    - df['product_cost']
)

# %%

# DIFERENÇA ENTRE LUCRO ORIGINAL X LUCRO VALIDADO
df['diferenca_profit'] = (df['profit'] - df['profit_calculado']).round(2)

print(f'Diferença mínima, lucro original x lucro calculado: {df['diferenca_profit'].min()}' 
      f'\nDiferença máxima, lucro original x lucro calculado: {df['diferenca_profit'].max()}')
# %%

# VALIDANDO DE MARGEM DE LUCRO
df['profit_margin_calculada'] = ((
    df['profit'] / df['net_revenue']
) * 100).round(2)

# %%

diferenca = (
    df['profit_margin'] - 
    (df['profit'] / df['net_revenue']) 
).abs()

diferenca.max()

# %%

# VERIFICANDO REGISTROS DE DATAS
print(f'Período mínimo: {df['order_date'].min()}')
print(f'Período máximo: {df['order_date'].max()}')

# %%

# VERIFICANDO MESES DOS 3 ANOS

# 2023
(
    df[df['order_date'].dt.year == 2023]
             .groupby(df['order_date']
             .dt.to_period('M'))
             .size()
             .sort_index()
)
# %%

# 2024
(
    df[df['order_date'].dt.year == 2024]
             .groupby(df['order_date']
             .dt.to_period('M'))
             .size()
             .sort_index()
)

# %%

# 2025
(
    df[df['order_date'].dt.year == 2025]
             .groupby(df['order_date']
             .dt.to_period('M'))
             .size()
             .sort_index()
)

# %%

# VERIFICANDO INCONSISTÊNCIAS EM CATEGORIAS
df['category'].unique()

# %%

# VERIFICANDO INCONSISTÊNCIAS EM SUBCATEGORIAS
df['subcategory'].unique()

# %%

# VERIFICANDO INCONSISTÊNCIAS EM REGIÃO
df['region'].unique()

# %%

# VERIFICANDO INCONSISTÊNCIAS EM CANAL DE VENDAS
df['sales_channel'].unique()

# %%

# VERIFICAÇÃO DE OUTLIERS GROSS_SALES
df['gross_sales'].describe()

# %%

# VALIDANDO OUTLIERS POSITIVOS GROSS_SALES
df.nlargest(10, 'gross_sales')[['order_id', 
                                'quantity', 
                                'unit_price', 
                                'gross_sales']]

# %%

# VALIDANDO OUTLIERS NEGATIVOS GROSS_SALES
df.nsmallest(10, 'gross_sales')[['order_id', 
                                'quantity', 
                                'unit_price', 
                                'gross_sales']]

# %%

# VERIFICANDO DE OUTLIERS NET_REVENUE
df['net_revenue'].describe()

# %%

# VALIDANDO OUTLIERS POSITIVOS NET_REVENUE
df.nlargest(10, 'net_revenue')[['order_id', 
                                'quantity', 
                                'unit_price', 
                                'net_revenue']]

# %%

# VALIDANDO OUTLIERS NEGATIVOS NET_REVENUE
df.nsmallest(10, 'net_revenue')[['order_id', 
                                'quantity', 
                                'unit_price', 
                                'net_revenue']]

# %%

# VERIFICAÇÃO DE OUTLIERS PROFIT
df['profit'].describe()

# %%

# VALIDANDO OUTLIERS POSITIVOS PROFIT
df.nlargest(10, 'profit')[['order_id',
                            'net_revenue',
                            'product_cost',
                            'shipping_cost',
                            'shipping_charged_customer',
                            'channel_commission',
                            'return_cost',
                            'returned',
                            'profit']]

# %%

# VALIDANDO OUTLIERS NEGATIVOS PROFIT
df.nsmallest(10, 'profit')[['order_id',
                            'net_revenue',
                            'product_cost',
                            'shipping_cost',
                            'shipping_charged_customer',
                            'channel_commission',
                            'return_cost',
                            'returned',
                            'profit']]

# %%

# FUNÇÃO PARA RETORNAR O DATASET TRATADO
def transform_data(df):

    df['order_date'] = pd.to_datetime(
    df['order_date'],
    format= '%Y-%m-%d'
)

    df['customer_segment'] = df['customer_segment'].fillna('Não Informado')

    df.drop_duplicates(inplace= True)

    df['state'] = df['state'].str.strip()

    return df

# %%