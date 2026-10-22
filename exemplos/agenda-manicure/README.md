# Exemplo completo: Unhas em Dia

O pacote inteiro rodado de ponta a ponta numa ideia **fictícia**: uma agenda com
lembrete no WhatsApp para manicures autônomas, a R$ 29,90 por mês. A pesquisa de
mercado e de concorrentes é real e tem link; o negócio, os custos estimados e as
compradoras do painel são inventados.

## O que saiu

**Veredito: Ainda não.** A conta fecha, mas a demanda não: só 3 de 20 compradoras
simuladas compram (15%, a régua é 25%).

O que o pacote ensinou, em ordem:

1. **Mercado** (`mercado.md`): o CNAE de cabeleireiros, manicure e pedicure é o
   maior do MEI, com ~1,06 milhão. Uma falta custa de R$ 25 a R$ 300.
2. **Conselho** (`conselho.md`): 3 votos "investe se", nota média 5,3. Todos pedem o
   mesmo número, que ninguém tem: quantas faltas a manicure tem hoje.
3. **Painel** (`painel/resultados.md`): 13 dos 17 nãos são hábito ("minhas clientes
   marcam pelo WhatsApp"). Mas **3 de 4 manicures que sofrem com falta compram**, e
   o pedido que mais aparece para virar um não é **sinal no Pix**.
4. **Preço** (`preco.md`): o painel inteiro acha R$ 29,90 caro, e o segmento que
   compra aceita até R$ 45. A R$ 19,90 o ano 1 dá prejuízo; a R$ 39,90 o lucro mais
   que dobra.
5. **Oferta** (`oferta.md`): de "agenda" para **"Sem Furo"**: lembrete, confirmação
   de um toque, sinal no Pix e lista de espera.
6. **CFO** (`cfo.md`): 25 assinantes pagam a operação; **241 pagam o fundador**
   (R$ 4.000 por mês, pró-labore no Fator R + lucros).
7. **Lançamento** (`lancamento.md`): 50 vagas de fundadora no Pix e um piloto de 10
   manicures medindo faltas antes de gastar.

## Os arquivos

Tudo em [`fundador/`](fundador/), na ordem do pacote:

`ideia.md` → `mercado.md` → `conselho/` e `conselho.md` → `concorrentes.md` →
`cliente.json`, `pitch.md`, `painel/` → `curva-de-preco.md`, `preco.md` →
`oferta.md` → `numeros.json`, `cfo.md` → `marketing.md` → `marca.md` →
`operacoes.md` → `lancamento.md` → `resumo.md`, `plano-de-negocio.md`, `uma-pagina.md`

Os briefings de cada compradora estão em `painel/briefings/` e as respostas em
`painel/respostas/`: dá para conferir que nenhuma resposta foi escrita à mão.

## O que ficou de fora

- O novo teste da oferta no painel (`/fundador-consumidor --quick --seed 42` com o
  pitch Sem Furo).
- As buscas de INPI, domínio e arroba da marca.
- As avaliações dos concorrentes na Google Play BR.

Para reproduzir os números:

```bash
python3 skills/fundador-cfo/economia_unitaria.py exemplos/agenda-manicure/fundador/numeros.json
python3 skills/fundador-preco/van_westendorp.py exemplos/agenda-manicure/fundador/painel/respostas --preco 29.90
python3 skills/fundador-plano/compilar.py --dir exemplos/agenda-manicure/fundador --check
```
