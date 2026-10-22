# Nota do CFO

Valores aproximados, marcados como estimativa no `numeros.json`. Não é aconselhamento
tributário; um contador confirma o regime.

- **A margem:** cada assinante deixa R$ 19,52 de R$ 29,90 (65,3%). O lembrete no
  WhatsApp (~R$ 4,20) e o Simples no Anexo V (R$ 4,63) são os dois maiores custos.
- **Equilíbrio:** 25 assinantes pagam a operação. **Para o fundador receber
  R$ 4.000 por mês são 241**, e o plano passa disso no mês 10 (261). Mas o lucro do
  mês 12 ainda é R$ 3.794: enquanto cresce, a empresa gasta R$ 2.400 por mês para
  trazer 60 assinantes novos. A meta só vira dinheiro no bolso quando o crescimento
  desacelera, ou com um CAC menor que os R$ 40 estimados.
- **A linha a vigiar é o preço**, não o churn: a R$ 19,90 o ano 1 dá prejuízo
  (-R$ 3.025); a R$ 39,90 o lucro vai a R$ 26.730 e a meta cai para 164 assinantes.
- **Caixa:** R$ 4.438, acima dos R$ 3.000 do orçamento. Faltam ~R$ 1.400, ou é
  preciso cortar os anúncios de lançamento.
- **Três jeitos de melhorar:**
  1. Preço R$ 39,90 no plano Sem Furo: +R$ 14.878 no ano 1.
  2. Pró-labore de 28% da receita: troca o Anexo V (15,5%) pelo III (6%) e dá o
     caminho com menos clientes para a meta (241 contra 268 só com lucros).
  3. Reduzir lembretes pagos: confirmação dentro da janela de 24 h do WhatsApp sai
     de graça; medir quanto do volume cabe nela.
- **Condições do conselho:** a margem foi refeita com o custo do WhatsApp e o CAC
  (estimado em R$ 40; LTV/CAC 7,0). Falta o uso real de lembretes e o CAC medido.

---

# Economia unitária: Unhas em Dia (exemplo fictício)

Todo número abaixo vem do arquivo de entrada. Nada foi buscado nem chutado.

## Por assinante-mês

| linha | por assinante-mês |
| --- | ---: |
| Preço | R$ 29,90 |
| Lembretes no WhatsApp (estimativa: 120 por mês x R$ 0,035) | -R$ 4,20 |
| Servidor e banco por assinante (estimativa) | -R$ 0,80 |
| Meios de pagamento, mix de Pix e cartão (estimativa) (2,5% do preço) | -R$ 0,75 |
| Simples Nacional, Anexo V (alíquota efetiva do mês 12: 15,5%) | -R$ 4,63 |
| **Margem de contribuição** (o que cada assinante-mês deixa para pagar os fixos) | **R$ 19,52** (65,3%) |

## A margem que importa

Custos fixos: R$ 480 por mês (VPS (estimativa) R$ 100, Contador (estimativa) R$ 300, Domínio, e-mail e ferramentas (estimativa) R$ 80).

- **Ponto de equilíbrio: 25 assinantes ativos.**
- Margem de lucro com a base do mês 12 (342 assinantes): **60,6%**.
- Churn de 7% por mês: um assinante fica em média 14,3 meses.
- **LTV** (margem de contribuição na vida do assinante): R$ 278,83. Para pagar a aquisição com folga, gaste no máximo **R$ 92,94 por assinante** (LTV/3, regra de bolso).
- Custo de aquisição: R$ 40,00 por assinante novo. LTV/CAC: **7,0**; a margem paga a aquisição em 2,0 meses.
- Capacidade: 5000 assinantes.

## Ano 1, mês a mês

| mês | assinantes ativos | receita | lucro | acumulado (após R$ 2.480 iniciais) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 10 | R$ 299 | -R$ 685 | -R$ 3.165 |
| 2 | 24 | R$ 727 | -R$ 606 | -R$ 3.771 |
| 3 | 43 | R$ 1.274 | -R$ 449 | -R$ 4.219 |
| 4 | 65 | R$ 1.932 | -R$ 219 | -R$ 4.438 |
| 5 | 90 | R$ 2.694 | R$ 78 | -R$ 4.359 |
| 6 | 119 | R$ 3.552 | R$ 438 | -R$ 3.921 |
| 7 | 150 | R$ 4.499 | R$ 857 | -R$ 3.064 |
| 8 | 185 | R$ 5.530 | R$ 1.330 | -R$ 1.734 |
| 9 | 222 | R$ 6.638 | R$ 1.853 | R$ 118 |
| 10 | 261 | R$ 7.817 | R$ 2.423 | R$ 2.542 |
| 11 | 303 | R$ 9.064 | R$ 3.037 | R$ 5.578 |
| 12 | 342 | R$ 10.224 | R$ 3.794 | R$ 9.372 |

- **Lucro operacional do ano 1: R$ 11.852** sobre R$ 54.249 de receita.
- Depois dos R$ 2.480 iniciais: R$ 9.372.
- Investimento inicial recuperado: no mês 9.
- Caixa necessário antes de se pagar: **R$ 4.438**.
- Simples no ano 1: R$ 8.409 (15,5% da receita), Anexo V, pelo Fator R.

## Para viver disso

Meta: receber **R$ 4.000,00 por mês**, já descontados os 11% de INSS do pró-labore. Regime estável, mesmos custos de hoje; a RBT12 é 12 vezes a receita do mês.

| jeito de tirar o dinheiro | assinantes ativos | pró-labore | lucro distribuído | anexo | Simples por mês |
| --- | ---: | ---: | ---: | :---: | ---: |
| Tudo em pró-labore | **255** | R$ 4.494 | R$ 13 | III (6%) | R$ 457 |
| Pró-labore no Fator R + lucros | **241** | R$ 2.018 | R$ 2.216 | III (6%) | R$ 432 |
| Só lucros distribuídos | **268** | R$ 0 | R$ 4.000 | V (15,5%) | R$ 1.242 |

O caminho com menos clientes: **pró-labore no Fator R + lucros**, com 241 assinantes ativos.

Lucro distribuído no Simples é isento de IR até o limite presumido; acima dele, só com contabilidade completa. O INSS do sócio tem teto, e o pró-labore paga IR pela tabela. Combine a estratégia com um contador.

## E se

| cenário | margem no plano | equilíbrio (assinantes) | lucro do ano 1 |
| --- | ---: | ---: | ---: |
| Plano base | 60,6% | 25 | R$ 11.852 |
| Preço -10% | 58,2% | 29 | R$ 7.404 |
| Volume -20% | 59,4% | 25 | R$ 8.330 |
| Custos unitários +15% | 57,7% | 26 | R$ 10.288 |
| Churn +50% | 60,0% | 25 | R$ 8.784 |

Nenhum alerta nesses números. Eles valem o que valem as entradas: confira cada custo com um orçamento real.
