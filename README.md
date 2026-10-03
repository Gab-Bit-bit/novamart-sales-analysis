# NovaMart — Análise de Vendas e Rentabilidade

**Por que a receita está crescendo enquanto a margem de lucro está caindo?**

O NovaMart é um projeto de análise de dados que investiga essa pergunta em um cenário de varejo, integrando **Python, PostgreSQL e Power BI**. Foi desenvolvido para aplicar conhecimentos técnicos e aprimorar a visão analítica e de negócio.

> A base é sintética e representa uma empresa fictícia. Após o tratamento, foram analisadas 65.000 vendas entre 2023 e 2025.

## Objetivo

Investigar a evolução da receita, dos custos e da margem, identificar o comportamento das vendas promocionais e apresentar informações úteis para decisões comerciais.

## Como o projeto foi desenvolvido

1. **ETL em Python:** leitura do CSV com Pandas, remoção de duplicados, tratamento de valores ausentes, conversão de tipos e validação das regras financeiras.
2. **Modelagem dimensional:** organização dos dados em `fato_vendas`, `dim_produtos`, `dim_localizacao` e `dim_data`, formando um modelo em estrela.
3. **PostgreSQL e SQL:** carga das tabelas, conferência dos registros e análises de receita, lucro, margem, custos e descontos ao longo do tempo.
4. **Power BI e DAX:** criação dos indicadores e de três páginas interativas, com filtros, navegação e dicas de ferramenta.

A validação considerou receita, custo dos produtos, frete absorvido, comissões e devoluções na reconciliação do lucro. A margem foi calculada como **lucro total ÷ receita líquida total**, evitando a média simples das margens individuais.

## Principais resultados

| Indicador | 2023 | 2025 | Variação |
| --- | ---: | ---: | ---: |
| Receita líquida | R$ 27,82 milhões | R$ 40,20 milhões | +44,5% |
| Lucro | R$ 6,75 milhões | R$ 5,52 milhões | −18,3% |
| Margem de lucro | 24,28% | 13,73% | −10,54 p.p. |
| Desconto efetivo | 3,91% | 11,82% | +7,91 p.p. |
| Participação da receita em promoção | 28,47% | 48,66% | +20,19 p.p. |

O custo dos produtos passou de **71,57% para 81,47% da receita líquida**, sendo o maior componente da queda da margem na decomposição apresentada. Essa razão também pode aumentar com descontos maiores, sem necessariamente indicar aumento do preço de compra.

A margem das vendas em promoção caiu de **16,59% para 2,96%**. Em 2025, **Eletrônicos em promoção apresentou margem de −2,04%**, indicando prejuízo nesse recorte. A margem sem promoção também caiu, de 27,34% para 23,95%.

## Dashboards e storytelling

As três páginas conduzem a investigação:

- **Visão Executiva — O que aconteceu?** Evolução da receita, do lucro e da margem, com contexto de pedidos, ticket, categorias e regiões.
- **Rentabilidade — O que explica a queda?** Cascata da variação da margem e comparação do peso dos custos por categoria e ano.
- **Descontos — Como as promoções se comportam?** Evolução dos descontos, participação promocional e comparação das margens com e sem promoção.

<details>
<summary>Visualizar os dashboards</summary>

### Visão Executiva

![Visão Executiva](assets/visao-executiva.png)

### Rentabilidade

![Rentabilidade](assets/rentabilidade.png)

### Descontos

![Descontos](assets/descontos.png)

*Capturas registradas durante o desenvolvimento do relatório.*
S
## Conclusão

O crescimento das vendas foi acompanhado por maior peso dos custos e maior participação de vendas promocionais com margens menores. **Vender mais não garantiu lucrar mais.**

Os achados sugerem revisar campanhas de Eletrônicos, definir descontos considerando a margem e aprofundar a análise de custos por produto e canal. São propostas de ação: a análise é descritiva e não isola o efeito causal das promoções.

## Autor

**Gabriel de Conto Oliveira**

[LinkedIn](https://www.linkedin.com/in/gabriel-de-conto/) · [GitHub](https://github.com/Gab-Bit-bit) · [Portfólio](https://portfoliogabs.netlify.app/)
