---
name: fundador-consumidor
description: >-
  O painel de consumidores. Cria um enxame de subagentes compradores (100 por
  padrão, --quick para 20) a partir do cliente-alvo brasileiro do usuário, cada um
  com renda mensal, idade, jeito de comprar e objeção diferentes, mostra a todos o
  mesmo pitch em português e passa o negócio por 100 cenários de compra para ver
  quem compra, quem não compra e por quê. Apura as respostas em taxa de compra por
  segmento, os motivos de quem passa nas palavras deles, o que viraria um não, e
  respostas de preço em reais para o fundador-preco. Use quando o usuário disser
  "as pessoas comprariam isso?", "testa com clientes", "roda o painel", "simula
  compradores", "quem é meu cliente", ou "valida a demanda".
argument-hint: "[--n 100 | --quick] [--seed S]"
---

# fundador-consumidor

Em vez de chutar se as pessoas vão comprar, você pergunta para cem delas, cada uma
um subagente fazendo o papel de um comprador tirado do seu cliente-alvo. Você é o
moderador. Você nunca responde por um comprador.

O que o usuário digitou depois de `/fundador-consumidor`: `$ARGUMENTS`

## A ferramenta

Toda a contabilidade passa pelo `painel.py` desta pasta:

```bash
python3 "${CLAUDE_SKILL_DIR}/painel.py" <comando>
```

Abaixo, `PAINEL` significa exatamente isso. Se o caminho não expandir, use o
diretório base que o Claude Code mostrou para esta skill. O estado fica em
`fundador/painel/`.

## Passo 1: o cliente-alvo

Escreva `fundador/cliente.json` (formato: `cliente.exemplo.json` nesta pasta):

- `negocio`, e `alvo`: quem é o cliente, numa linha específica.
- `segmentos`: 2 a 4 grupos com `share` e `renda_mensal` [mínima, máxima] em reais
  **por mês** (como o brasileiro fala de renda).
- `comportamentos`: 4 a 8 jeitos de comprar com `share` e uma linha `como`
  (freguês fiel, caçador de promoção, só compra com indicação, fiel a um
  concorrente, só paga no Pix...).
- `objecoes`: as 4 a 8 dúvidas reais desse tipo de cliente.
- `habitos` (opcional): linhas do dia a dia que deixam o comprador concreto.
- `idade` (opcional): [mínima, máxima].

Baseie em algo real. Use o que o usuário sabe dos clientes, `fundador/mercado.md`
(renda e realidade do setor no Brasil) e, se o `/fundador-concorrentes` rodou, as
reclamações em `fundador/concorrentes.md`. Se o usuário tiver dados reais
(entrevistas, avaliações, respostas de formulário), prefira-os aos seus palpites e
diga quais partes são palpite. Mostre o perfil em poucas linhas e deixe o usuário
corrigir antes de distribuir: cliente errado deixa o painel inteiro errado.

## Passo 2: o pitch

Escreva `fundador/pitch.md`: o que o comprador veria de verdade, em português. O
produto, o preço em reais, onde e como conseguir, como paga (Pix, cartão), alguma
oferta de abertura. Três a seis linhas simples, sem superlativos, nada que o negócio
não consiga entregar. Todo comprador vê exatamente isso.

## Passo 3: distribuir e rodar

```bash
PAINEL init --cliente fundador/cliente.json --pitch fundador/pitch.md --n 100
PAINEL prompts
```

`init` distribui as fichas (mesma seed, mesmas fichas; a seed fica registrada).
`prompts` escreve um briefing por comprador e lista em ondas de 10. Para cada onda,
mande UMA mensagem com uma chamada da ferramenta Agent por comprador da onda:

- `subagent_type`: `general-purpose`
- `description`: `painel <id>`
- `prompt`: `Leia <caminho do briefing> e siga exatamente. É todo o seu briefing.`

Espere a onda inteira antes da próxima. O Claude Code roda cerca de 10 chamadas ao
mesmo tempo, então 100 compradores são 10 ondas. Depois da última:

```bash
PAINEL check      # lista respostas faltando ou quebradas
PAINEL prompts    # reescreve briefings só para essas; rode mais uma vez
PAINEL tally
```

Se um comprador imprimiu o JSON na resposta em vez de gravar o arquivo (acontece),
arquive a resposta dele com `PAINEL save <id>` e a resposta no stdin; `save` recusa
o que não for resposta válida. Comprador que falha duas vezes fica de fora e é
contado no resultado. Nunca escreva uma resposta por um comprador.

Antes de uma rodada de 100, avise o usuário que são 100 chamadas de subagente
(custo de tokens alto) e sugira `--quick` (20 compradores) para uma primeira
olhada. Os subagentes gravam um arquivo cada em `fundador/painel/respostas/`; no
modo de permissão padrão é uma aprovação por arquivo, então sugira o modo
accept-edits (Shift+Tab) para a rodada.

## Passo 4: contar ao usuário

`PAINEL tally` grava `fundador/painel/resultados.md` e `resultados.json`. Diga:

1. A manchete: "40 compram · 60 passam" e a taxa de compra.
2. Quem compra e quem não: as linhas de segmento e comportamento que mais diferem.
3. Por que passam: os três motivos principais com uma citação cada, como escrita.
4. O que viraria um não: as respostas mais repetidas.
5. Uma frase sobre o que mudar antes de gastar dinheiro, e qual skill faz isso
   (preço, oferta, marketing).

## Limites honestos, diga uma vez

São compradores simulados. São bons para revelar objeções, segmentos e palavras em
que você não tinha pensado, e ruins para prever conversão real: modelos de
linguagem tendem a concordar, então trate a taxa de compra como teto. Eles também
não conhecem a fundo o dia a dia do nicho no Brasil; um perfil bem baseado em
`fundador/mercado.md` reduz isso, mas não elimina. Confirme as grandes decisões com
gente de verdade (lista de espera, pré-venda, página com preço, conversa no
WhatsApp) antes de assinar qualquer coisa. Nunca apresente citações do painel como
depoimento de cliente.

## O briefing de cada comprador

`painel.py` preenche a ficha num modelo fixo (veja `BRIEF` no script): quem é o
comprador (nome, idade, segmento, renda mensal, jeito de comprar, um hábito, a
dúvida que vem à cabeça), o pitch palavra por palavra, a instrução de não ser
agradável e não inventar fatos, e o JSON exato a gravar: compra, compras no
primeiro mês, um código de motivo, o motivo na voz dele, a objeção principal, o que
mudaria a ideia dele e quatro respostas de preço em reais (barato demais, pechincha,
ficando caro, caro demais). Nunca edite o briefing de um comprador só.

## Saída

`fundador/cliente.json`, `fundador/pitch.md`, `fundador/painel/` (fichas,
briefings, respostas, resultados). Próximo: `/fundador-preco` lê as respostas de
preço, `/fundador-oferta` e `/fundador-marketing` leem as objeções.
