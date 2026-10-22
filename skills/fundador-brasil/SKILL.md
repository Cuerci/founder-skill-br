---
name: fundador-brasil
description: >-
  Base brasileira do pacote fundador. Monta e atualiza fundador/mercado.md, o
  dossiê do mercado do negócio no Brasil (tamanho, quem é o cliente, quanto ele
  ganha e gasta, onde está, concorrentes locais e substitutos), com toda
  informação vinda de fonte pública, com link e data. Também guarda em
  regras-br.md as regras que todas as skills fundador-* usam: MEI, Simples
  Nacional e Fator R, taxas do Pix e do Mercado Pago, CDC e direito de
  arrependimento, CONAR, LGPD, INPI e Registro.br. Use quando o usuário disser
  "pesquise o mercado no Brasil", "atualize o dossiê", "quais as regras daqui",
  "quanto é o imposto", "posso ser MEI", ou antes de rodar o pacote num negócio novo.
argument-hint: "[setor ou nicho, ex.: tatuadores, clínicas, e-commerce de moda]"
---

# fundador-brasil

O pacote original foi escrito para os EUA. Esta skill dá a ele o chão brasileiro:
as regras do país (`regras-br.md`, nesta pasta) e o dossiê do mercado do negócio
(`fundador/mercado.md`, no projeto). Todas as outras skills `fundador-*` leem os
dois antes de começar.

O que o usuário digitou depois de `/fundador-brasil`: `$ARGUMENTS`.

## Passo 1: ler o que já existe

- `${CLAUDE_SKILL_DIR}/regras-br.md`: as regras com fonte e data de verificação.
- `fundador/ideia.md` e `fundador/mercado.md`, se existirem.

Se `regras-br.md` tiver itens verificados há mais de 90 dias e o usuário for
decidir preço, imposto ou pagamento, refaça a busca desses itens e atualize a data.

## Passo 2: o dossiê do mercado

Escreva ou atualize `fundador/mercado.md` com estas seções, cada fato com link e a
data em que foi lido:

1. **Tamanho**: quantas pessoas ou empresas são o cliente (Data Sebrae, dados do
   MEI por CNAE, IBGE, associações do setor, eventos do setor). Se não houver
   número oficial, diga isso e dê a melhor estimativa **marcada como estimativa**,
   com o raciocínio.
2. **Quem é o cliente**: renda mensal típica, quanto cobra ou ganha, onde trabalha,
   formal ou informal, região.
3. **Onde ele está**: canais que o cliente usa de verdade (Instagram, WhatsApp,
   TikTok, grupos, eventos, fornecedores).
4. **Quanto ele já gasta com o problema**: ferramentas e serviços que paga hoje,
   com o preço em reais da página oficial ou da loja de apps Brasil.
5. **Concorrentes e substitutos locais**: o resumo; o detalhe é do
   `/fundador-concorrentes`.
6. **Regras específicas do setor**: vigilância sanitária, conselho de classe,
   restrições de publicidade.
7. **Lacunas**: o que não foi possível confirmar e onde procurar.

## Regras

- **Fonte pública, com link e data.** Nunca invente número, preço, estatística ou
  depoimento. Número sem fonte oficial é estimativa e aparece como tal.
- Prefira fontes brasileiras e oficiais (gov.br, IBGE, Sebrae, INPI, Banco Central,
  página de preços da própria empresa). Blog de contabilidade serve de pista, e a
  confiança diminui.
- Quando duas fontes divergem, mostre as duas.
- Não é aconselhamento jurídico, contábil nem tributário.

## Saída

`fundador/mercado.md` e, se mudou alguma regra, `regras-br.md` com a nova data.
Próximo passo: `/fundador-conselho`.
