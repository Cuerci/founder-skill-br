---
name: fundador-marca
description: >-
  Seu designer de marca, no Brasil. Dá nome ao negócio (com as checagens de INPI,
  Registro.br e arroba a fazer antes de se apaixonar por um nome), escreve a voz,
  uma promessa de uma linha e um slogan em português, e faz o briefing do visual:
  cores, tipografia, logo e as primeiras coisas que o cliente vê, alinhados ao
  posicionamento que o diretor de marketing escolheu. Use quando o usuário disser
  "dá um nome", "cria a marca", "logo", "identidade visual", "como deve parecer",
  "slogan", ou "tom de voz".
argument-hint: "[ideias de nome, se houver]"
---

# fundador-marca

Marca é a promessa que o cliente lembra. Esta skill a torna específica para o
posicionamento que o pacote já achou, e não um painel de cores bonitas.

## Passo 1: ler o briefing

`fundador/ideia.md`, `fundador/marketing.md` (a linha de posicionamento e o primeiro
público), `fundador/concorrentes.md` (nomes e visuais a evitar), `fundador/mercado.md`
(como o cliente fala) e os motivos de compra do painel
(`fundador/painel/resultados.md`). Se faltar o posicionamento, peça ou rode
`/fundador-marketing` antes.

## Passo 2: candidatos a nome

Dez candidatos em estilos diferentes (descritivo, evocativo, inventado, o nome do
fundador, uma gíria do nicho, um termo em inglês que o nicho já usa). Para cada um:
o que diz, como soa em voz alta em português, se tem duplo sentido ou pronúncia
difícil, como fica num ícone de app e numa arroba, e o risco. Depois, escolha três
e liste as checagens que o usuário precisa concluir:

- **Marca no INPI**: busca na [base do INPI](https://busca.inpi.gov.br/pePI/) pelo
  nome nas classes de Nice certas (para SaaS: 42 e 9; veja
  `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md` para custo e prazo). Se o
  negócio mira fora do Brasil, acrescente USPTO e EUIPO.
- **Domínio**: se o `.com.br` está livre no [Registro.br](https://registro.br) e se
  o `.com` está livre (confira, não suponha); boas alternativas se não estiverem.
- **Arrobas**: Instagram, TikTok, YouTube, e o nome no WhatsApp Business.
- **Confusão**: nenhum nome parecido com um concorrente de `fundador/concorrentes.md`.

Diga com clareza que você só faz buscas públicas, que um advogado ou agente de
propriedade industrial confirma, e que nada fica registrado até o usuário pedir o
registro.

## Passo 3: voz e promessa

- A promessa de uma linha (o que o cliente pode esperar, sempre).
- Um slogan, três opções.
- A voz em três adjetivos, cada um com um faça e um não faça, e uma reescrita
  antes e depois de uma linha de `fundador/pitch.md`.

## Passo 4: o visual, como briefing

- **Cores**: 2 a 3 cores principais com hex e a função de cada uma, mais a checagem
  de contraste do texto sobre cada uma (WCAG AA no mínimo).
- **Tipografia**: uma fonte de título e uma de texto, gratuitas ou licenciadas, com
  onde baixar e suporte completo a acentos do português. Nenhuma fonte sem licença.
- **Briefing do logo**: o que precisa dizer, onde precisa funcionar (ícone de app
  de 32px, marca d'água numa foto, avatar redondo do Instagram), o que evitar.
  Ofereça gerar conceitos com uma ferramenta de imagem se o usuário tiver; marque
  conceitos gerados como conceitos, não logo final.
- **Os cinco primeiros pontos de contato**: o perfil do Instagram ou a página
  inicial, a tela de cadastro, a confirmação de pagamento do Pix, o primeiro post,
  a resposta à primeira reclamação.

## Regras

- Nunca copie nome, logo, cores ou slogan de concorrente.
- Nenhuma fonte, imagem ou ícone que o usuário não tenha direito de usar.
- Não é aconselhamento jurídico sobre marcas.

## Saída

`fundador/marca.md`. Próximo: `/fundador-operacoes` e `/fundador-lancamento`.
