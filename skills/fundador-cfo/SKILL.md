---
name: fundador-cfo
description: >-
  Seu CFO, em reais. Monta a economia unitária de um negócio antes de gastar: o que
  uma unidade deixa depois dos custos diretos (incluindo imposto do Simples e taxa
  do Pix ou do cartão), a margem de lucro real no volume planejado, o ponto de
  equilíbrio, o ano 1 mês a mês, o caixa necessário até se pagar, quando o
  investimento inicial volta, e o que acontece se o preço cair, as vendas vierem
  abaixo ou os custos subirem. Tem modo assinatura para SaaS, com churn, LTV e o
  máximo a pagar por cliente. Todo número vem de uma entrada que o usuário pode
  conferir. Use quando o usuário disser "acha as margens", "faz as contas", "isso
  dá lucro?", "ponto de equilíbrio", "economia unitária", "quanto preciso para
  começar", "LTV", "churn" ou "roda o CFO".
argument-hint: "[caminho do numeros.json]"
---

# fundador-cfo

A pessoa que pergunta "e quanto custa isso?". Margem decide se uma boa ideia é um
negócio. Esta skill encontra a margem, com todo número rastreável até uma entrada.

Ferramenta nesta pasta:

```bash
python3 "${CLAUDE_SKILL_DIR}/economia_unitaria.py" fundador/numeros.json --out fundador/cfo.md
```

## Passo 1: juntar as entradas

Leia `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md` (imposto, taxas, MEI).
Escreva `fundador/numeros.json`. Formatos nesta pasta: `exemplo.json` (cafeteria,
modo dia), `exemplo-venda-unica.json` (curso online, modo mês) e
`exemplo-assinatura.json` (SaaS, modo assinatura).

| campo | o que vai nele |
| --- | --- |
| `unidade` | o que é uma venda: um copo, um pedido, um assinante-mês |
| `preco` | preço por unidade em reais, o que o cliente paga |
| `variavel` | o custo de UMA unidade: insumos, embalagem, frete, comissões. Use `{"item", "percentual"}` para o que é proporcional ao preço: **imposto do Simples**, taxa do Pix, do cartão, do marketplace |
| `fixo_mensal` | o que se paga todo mês de qualquer jeito: servidor, aluguel, salários, pró-labore, contador, ferramentas |
| `inicial` | gasto único antes de abrir: abertura do CNPJ, registro no INPI, equipamento, reforma, anúncios de lançamento |

Modo dia (padrão): `dias_por_mes`, `plano_por_dia`, `rampa_por_dia` (12 números),
`capacidade_por_dia`.

Modo mês (`"modelo": "mes"`), para venda única contada por mês (curso, e-book,
template, app pago uma vez, projeto): `plano_por_mes`, `rampa_por_mes` (12 números),
`capacidade_por_mes`. O custo de aquisição por venda entra em `variavel`.

Modo assinatura (`"modelo": "assinatura"`): `novos_por_mes` (12 números),
`churn_mensal` (fração que cancela ou não renova por mês), `assinantes_iniciais`,
`capacidade_assinantes` e `custo_aquisicao` (R$ por assinante novo, gasto no mês
em que ele chega; dá o LTV/CAC e em quantos meses a margem paga a aquisição). Plano pré-pago no Pix sem renovação automática tem churn
alto: quem não paga de novo conta como churn.

De onde vêm os números, nesta ordem:

1. Orçamentos, notas, contratos e tabelas de preço do próprio usuário.
2. Preços públicos que dá para conferir (página de preço do provedor, tarifa do
   Mercado Pago, tabela do Simples). Anote a fonte ao lado do número em
   `fundador/cfo-fontes.md`.
3. Sua estimativa, marcada claramente como estimativa, com o raciocínio. Nunca
   apresente estimativa como fato.

Pergunte ao usuário o que só ele sabe (aluguel, salário que vai pagar, quanto quer
de pró-labore). Use o preço de `fundador/preco.md` ou `fundador/pitch.md` se
existirem.

**Imposto não é opcional.** Sempre inclua o imposto sobre a receita como
`percentual` e diga qual regime e anexo foi assumido. Para SaaS: Simples Anexo III
(6%) só se o Fator R passar de 28%; sem pró-labore, o cenário honesto é o Anexo V
(15,5%). SaaS não pode ser MEI hoje.

**O pró-labore do fundador é custo.** Se o fundador vai viver disso, ponha um
pró-labore em `fixo_mensal`; senão o "lucro" é o salário dele disfarçado.

**A rampa é onde os planos mentem.** O mês 1 quase nunca é o volume do plano. Se o
painel rodou, use a taxa de compra e as compras do primeiro mês para conferir a
rampa (`fundador/painel/resultados.md`) e diga como fez.

## Passo 2: rodar

```bash
python3 "${CLAUDE_SKILL_DIR}/economia_unitaria.py" fundador/numeros.json --out fundador/cfo.md
```

Grava: a tabela por unidade e a margem de contribuição, os custos fixos, o ponto de
equilíbrio (por dia, por mês ou em assinantes ativos), a margem de lucro no plano, o ano 1
mês a mês, o lucro operacional do ano 1 e o resultado depois do investimento
inicial, o caixa necessário, o mês em que o investimento volta e uma tabela de
cenários (preço -10%, volume -20%, custos unitários +15% e, no modo assinatura,
churn +50%). No modo assinatura também dá o LTV, o máximo a pagar por assinante e,
com `custo_aquisicao`, o LTV/CAC (alerta abaixo de 3).
Alerta para preço abaixo do custo variável, equilíbrio acima da capacidade, ano 1
com prejuízo e retorno depois de 12 meses.

Cenários sem editar o arquivo:

```bash
python3 "${CLAUDE_SKILL_DIR}/economia_unitaria.py" fundador/numeros.json --preco 59.90
python3 "${CLAUDE_SKILL_DIR}/economia_unitaria.py" fundador/numeros.json --volume 0.8
```

## Passo 3: a nota do CFO

Acrescente uma seção curta no topo de `fundador/cfo.md`, em palavras simples:

- **A margem**: a margem de lucro no plano e a margem de contribuição por unidade.
- **A linha a vigiar**: o custo ou a premissa que mais mexe no resultado
  (normalmente a rampa, o churn, o aluguel ou o preço), com o cenário que prova.
- **Caixa**: quanto dinheiro o fundador precisa antes de se pagar.
- **Três jeitos de melhorar a margem**, cada um com o número que muda e quanto
  (rode o cenário, não chute).
- Se as condições financeiras do conselho (`fundador/conselho.md`) foram cumpridas.

## Regras

- Todo número da sua nota vem da saída da ferramenta ou de uma entrada que você
  sabe nomear.
- Diga uma vez que um contador deve confirmar o regime, o anexo, o pró-labore e os
  encargos antes de o dinheiro sair. Não é aconselhamento financeiro, tributário nem
  jurídico.

## Saída

`fundador/numeros.json`, `fundador/cfo.md`, `fundador/cfo-fontes.md`. Próximo:
`/fundador-plano` usa estes números no veredito; `/fundador-preco` se a margem
estiver apertada.
