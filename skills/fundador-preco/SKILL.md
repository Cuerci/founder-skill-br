---
name: fundador-preco
description: >-
  Acha o preço que o cliente brasileiro paga de verdade. Lê as quatro respostas de
  preço por comprador (do painel simulado ou, melhor, de um Google Forms com
  clientes reais) numa faixa de sensibilidade de preço Van Westendorp (barato
  demais, pechincha, ficando caro, caro demais), compara com o que os concorrentes
  cobram em reais e com a margem do CFO depois de imposto e taxa do Pix, e
  recomenda um preço, uma escada de planos (básico / intermediário / completo) e
  uma oferta de abertura para testar. Use quando o usuário disser "quanto eu
  cobro", "precifica isso", "R$ X é caro?", "estratégia de preço", "qual preço",
  ou depois do painel de consumidores.
argument-hint: "[preço atual]"
---

# fundador-preco

Preço é a alavanca mais rápida da margem e a que o fundador mais chuta. Esta skill
define o preço a partir de três coisas que dá para conferir: o que os compradores
disseram, o que os concorrentes cobram e o que o negócio precisa ganhar.

Ferramenta nesta pasta:

```bash
python3 "${CLAUDE_SKILL_DIR}/van_westendorp.py" fundador/painel/respostas --preco 50 --out fundador/curva-de-preco.md
```

## Passo 1: o que os compradores disseram

**A melhor fonte é gente de verdade.** Proponha ao usuário um Google Forms curto
para 15 a 40 clientes reais (pelo WhatsApp, Instagram, grupos do setor) com quatro
perguntas, nesta ordem, depois de mostrar o pitch:

1. A que preço por mês você acharia tão barato que duvidaria da qualidade? (`muito_barato`)
2. A que preço você acharia uma pechincha? (`barato`)
3. A que preço começaria a achar caro, mas ainda pensaria em pagar? (`caro`)
4. A que preço seria caro demais e você não pagaria de jeito nenhum? (`muito_caro`)

Exporte o CSV (Google Forms ou Excel brasileiro funcionam: vírgula ou ponto e
vírgula, valores como "R$ 49,90") e renomeie as colunas para esses quatro nomes.

Sem dados reais, use as respostas do painel (`fundador/painel/respostas`). A
ferramenta informa:

| ponto | significado |
| --- | --- |
| PMC | abaixo dele, gente demais acha barato demais para prestar |
| OPP | o preço com menos resistência para os dois lados |
| IPP | onde tantos acham pechincha quanto acham caro |
| PME | acima dele, gente demais não compra |

De PMC a PME é a faixa aceitável. Se nem o painel rodou, diga isso e ofereça
`/fundador-consumidor --quick` ou o formulário. Não invente faixa.

## Passo 2: o que os concorrentes cobram

De `fundador/concorrentes.md` (ou busque agora, nas páginas de preço oficiais, com
links): o preço em reais dos substitutos mais próximos para o mesmo trabalho.
Anote o que cada preço inclui, para comparar igual com igual. Preço gringo em
dólar não é o que o cliente sente: registre se há preço local.

## Passo 3: o que o negócio precisa

De `fundador/numeros.json`: o custo variável por unidade (com o imposto do Simples e
a taxa do Pix como `percentual`, que acompanham o preço) e o ponto de equilíbrio.
Rode a ferramenta do CFO em dois ou três preços candidatos:

```bash
python3 "${CLAUDE_SKILL_DIR}/../fundador-cfo/economia_unitaria.py" fundador/numeros.json --preco 59.90
```

## Passo 4: decidir

Escreva `fundador/preco.md`:

1. **O preço**, e por quê: onde fica na faixa aceitável, contra os concorrentes, e a
   margem que dá (da ferramenta, não de chute).
2. **A escada**, se couber: básico / intermediário / completo (volume, recursos,
   plano anual) com um motivo para subir cada degrau. No Brasil, plano anual pago à
   vista no Pix com desconto é comum e melhora o caixa.
3. **A oferta de abertura**: um preço ou bônus de lançamento que não ensine o
   cliente a esperar promoção, com data para acabar.
4. **O que testar com clientes reais**: dois preços dentro da faixa e como testar
   (duas páginas, pré-venda em cada, oferta para dois grupos de WhatsApp).
5. As três objeções de preço do painel, literais, para o marketing responder.

## Regras

- Respostas de preço de compradores simulados escolhem o que testar. Não são prova.
- Nunca precifique abaixo do custo variável para "comprar" cliente sem dizer isso, e
  por quanto tempo o CFO diz que o negócio aguenta.
- Sem âncora falsa: nada de "de R$ X por" um preço que nunca foi cobrado (é
  publicidade enganosa pelo CDC).
- Mostre o preço final ao consumidor; a taxa do Pix é custo seu, não acréscimo.

## Saída

`fundador/curva-de-preco.md`, `fundador/preco.md`. Se o preço mudou, atualize
`fundador/numeros.json` e rode o `/fundador-cfo` de novo.
