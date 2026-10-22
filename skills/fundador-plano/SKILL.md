---
name: fundador-plano
description: >-
  Seu planejador de negócio. Junta tudo o que as outras skills fundador
  escreveram (o dossiê do mercado brasileiro, o voto do conselho, os concorrentes,
  o painel de compradores, o preço, a oferta, os números do CFO, o marketing, a
  marca, a operação e o plano de lançamento) num plano de negócio com um veredito
  no topo calculado pelos números, nunca escrito à mão: Lucrativo, Ainda não (com
  os números que falham) ou Incompleto. Acrescenta um resumo executivo e uma
  versão de uma página para sócio, banco ou investidor. Use quando o usuário
  disser "escreve meu plano de negócio", "junta tudo", "dá lucro?", "me dá o
  plano", ou no fim do pacote fundador.
argument-hint: "[--taxa-minima 0.25]"
---

# fundador-plano

O último passo. Um documento em que o fundador pode agir, ou entregar a um sócio ou
a um banco, feito só com o que o pacote encontrou.

Ferramenta nesta pasta:

```bash
python3 "${CLAUDE_SKILL_DIR}/compilar.py" --dir fundador
```

## Passo 1: ver o que existe

```bash
python3 "${CLAUDE_SKILL_DIR}/compilar.py" --dir fundador --check
```

imprime o veredito e cada checagem. As checagens, todas calculadas:

1. Cada unidade dá dinheiro antes dos custos fixos (`fundador/numeros.json`).
2. O ano 1 dá lucro operacional.
3. O ponto de equilíbrio cabe na capacidade, se houver capacidade.
4. O plano chega à meta de renda do fundador no mês 12, se o CFO tiver
   `meta_renda_mensal`. Sem meta, avise que "Lucrativo" não diz se o fundador vive
   do negócio.
5. Compradores simulados suficientes compram (`fundador/painel/resultados.json`;
   régua padrão de 25%, mude com `--taxa-minima` e diga por quê).

Sem números, o veredito é Incompleto: ofereça rodar `/fundador-cfo`. Liste as outras
seções que faltam com a skill que preenche cada uma. Não preencha uma seção que
falta com palpites.

## Passo 2: o resumo

Escreva `fundador/resumo.md`, meia página, palavras simples:

- O que é o negócio e para quem, em duas frases.
- O veredito e os três números por trás dele (margem, equilíbrio, ano 1).
- No que o painel e o conselho concordaram e onde discordaram.
- O maior risco e o que será feito a respeito.
- Do que o fundador precisa para começar (o caixa do CFO, o primeiro teste do
  lançamento, a empresa a abrir).
- A única coisa a fazer esta semana.

Se o veredito for Ainda não, o resumo começa pelo que precisa mudar e qual skill
muda. Nunca suavize uma checagem que falhou.

## Passo 3: compilar

```bash
python3 "${CLAUDE_SKILL_DIR}/compilar.py" --dir fundador
```

grava `fundador/plano-de-negocio.md`: título, o veredito e as checagens, a tabela de
números-chave, a ideia, depois cada seção que o pacote produziu (resumo, conselho,
mercado, concorrência, painel, preço, oferta, números, marketing, marca, operação,
lançamento) e o que ainda falta.

## Passo 4: a página única

Escreva `fundador/uma-pagina.md` para quem decide em dois minutos: o problema, o
cliente, a oferta e o preço, a tabela de números, as evidências (resultado do
painel, brecha nos concorrentes, algum teste real), para que é o dinheiro e o
pedido. Os mesmos números do plano, palavra por palavra.

## Regras

- O veredito vem do `compilar.py`. Nunca escreva Lucrativo à mão e nunca
  arredonde um número que falha para um que passa.
- Diga uma vez, com clareza: o painel é de compradores simulados e os números são
  projeções; clientes reais e orçamentos reais confirmam. Não é aconselhamento
  financeiro, jurídico nem tributário.
- Se o usuário quiser PDF ou apresentação, ofereça exportar o plano, mas mantenha o
  markdown como fonte da verdade.

## Saída

`fundador/resumo.md`, `fundador/plano-de-negocio.md`, `fundador/uma-pagina.md`.
Depois diga ao usuário o veredito numa linha e a única coisa a fazer esta semana.
