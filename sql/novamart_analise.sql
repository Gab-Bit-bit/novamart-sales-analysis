-- FATURAMENTO x LUCRO x MARGEM DE LUCRO DURANTE OS ANOS
select extract(YEAR from order_date) as ano,
	   sum(gross_sales) as faturamento,
	   sum(profit) as lucro,
	   sum(profit) / sum(net_revenue) as margem_lucro

from fato_vendas
group by ano
order by ano desc

-- Entre 2023 e 2025, o faturamento cresceu aproximadamente 57,5%. Apesar desse crescimento, 
-- o lucro caiu 18,2% e a margem de lucro passou de 24,28% para 13,73%, uma redução de 10,55 pontos percentuais (43,5% em termos relativos)


-- CUSTO DO PRODUTO x RECEITA LÍQUIDA DURANTE OS ANOS
select extract(YEAR from order_date) as ano,
	   sum(net_revenue) as receita_liquida,
	   sum(product_cost) as custo_produto,
	   sum(product_cost) / sum(net_revenue) as receitaXgasto

from fato_vendas
group by ano
order by ano desc

-- Entre 2023 e 2025, a participação do custo dos produtos sobre a receita líquida aumentou 9,9 pontos percentuais, 
-- passando de 71,57% para 81,47%. Isso representa um crescimento relativo de aproximadamente 13,8%.


-- VERIFICANDO CATEGORIAS DE POSSÍVEIS PRODUTOS CAUSADORES DE AUMENTO DE CUSTO
select extract(YEAR from order_date) as ano,
	   category as categoria,
	   sum(net_revenue) as receita_liquida,
	   sum(product_cost) as custo_produto,
	   sum(product_cost) / sum(net_revenue) as receitaXgasto
	   
from fato_vendas as vendas
left join dim_produtos as produtos
	on vendas.product_id = produtos.product_id
group by ano, categoria
order by ano

-- Eletrodomésticos piorou mais em pontos percentuais (+10,5 p.p. contra +9,8 p.p.), mas Eletrônicos gera muito mais receita, 
-- então o impacto estimado em reais fica maior.


-- VERIFICANDO FRETE DURANTES OS ANOS
select extract(YEAR from order_date) as ano,
	   sum(shipping_cost) as frete_novamart,
	   sum(shipping_charged_customer) as frete_cliente,
	   sum(shipping_cost - shipping_charged_customer) as absorvido,
	   (sum(shipping_cost) - sum(shipping_charged_customer)) / sum(net_revenue) * 100 as impacto_receita
	   
from fato_vendas
group by ano
order by ano desc

-- O FRETE ABSORVIDO CRESCEU DE 0,21% PARA 0,39% DA RECEITA ENTRE 2023 E 2025, AUMNETO PROPORCIONAL COM O CUSTO


-- VERIFICANDO AS COMISSÕES POR CANAIS DE VENDAS DURANTE OS ANOS
select extract(YEAR from order_date) as ano,
	   sum(channel_commission) as comissoes_canal,
	   (sum(channel_commission) / sum(net_revenue) * 100) as impacto_receita

from fato_vendas
group by ano
order by ano desc

-- AS COMISSÕES SE MANTIVERAM ESTÁVEIS DE 2,56% PARA 2,62% DA RECEITA ENTRE 2023 E 2025


-- VERIFICANDO AS TAXAS DE RETORNO DURANTE OS ANOS
select extract(YEAR from order_date) as ano,
	   sum(return_cost) as taxa_retorno,
	   (sum(return_cost) / sum(net_revenue) * 100) as impacto_receita

from fato_vendas
group by ano
order by ano desc

-- O custo de devoluções aumentou de 1,39% para 1,78% da receita entre 2023 e 2025, indicando maior impacto proporcional sobre a rentabilidade.


select extract(YEAR from order_date) as ano,
	   (sum(profit) / sum(net_revenue) * 100) as margem_lucro,
	   (sum(product_cost) / sum(net_revenue) * 100) as "% custo_produto",
	   (sum(shipping_cost) - sum(shipping_charged_customer)) / sum(net_revenue) * 100 as "% frete",
	   (sum(channel_commission) / sum(net_revenue) * 100) as "% comissoes",
	   (sum(return_cost) / sum(net_revenue) * 100) as "% devolucao"

from fato_vendas
group by ano
order by ano desc


-- VERIFICANDO SUBCATEGORIAS DURANTE OS ANOS
select extract(YEAR from order_date) as ano,
	   subcategory as subcategoria,
	   (sum(product_cost) / sum(net_revenue) * 100) as custo_produto,
	   sum(net_revenue) as receita_total

from fato_vendas as vendas
left join dim_produtos as produtos
	on vendas.product_id = produtos.product_id
group by ano, subcategoria
order by ano desc


-- QUANTO DO CUSTO ADICIONAL DE 2025 PODE SER ASSOCIADO A PIORA DE RELAÇÃO CUSTO/RECEITA
with custo_subcategoria as (

    select 
        extract(year from order_date) as ano,
        subcategory as subcategoria,
        sum(product_cost) / sum(net_revenue) * 100 as custo_produto,
		sum(net_revenue) as receita_total

    from fato_vendas as vendas
    left join dim_produtos as produtos
        on vendas.product_id = produtos.product_id
    where extract(year from order_date) in (2023, 2025)
    group by ano, subcategoria
),

comparacao as (

    select
        subcategoria,
        max(
            case 
                when ano = 2023 then custo_produto
            end
        ) as custo_2023,
		
        max(
            case 
                when ano = 2025 then custo_produto
            end
        ) as custo_2025,

		max(
			case
				when ano = 2025 then receita_total
			end
		) as receita_2025
		
    from custo_subcategoria
    group by subcategoria
)

select
    subcategoria,
    custo_2023,
    custo_2025,
    custo_2025 - custo_2023 as variacao_pp,
	receita_2025,
	receita_2025 * ((custo_2025 - custo_2023) / 100) as impacto_estimado

from comparacao
order by impacto_estimado desc;

-- todas as subcategorias apresentaram aumento no custo/receita entre 2023 e 2025,
-- com maior impacto financeiro estimado em notebooks, linha branca e smartphones.


-- VERIFICANDO DESCONTOS DURANTE OS ANOS
select extract(year from order_date) as ano,
	   case
	   	   when discount_pct = 0 then 'sem desconto'
	   	   when discount_pct > 0 and discount_pct <= 0.05 then 'até 5%'
	   	   when discount_pct <= 0.10 then '5% a 10%'
	   	   when discount_pct <= 0.20 then '10% a 20%'
		   else 'acima de 20%'
		   end as descontos,
	   count(order_id) as qtde_pedidos,
	   sum(net_revenue) as receita,
	   sum(profit) as lucro,
	   (sum(profit) / sum(net_revenue) * 100) as margem
from fato_vendas
group by ano, descontos
order by ano desc

-- descontos mais elevados estão associados a margens menores.
-- em 2025, 7.311 pedidos tiveram descontos acima de 20%,
-- faixa que apresentou margem negativa de -1,53%.


-- VERIFICANDO DESCONTOS DE 2025
select extract(year from order_date) as ano,
	   case
	   	   when discount_pct = 0 then 'sem desconto'
	   	   when discount_pct > 0 and discount_pct <= 0.05 then 'até 5%'
	   	   when discount_pct <= 0.10 then '5% a 10%'
	   	   when discount_pct <= 0.20 then '10% a 20%'
		   else 'acima de 20%'
		   end as descontos,
	   count(order_id) as qtde_pedidos,
	   sum(net_revenue) as receita,
	   sum(profit) as lucro,
	   (sum(profit) / sum(net_revenue) * 100) as margem
from fato_vendas
where extract(year from order_date) = 2025
group by ano, descontos
order by ano desc

-- em 2025, vendas com descontos acima de 20% geraram R$ 11,26 milhões em receita,
-- mas apresentaram prejuízo de R$ 171,9 mil e margem de -1,53%.


-- VERIFICANDO SUBCATEGORIAS COM DESCONTOS MAIS AGRESSIVOS
select subcategory as subcategorias,
	    case
	   	   when discount_pct = 0 then 'sem desconto'
	   	   when discount_pct > 0 and discount_pct <= 0.05 then 'até 5%'
	   	   when discount_pct <= 0.10 then '5% a 10%'
	   	   when discount_pct <= 0.20 then '10% a 20%'
		   else 'acima de 20%'
		   end as descontos,
	    count(order_id) as qtde_pedidos,
	    sum(net_revenue) as receita,
	    sum(profit) as lucro,
	    (sum(profit) / sum(net_revenue) * 100) as margem
		   
from fato_vendas as vendas
left join dim_produtos as produtos
	on vendas.product_id = produtos.product_id
where extract(year from order_date) = 2025 and discount_pct > 0.20
group by subcategorias, descontos
order by descontos

-- em 2025, notebooks concentrou o maior prejuízo entre as vendas com descontos acima de 20%,
-- com r$ 495 mil de prejuízo e margem de -12,44%, seguido por smartphones e linha branca.


-- Como receita, lucro, margem, custo do produto e desconto médio evoluíram mês a mês
select data.ano as ano,
	   data.mes as num_mes,
	   data.nome_mes as meses,
       sum(net_revenue) as receita,
	   sum(profit) as lucro,
	   (sum(profit) / sum(net_revenue) * 100) as margem,
	   (sum(product_cost) / sum(net_revenue) * 100) as custo_produto,
	   avg(discount_pct) as desconto_medio

from fato_vendas as vendas
left join dim_data as data
	on vendas.order_date = data.order_date
group by ano, num_mes, meses
order by data.ano, data.mes

-- a análise mensal reforça a deterioração da rentabilidade:
-- meses de maior receita apresentam aumento de custos e descontos,
-- com destaque para nov/2025, maior receita mensal e menor margem da série.
	
select
    order_date,
    count(*) as quantidade
from dim_data
group by order_date
having count(*) > 1
order by quantidade desc;