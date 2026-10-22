---
name: fundador-concorrentes
description: >-
  Mapeia cada concorrente e a brecha que eles deixam, no Brasil. Acha os
  concorrentes diretos, os indiretos e os substitutos que o cliente usaria no
  lugar, só de fontes públicas, e registra o que cada um vende, o preço em reais,
  como se posiciona e do que os clientes reclamam (Reclame Aqui, avaliações da
  Google Play e App Store Brasil, Google Maps, comentários no Instagram), cada fato
  com link. Termina com um mapa de posicionamento e a brecha que o negócio novo
  pode ocupar. Use quando o usuário disser "quem são meus concorrentes", "o
  mercado está lotado?", "o que mais existe", "análise de concorrência", "acha a
  brecha", ou "contra quem eu vou brigar".
argument-hint: "[cidade ou mercado]"
---

# fundador-concorrentes

Todo cliente já resolve esse problema de algum jeito. Esta skill descobre como, quanto
ele paga e do que ele reclama, para o negócio novo começar com uma brecha em vez de
um chute.

## As regras

- **Só fonte pública, todo fato com link.** Sites, páginas de preço, cardápios,
  Google Play e App Store **Brasil**, Google Maps, Reclame Aqui, Reddit, grupos
  públicos, notícias. Se uma fonte não abrir, diga. Nunca invente concorrente,
  preço, nota ou avaliação.
- **Leia, não raspe.** Leia as páginas como uma pessoa leria. Respeite os termos de
  cada site.
- **Citações literais**, curtas, com link. São pesquisa, nunca depoimento.
- **Preço em reais**, como o cliente brasileiro paga. Se só houver preço em dólar,
  registre em dólar e diga que não há preço local.

## Passo 1: quem está lá

Leia `fundador/ideia.md` (escreva antes se faltar; veja `/fundador-conselho` passo 0),
`fundador/mercado.md` e `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md`.

| tipo | o que significa | exemplo para uma cafeteria |
| --- | --- | --- |
| Direto | vende a mesma coisa para o mesmo cliente | outras cafeterias a uma caminhada |
| Indireto | outro produto para o mesmo trabalho | a padaria da esquina |
| Substituto | como o cliente resolve sem empresa | café passado em casa |

Busque de 5 a 10 diretos e indiretos, mais os principais substitutos. Para negócio
local, busque no mapa da região exata; para online, busque como o cliente buscaria
em português ("melhor <coisa> para <quem>", "<coisa> alternativa", "app para
<profissão>") e também em inglês, porque muita ferramenta gringa é usada aqui.

## Passo 2: os fatos

Uma linha por concorrente em `fundador/concorrentes.csv`:

`nome,tipo,url,local_ou_canal,preco_do_item_comparavel,o_que_vende,frase_de_posicionamento,nota,num_avaliacoes,em_portugues,data_da_fonte`

`frase_de_posicionamento` é o título ou slogan deles, copiado. O preço é o do item
mais próximo do que o negócio novo vende, com o que inclui. `em_portugues` diz se o
produto tem interface e suporte em português: para muito cliente brasileiro, isso
decide.

## Passo 3: o que os clientes deles dizem

Para os 3 a 5 principais, leia as avaliações (1 a 3 estrelas primeiro, depois as de
4 estrelas com "adoro, mas..."). No Brasil, olhe também o Reclame Aqui e os
comentários públicos no Instagram. Anote as reclamações que se repetem como temas,
com contagem e uma ou duas citações com link. Marque como fraco um tema com menos
de três avaliações.

## Passo 4: o mapa e a brecha

Escreva `fundador/concorrentes.md`:

1. A tabela (do CSV), ordenada por quão diretamente cada um concorre.
2. Faixa de preço: menor, mediano, maior para o item comparável.
3. Um mapa de posicionamento em texto: dois eixos que importam para este cliente
   (preço e facilidade, qualidade e rapidez...) e onde cada concorrente fica.
4. As reclamações, ranqueadas, com links.
5. **A brecha**: o que ninguém faz bem e este negócio poderia fazer, amarrado às
   evidências. Se não houver brecha, diga com clareza; é o resultado mais útil que
   esta skill pode dar.
6. A ameaça: quem copiaria o negócio novo mais rápido, e como.

## Saída

`fundador/concorrentes.csv`, `fundador/concorrentes.md`. Próximo:
`/fundador-consumidor` usa as reclamações para escrever objeções reais;
`/fundador-preco` usa a faixa de preço.
