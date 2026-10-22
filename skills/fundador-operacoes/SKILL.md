---
name: fundador-operacoes
description: >-
  Seu gerente de operações, no Brasil. Define como o negócio roda no primeiro dia:
  fornecedores e quanto custam, quem trabalha quando, as rotinas passo a passo
  (para negócio físico: abrir, atender, fechar; para SaaS: cadastro, pagamento no
  Pix, suporte no WhatsApp, backup, reembolso), as ferramentas, a empresa e as
  licenças a conferir (CNPJ, CNAE, Simples, alvará, vigilância sanitária, LGPD) e
  um registro de riscos com o que fazer quando cada coisa der errado. Devolve
  custos reais para o CFO. Use quando o usuário disser "como eu rodo isso",
  "operação", "fornecedores", "equipe", "processos", "o que preciso para abrir",
  "licenças", "alvará" ou "primeiro dia".
argument-hint: "[cidade e estado]"
---

# fundador-operacoes

Plano que funciona no papel quebra às 7h de uma segunda-feira. Esta skill garante
que o primeiro dia, a primeira semana e o primeiro mês dão para ser tocados, e que
os números do CFO incluem o que custa tocar.

## Passo 1: o que o negócio faz todo dia

De `fundador/ideia.md`, `fundador/oferta.md` e `fundador/numeros.json`, escreva o
ciclo diário como lista de passos do primeiro ao último (para uma cafeteria:
entrega, preparo, abrir, atender, limpar, fechar o caixa, pedir; para um SaaS:
cadastros, pagamentos no Pix confirmados, processamento, suporte no WhatsApp,
monitoramento do servidor, backup, pedidos de reembolso e de exclusão de dados).
Marque quais passos o cliente vê.

## Passo 2: fornecedores

Para todo item dos custos variáveis do CFO e todo equipamento ou serviço: dois ou
três fornecedores reais que o usuário pode contatar (no Brasil, ou gringos que
cobram em dólar, com o efeito do câmbio e do IOF), preços públicos ou como pedir
orçamento, pedido mínimo, prazo e condições de pagamento. Linke as fontes. Onde só
um orçamento dirá, registre nas perguntas abertas. Se um preço real diferir de
`fundador/numeros.json`, atualize e diga que o CFO precisa rodar de novo.

## Passo 3: pessoas

Quem faz o quê, quando: uma escala semanal para o volume planejado e para o mês
lento do começo. As funções, as horas e a premissa de salário (do usuário, ou de
fonte pública para o piso e a média da região, com link). Encargos de CLT, pró-labore
e INSS variam; sinalize para o contador.

## Passo 4: rotinas (POPs)

Rotinas curtas e numeradas para os momentos que fazem ou quebram o negócio: o
serviço principal, atender uma reclamação, pedido de reembolso dentro dos 7 dias do
CDC, pedido de exclusão de dados pela LGPD, e uma revisão semanal. Cada uma cabe
numa página que alguém seguiria no primeiro dia.

## Passo 5: ferramentas

A menor pilha que roda o negócio: pagamentos (Pix, cartão), emissão de nota fiscal
de serviço (NFS-e da prefeitura ou um emissor), contabilidade, atendimento
(WhatsApp Business), agenda, estoque se houver. Produtos reais com preço publicado
em reais, e por quê.

## Passo 6: empresa, licenças e seguros

Uma checklist do que esse tipo de negócio costuma precisar na cidade e no estado do
usuário, cada item com a página oficial para confirmar:

- Natureza jurídica e regime (MEI, ME no Simples, SLU), CNAE certo, inscrição
  municipal. Veja `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md` (SaaS não
  pode ser MEI).
- Alvará de funcionamento, licença sanitária, AVCB dos bombeiros (negócio físico).
- Nota fiscal de serviço e ISS do município.
- LGPD: política de privacidade, termos de uso, encarregado, onde os dados ficam.
- Seguros que fazem sentido.

Diga com clareza que as regras mudam por município e com o tempo, e que o usuário
precisa confirmar cada item com o órgão ou um profissional. Não é aconselhamento
jurídico.

## Passo 7: registro de riscos

As dez coisas com mais chance de dar errado (servidor cai, Pix não confirma, um
fornecedor some, uma pessoa-chave adoece, uma avaliação ruim, um mês fraco, um
vazamento de dados), cada uma com probabilidade, gravidade e o plano.

## Saída

`fundador/operacoes.md`, mais `fundador/numeros.json` atualizado se custos reais
mudaram. Próximo: `/fundador-lancamento`.
