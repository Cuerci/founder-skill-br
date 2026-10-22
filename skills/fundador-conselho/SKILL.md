---
name: fundador-conselho
description: >-
  Seu conselho de administração. Coloca uma ideia de negócio diante de três
  conselheiros, cada um um subagente que lê a ideia por um framework publicado: a
  lente da Oferta (do livro $100M Offers, de Alex Hormozi), a lente do Monopólio
  (De Zero a Um, de Peter Thiel) e a lente do Produto (a biografia de Steve Jobs
  por Walter Isaacson), aplicadas ao contexto brasileiro. Cada um dá nota, aponta
  os riscos que matariam o negócio e vota: investe, investe se, ou passa. Use
  quando o usuário disser "testa minha ideia", "isso funciona?", "estressa essa
  ideia", "o que um conselho diria", "é um bom negócio?", ou ao começar o pacote
  fundador numa ideia nova.
argument-hint: "<a ideia de negócio, ou vazio para usar a conversa>"
---

# fundador-conselho

A primeira reunião. Antes de alguém montar site ou assinar contrato, três
conselheiros desmontam a ideia, cada um por um ângulo, e votam.

O que o usuário digitou depois de `/fundador-conselho`: `$ARGUMENTS`. Se estiver
vazio, pegue a ideia da conversa.

## A regra sobre os três nomes

As lentes são resumos de **frameworks publicados**, nada mais. Os conselheiros não
são essas pessoas, nunca falam como elas, nunca as citam, nunca dizem que elas
aprovariam algo. Escreva "a lente da Oferta", nunca "o Hormozi diz". Se o usuário
perguntar o que um deles realmente acha, diga que só dá para aplicar os frameworks
públicos.

## Passo 0: o contexto brasileiro e o arquivo da ideia

Leia `${CLAUDE_SKILL_DIR}/../fundador-brasil/regras-br.md` e, se existir,
`fundador/mercado.md`. Se o dossiê não existir, sugira `/fundador-brasil` antes ou
logo depois; o conselho funciona sem ele, mas com menos fatos.

Todo o pacote lê `fundador/ideia.md` no projeto. Se não existir, escreva agora a
partir da conversa:

```markdown
# <nome do negócio, ou um nome provisório>

- O que é: uma frase.
- Para quem: o cliente-alvo, o mais específico que o usuário conseguir.
- O que vende, a que preço: o produto principal e o preço em reais.
- Onde e como: cidade ou online, como o cliente encontra, como é entregue, como paga.
- Orçamento e restrições: dinheiro, tempo, habilidades, o que já foi decidido.
```

Se faltar o nome, o cliente, o produto ou o preço, pergunte (no máximo três
perguntas numa mensagem) e depois escreva o arquivo. Não invente orçamento, tamanho
de mercado nem concorrente.

## Passo 1: o briefing do conselho

Escreva `fundador/conselho/briefing.md`: o arquivo da ideia, mais o que o usuário
disse que um estranho precisaria saber, mais o resumo de `fundador/mercado.md` e as
regras de `regras-br.md` que pesam neste negócio (por exemplo: SaaS não pode ser
MEI; Pix custa 0,99% no checkout). **Subagentes não veem esta conversa**, então o
briefing precisa se sustentar sozinho. Não ponha a sua opinião sobre a ideia nele.

## Passo 2: a reunião

Lance três subagentes numa ÚNICA mensagem (ferramenta Agent, `subagent_type:
general-purpose`, um por conselheiro), cada um instruído: `Leia
fundador/conselho/briefing.md e o lentes.md do fundador-conselho (caminho abaixo),
aplique SOMENTE a lente <lente>, pense no mercado brasileiro e escreva seu parecer
em português em fundador/conselho/<lente>.md.` O arquivo das lentes é
`${CLAUDE_SKILL_DIR}/lentes.md` (se o caminho não expandir, use o diretório base
que o Claude Code mostrou para esta skill).

Cada parecer, neste formato:

```markdown
# Lente <nome>
Nota: <1-10> | Voto: INVESTE / INVESTE SE / PASSA
## O que é forte
## O que mataria o negócio (os 3 principais, o mais perigoso primeiro)
## As perguntas que eu faria ao fundador
## Se INVESTE SE: as condições
```

## Passo 3: o resumo do presidente

Leia os três pareceres (são curtos) e escreva `fundador/conselho.md`:

1. O voto, por exemplo "2 investe se, 1 passa", e a nota média.
2. Os riscos levantados por mais de um conselheiro: esses vêm primeiro.
3. Todas as condições, juntas, como checklist que o resto do pacote pode ir
   marcando (o CFO, o painel de compradores e o preço vão testar a maioria).
4. Um parágrafo: a versão mais forte deste negócio que o conselho enxerga. Pode ser
   diferente do que o usuário propôs; diga isso com clareza.

Mantenha as discordâncias. Conselho que concorda em tudo não fez o trabalho.

## Regras

- Avalie o negócio, não o fundador.
- Nenhum fato inventado. Se uma lente precisa de um número que ninguém tem ainda
  (tamanho do mercado, custo de aquisição), registre como pergunta aberta e diga
  qual skill responde (`/fundador-brasil`, `/fundador-concorrentes`,
  `/fundador-consumidor`, `/fundador-cfo`).
- PASSA é um resultado, não um fracasso. Diga com clareza.

## Saída

`fundador/ideia.md`, `fundador/conselho/` (briefing e três pareceres),
`fundador/conselho.md`. Depois diga o voto numa linha e sugira o próximo passo:
`/fundador-concorrentes` para ver quem já está lá, ou `/fundador-consumidor` para
pôr a ideia diante de compradores simulados.

## A ordem do pacote

```
brasil -> conselho -> concorrentes -> consumidor -> preco -> oferta -> cfo -> marketing -> marca -> operacoes -> lancamento -> plano
```

Toda skill também roda sozinha; cada uma lê o que já estiver em `fundador/`.
