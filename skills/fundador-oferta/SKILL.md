---
name: fundador-oferta
description: >-
  Monta uma oferta boa demais para recusar, dentro das regras brasileiras. Lista
  todo problema que o cliente encontra até o resultado que quer, transforma cada um
  em solução, fica com o que é barato de entregar e valioso para o cliente, e
  empilha com bônus honestos, uma garantia que o CFO aguenta (lembrando que os 7
  dias de arrependimento do CDC já são lei), urgência real e um nome claro. Dá nota
  na equação de valor (resultado, probabilidade, tempo, esforço) e testa de novo
  num painel rápido. Use quando o usuário disser "melhora minha oferta", "por que
  ninguém compra", "o que eu incluo", "garantia", "bônus", "oferta irresistível",
  ou depois que o painel mostrar gente passando.
argument-hint: "[o que você vende]"
---

# fundador-oferta

A maioria dos negócios vende um produto. Os bons vendem uma oferta: o produto mais
tudo o que torna a compra um sim fácil. Esta skill monta isso usando a lente da
Oferta em `${CLAUDE_SKILL_DIR}/../fundador-conselho/lentes.md` como método (um
resumo do framework de *$100M Offers*, de Alex Hormozi; nunca apresente como
palavras dele).

## Passo 1: ler o que já se sabe

- `fundador/ideia.md` e `fundador/pitch.md`: o que se vende hoje.
- `fundador/painel/resultados.md`: por que os compradores passam, nas palavras
  deles. É a matéria-prima: toda objeção principal deve ser respondida por algo na
  oferta.
- `fundador/numeros.json`: quanto custa cada extra, para a pilha continuar lucrativa.
- `fundador/conselho.md`: as condições do conselho.
- `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md`: CDC, CONAR, LGPD.

## Passo 2: a lista de problemas

Escreva todo obstáculo entre o cliente e o resultado, nas palavras dele: antes de
comprar (dúvida, preço, trabalho de trocar), durante (espera, aprender a usar,
incômodo), depois (dura? e se der errado?). Busque de 15 a 30. Puxe primeiro das
objeções do painel e das reclamações dos concorrentes.

## Passo 3: soluções, cortadas e empilhadas

Transforme cada problema numa solução (um recurso, um serviço, uma garantia, um
formato). Dê nota de valor para o cliente (1 a 5) e custo de entregar (1 a 5, pelos
números do CFO). Fique com valor alto e custo baixo. Empilhe o que sobrou em:

- **O núcleo**: a coisa em si, descrita pelo resultado, não pelos ingredientes.
- **Bônus**: dois ou três, cada um matando uma objeção específica.
- **A garantia**: o que acontece se não entregar. O direito de arrependimento de 7
  dias em compra online (CDC, art. 49) é obrigatório; não o venda como bônus. Uma
  garantia além dele (30 dias, "devolvo se não postar") precisa ser modelada com a
  ferramenta do CFO numa taxa de pedido realista antes de prometer.
- **Urgência e escassez**: só se forem verdade (uma semana de lançamento, as
  primeiras 50 vagas de membro fundador). Nunca contagem regressiva falsa nem "só
  restam 3".
- **O nome**: um nome claro e específico para a oferta, não para a empresa.

## Passo 4: a nota

Na equação de valor, antes e depois, de 1 a 10 cada: resultado dos sonhos,
probabilidade percebida de chegar lá, tempo até o resultado, esforço e sacrifício.
Diga qual item da pilha move qual nota.

## Passo 5: testar de novo

Escreva a oferta nova em `fundador/pitch.md` (guarde a antiga como
`fundador/pitch-v1.md`) e rode `/fundador-consumidor --quick` com a mesma seed.
Informe a taxa de compra antes e depois e quais objeções caíram. Se nada mudou,
diga: o problema pode ser o mercado ou o preço, não a oferta.

## Regras

- Toda promessa precisa ser entregável e caber no bolso; confira com o CFO.
- Nada de avaliação, depoimento, escassez, desconto ou "visto na TV" falsos.
- Siga o CDC e o CONAR para garantias e alegações (de saúde, sobretudo). Não é
  aconselhamento jurídico.

## Saída

`fundador/oferta.md` (lista de problemas, a pilha, os custos, as notas da equação
de valor, o resultado do novo teste) e o `fundador/pitch.md` atualizado. Próximo:
`/fundador-cfo` com os custos da oferta.
