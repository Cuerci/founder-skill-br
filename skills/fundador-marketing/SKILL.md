---
name: fundador-marketing
description: >-
  Seu diretor de marketing, para o Brasil. Transforma o painel de compradores e o
  mapa de concorrentes em posicionamento, nos canais que o cliente brasileiro usa
  de verdade (Instagram, WhatsApp, TikTok, Google Maps, grupos, eventos do setor,
  parcerias), numa campanha de lançamento de 30 dias com posts e anúncios
  datados, nos dez primeiros ganchos em português, numa divisão de orçamento e nos
  números a acompanhar. Toda mensagem responde a uma objeção levantada por
  compradores reais ou simulados. Use quando o usuário disser "como divulgo isso",
  "plano de marketing", "campanha de lançamento", "como consigo clientes", "onde
  anuncio", "escreve meus anúncios", ou "posicionamento".
argument-hint: "[orçamento em reais]"
---

# fundador-marketing

Negócio de que ninguém ouve falar não existe. Esta skill planeja como os primeiros
clientes ficam sabendo, usando o que o resto do pacote já aprendeu em vez de uma
receita genérica.

## Passo 1: ler as evidências

- `fundador/painel/resultados.md`: quem compra, quem não, e por quê. Os segmentos
  com maior taxa de compra são o primeiro público. As objeções principais são o que
  o marketing precisa responder.
- `fundador/concorrentes.md`: como os concorrentes se posicionam (para não soar
  igual) e a brecha.
- `fundador/mercado.md`: onde o cliente está e como fala.
- `fundador/oferta.md` e `fundador/preco.md`: o que se vende, a que preço.
- `fundador/numeros.json` e `fundador/cfo.md`: quanto vale um cliente, o que limita
  quanto dá para gastar para conquistar um.
- `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md`: CONAR, CDC, LGPD.

Se nada disso existir, diga o que falta e ofereça rodar `/fundador-consumidor
--quick` antes. Não invente público.

## Passo 2: posicionamento

Uma linha, depois os motivos:

```
Para <o segmento que mais compra>, que <o problema nas palavras dele>,
<negócio> é o/a <categoria> que <a brecha>, diferente de <a alternativa mais próxima>.
```

Dê três versões, recomende uma e diga qual evidência do painel sustenta.

## Passo 3: canais

Liste onde o primeiro público gasta atenção, específico para o tipo de negócio e o
lugar: Instagram (Reels, Stories, perfil), TikTok, WhatsApp (lista de transmissão,
grupos, Status), Google Maps e Perfil da Empresa, criadores e microinfluenciadores
do nicho, grupos de Facebook, eventos e convenções do setor, fornecedores que já
falam com o cliente, parcerias, e-mail, anúncios no Meta e no Google. Para cada um:
por que serve para este cliente, custo aproximado em reais e como saber se
funcionou. Escolha dois ou três para começar; diga o que fica de fora e por quê.

## Passo 4: a campanha de 30 dias

`fundador/marketing.md` recebe um calendário datado de 14 dias antes do lançamento
a 16 dias depois: o que sai em cada dia, em qual canal, com qual mensagem. Inclua:

- **Dez ganchos** em português, cada um respondendo a uma objeção do painel ou
  usando um motivo de compra, escritos para o formato (uma frase de abertura de 3
  segundos para vídeo, um título de anúncio, uma mensagem de WhatsApp).
- A oferta da semana de lançamento de `fundador/preco.md` e quando ela acaba.
- O que postar quando não houver nada novo (bastidores, processo, antes e depois
  com autorização).

## Passo 5: orçamento e números

- A divisão do orçamento entre os canais escolhidos, em reais.
- O máximo que dá para pagar por um cliente: do LTV ou da margem de contribuição do
  CFO e das compras por comprador do painel; mostre a conta.
- Os três números a olhar toda semana e o nível que significa "mude algo".

## Regras

- Nada de avaliação, número de seguidores, depoimento, antes e depois ou "visto na
  TV" falsos.
- Citação do painel é pesquisa; nunca use como depoimento de cliente em anúncio.
- Imagem de cliente só com autorização registrada (LGPD).
- Publicidade com influenciador precisa ser sinalizada (#publi), segundo o guia do
  CONAR. Alegações de saúde exigem cuidado redobrado. Não é aconselhamento jurídico.

## Saída

`fundador/marketing.md`. Próximo: `/fundador-marca`, depois `/fundador-lancamento`.
