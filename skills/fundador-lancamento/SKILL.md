---
name: fundador-lancamento
description: >-
  Seu líder de lançamento. Monta um plano de lançamento datado e passo a passo: um
  teste barato no mundo real primeiro (lista de espera, pré-venda no Pix, oferta de
  membro fundador ou um piloto com preço real, para clientes de verdade confirmarem
  o que o painel simulado disse), depois a contagem regressiva até o dia do
  lançamento com responsáveis e prazos, o roteiro do dia e os primeiros 30 dias
  do que medir e do que mudar. Use quando o usuário disser "como eu lanço", "plano
  de lançamento", "quando posso abrir", "checklist de lançamento", "colocar no ar",
  ou "soft opening".
argument-hint: "[data alvo de lançamento]"
---

# fundador-lancamento

Lançar é um projeto com data. Esta skill transforma o resto do pacote num plano
datado e começa pelo jeito mais barato de descobrir se gente de verdade paga, antes
de o dinheiro grande sair.

## Passo 1: testar antes de gastar

Escolha o teste real mais barato que serve ao negócio, e rode antes de assumir os
custos grandes de `fundador/numeros.json`:

| negócio | o teste |
| --- | --- |
| loja física ou cafeteria | uma barraca em feira, um pop-up ou uma lista de encomenda com preço e data |
| produto online | uma página com o preço e um botão de "reservar" ou "entrar na lista de espera" |
| serviço | três clientes piloto pagando o preço planejado |
| assinatura ou SaaS | uma oferta de membro fundador paga adiantado no Pix, com vagas limitadas de verdade |

Para chegar ao público no Brasil, use os canais de `fundador/marketing.md`: direct
no Instagram, grupos de WhatsApp do nicho, eventos do setor, indicação de quem já é
referência.

Escreva a linha de sucesso antes de rodar (por exemplo: 30 membros fundadores
pagos em duas semanas a R$ 50), e compare o resultado com a taxa de compra do
painel. Se os compradores reais ficarem bem abaixo do painel, confie nos reais e
volte ao `/fundador-oferta` ou ao `/fundador-preco`. Lembre que cada pré-venda
online tem 7 dias de arrependimento (CDC): conte só o que passou desse prazo.

## Passo 2: a contagem regressiva

De hoje até o dia do lançamento, com datas reais (pergunte a data alvo; o padrão é
a mais cedo realista, dados os prazos de `fundador/operacoes.md`). Blocos semanais,
cada tarefa com responsável e prazo:

- Jurídico e dinheiro: CNPJ, conta PJ, conta no meio de pagamento, emissão de nota,
  termos de uso e política de privacidade, licenças de `fundador/operacoes.md`.
- Construção: reforma ou produto, fornecedores pedidos pelos prazos deles.
- Marca: perfis, domínio, materiais de `fundador/marca.md`.
- Marketing: o calendário de `fundador/marketing.md` a partir de 14 dias antes.
- Equipe: contratação e treino nos POPs.
- Um soft opening ou beta fechado com amigos e clientes piloto antes do público.

Marque o caminho crítico: as tarefas que empurram a data se atrasarem.

## Passo 3: o dia do lançamento

Um roteiro hora a hora: quem está onde, o que sai em qual canal, a oferta de
abertura, o que fazer se algo quebrar (do registro de riscos).

## Passo 4: os primeiros 30 dias

Os números semanais a acompanhar (do CFO: vendas ou assinantes contra o ponto de
equilíbrio, churn; do marketing: os números dos canais), o nível que dispara uma
mudança, e uma revisão nos dias 7, 14 e 30 com as perguntas a responder.

## Saída

`fundador/lancamento.md` com o teste, a contagem regressiva, o roteiro do dia e a
revisão de 30 dias. Próximo: `/fundador-plano` junta tudo no plano de negócio.
