# founder-skill-br

**Doze skills do Claude que testam um negócio no Brasil antes de você gastar
dinheiro nele.** Em português, em reais, com as regras daqui: MEI, Simples
Nacional, Pix, CDC, LGPD e INPI. Grátis, MIT, sem cadastro, sem chave de API.

Versão brasileira do [founder-skill](https://github.com/Jakeschincariol/founder-skill),
de Jake Schincariol.

Uma das skills é o seu conselho de administração, que aplica os frameworks de
*$100M Offers*, *De Zero a Um* e da biografia de Steve Jobs. Outra é o seu CFO, que
acha a margem real **depois do imposto e da taxa do Pix**. E outra é o painel de
consumidores: cria 100 compradores simulados a partir do seu cliente-alvo, com
renda mensal, jeito de comprar e objeções de brasileiro, e mostra quem compraria,
quem não compraria e por quê.

## Por que uma versão brasileira

O original é ótimo, mas pensado para os EUA: dólar, renda anual, USPTO, "sales tax".
Rodando no Brasil, ele erra justamente onde dói:

- **Esquece o imposto.** Um SaaS não pode ser MEI. Sem pró-labore, ele cai no
  Simples Anexo V, a 15,5% da receita. No exemplo abaixo, o imposto por assinante é **5 vezes**
  o custo de infraestrutura.
- **Não conhece o Pix**, nem o direito de arrependimento de 7 dias do CDC, nem a LGPD.
- **Não tem modo assinatura**, então não calcula churn, LTV nem quanto você pode
  pagar por cliente.
- **Diz "lucrativo" sem perguntar se você vive disso.** Aqui o CFO calcula quantos
  clientes você precisa para a sua meta de renda, comparando pró-labore e
  distribuição de lucros pelo Fator R.

## Instalar

No Claude Code:

```
/plugin marketplace add Cuerci/founder-skill-br
/plugin install founder-skill-br@founder-skill-br
```

Instaladas como plugin, as skills aparecem como `/founder-skill-br:fundador-cfo` e
assim por diante. Para usar só `/fundador-cfo`, copie as pastas:

```bash
git clone https://github.com/Cuerci/founder-skill-br.git
cp -r founder-skill-br/skills/fundador-* ~/.claude/skills/
```

Para valer só num projeto, copie as mesmas pastas para `.claude/skills/` dentro
dele. As ferramentas precisam de Python 3.9 ou mais novo e não instalam nada.

## As doze

| comando | papel | o que faz |
| --- | --- | --- |
| `/fundador-brasil` | Pesquisador de mercado | Monta o dossiê do mercado no Brasil com fonte e data em cada fato, e mantém as regras do país (MEI, Simples, Pix, CDC, LGPD, INPI). **Nova nesta versão.** |
| `/fundador-conselho` | Conselho | Três conselheiros, cada um um subagente com uma lente (Oferta, Monopólio, Produto), dão nota, apontam o que mataria o negócio e votam. |
| `/fundador-concorrentes` | Batedor de concorrência | Mapeia concorrentes diretos, indiretos e substitutos, com preço em reais e reclamações do Reclame Aqui, da Google Play BR e do Google Maps, tudo com link. |
| `/fundador-consumidor` | Painel de consumidores | 100 compradores simulados (20 com `--quick`), cada um com renda mensal, hábitos e objeção, apurados em quem compra e por quê. |
| `/fundador-preco` | Estrategista de preço | Faixa de preço Van Westendorp a partir do painel ou de um **Google Forms com clientes reais**, comparada com a concorrência e a margem. |
| `/fundador-oferta` | Arquiteto da oferta | Pilha de bônus, garantia que cabe no bolso, urgência real e nome, testada de novo no painel. |
| `/fundador-cfo` | CFO | Margem, equilíbrio, ano 1 mês a mês, caixa necessário e cenários. Três modos: por dia, por mês (venda única) e assinatura (churn, LTV, LTV/CAC). |
| `/fundador-marketing` | Diretor de marketing | Posicionamento, canais brasileiros (Instagram, WhatsApp, TikTok, Google Maps), campanha de 30 dias e dez ganchos. |
| `/fundador-marca` | Designer de marca | Nomes com as checagens de INPI, Registro.br e arroba, voz, slogan e briefing visual. |
| `/fundador-operacoes` | Gerente de operações | Fornecedores, rotinas, CNPJ e CNAE, alvará, NFS-e, LGPD e registro de riscos. |
| `/fundador-lancamento` | Líder de lançamento | Um teste real barato primeiro (pré-venda no Pix, membro fundador), depois contagem regressiva e os primeiros 30 dias. |
| `/fundador-plano` | Planejador | Junta tudo num plano de negócio com veredito **calculado**: Lucrativo, Ainda não ou Incompleto. |

## Como usar

Rode nesta ordem. Cada skill lê o que as anteriores escreveram na pasta
`fundador/` do seu projeto:

```
brasil -> conselho -> concorrentes -> consumidor -> preco -> oferta -> cfo -> marketing -> marca -> operacoes -> lancamento -> plano
```

Ou rode qualquer uma sozinha. `/fundador-consumidor --quick` numa ideia que você
ainda está pensando é um bom jeito de descobrir se vale continuar.

Use **uma pasta por ideia**: cada ideia tem o seu próprio `fundador/`.

## Um exemplo

`skills/fundador-cfo/exemplo-assinatura.json` descreve um SaaS de R$ 49,90 por mês.
O CFO devolve:

| linha | por assinante-mês |
| --- | ---: |
| Preço | R$ 49,90 |
| Infraestrutura por assinante | -R$ 1,50 |
| Taxa do Pix (Mercado Pago) (0,99% do preço) | -R$ 0,49 |
| Simples Nacional, Anexo V (alíquota efetiva do mês 12: 15,5%) | -R$ 7,73 |
| **Margem de contribuição** | **R$ 40,17** (80,5%) |

- Ponto de equilíbrio: 15 assinantes ativos.
- Churn de 8% por mês: o assinante fica em média 12,5 meses; LTV de R$ 502,14.
- Para pagar a aquisição com folga, gaste no máximo R$ 167,38 por assinante.

E a pergunta que importa, **quantos assinantes para eu tirar R$ 5.000 por mês?**

| jeito de tirar o dinheiro | assinantes ativos | pró-labore | lucro distribuído | anexo | Simples por mês |
| --- | ---: | ---: | ---: | :---: | ---: |
| Tudo em pró-labore | **138** | R$ 5.618 | R$ 10 | III (6%) | R$ 413 |
| Pró-labore no Fator R + lucros | **131** | R$ 1.830 | R$ 3.483 | III (6%) | R$ 392 |
| Só lucros distribuídos | **139** | R$ 0 | R$ 5.014 | V (15,5%) | R$ 1.075 |

Quinze assinantes pagam o servidor. Para o fundador viver do produto, são 131.

Também há exemplos de cafeteria (`exemplo.json`, modo dia) e de curso online
(`exemplo-venda-unica.json`, modo mês).

### O pacote inteiro, de ponta a ponta

Em [`exemplos/agenda-manicure`](exemplos/agenda-manicure/) o pacote roda do começo
ao fim numa ideia fictícia: uma agenda com lembrete no WhatsApp para manicures, a
R$ 29,90. Pesquisa real, 3 conselheiros, 20 compradoras simuladas, preço, oferta,
CFO, marketing, marca, operação, lançamento e o plano compilado.

O veredito foi **Ainda não**: só 15% das compradoras compram. Mas o painel mostrou
que 3 de 4 manicures que sofrem com falta compram, e pedem sinal no Pix. O pacote
transformou "mais uma agenda" em "agenda sem furo a R$ 39,90". É esse tipo de
virada que ele existe para achar antes de você gastar.

## As ferramentas

Cinco scripts, só com a biblioteca padrão do Python. Nenhum acessa a rede.

```bash
python3 skills/fundador-cfo/economia_unitaria.py fundador/numeros.json --out fundador/cfo.md
python3 skills/fundador-consumidor/painel.py init --cliente fundador/cliente.json --pitch fundador/pitch.md
python3 skills/fundador-preco/van_westendorp.py respostas.csv --preco 50
python3 skills/fundador-plano/compilar.py --dir fundador
python3 skills/fundador-cfo/simples.py 15000 --anexo V                                   # alíquota efetiva do Simples
```

Testes:

```bash
python3 -m unittest discover -s tests -v
```

## O que muda em relação ao original

- Tudo em português do Brasil; valores em `R$ 1.234,56`; renda **mensal**.
- `fundador-brasil` (nova): dossiê de mercado com fontes e `regras-br.md` com MEI,
  Simples e Fator R, taxas do Pix, CDC, CONAR, LGPD, INPI e Registro.br.
- CFO: **Simples Nacional calculado** (Anexos III e V, RBT12 proporcional do início
  de atividade, Fator R mês a mês), **meta de renda do fundador** com três
  estratégias de pró-labore e lucros, modo **assinatura** (churn, LTV, custo de
  aquisição, LTV/CAC), modo **mês** para venda única, taxas como **percentual** que
  acompanham o preço nos cenários, e o cenário "churn +50%".
- Plano: o veredito também checa se o plano chega à meta de renda do fundador.
- Preço: lê CSV exportado do Google Forms ou do Excel brasileiro (ponto e vírgula,
  "R$ 49,90").
- Painel: compradores com nomes brasileiros, renda mensal e respostas em português.
- Marca, operação, lançamento e oferta: INPI no lugar do USPTO, CNPJ e alvará no
  lugar dos permits americanos, o arrependimento de 7 dias do CDC na garantia.

## Letras miúdas

**O conselho aplica frameworks publicados. Não é essas pessoas.** As três lentes
são resumos, com nossas palavras, de ideias de *$100M Offers* (Alex Hormozi), *De
Zero a Um* (Peter Thiel com Blake Masters) e da biografia de Steve Jobs por Walter
Isaacson. O conselho nunca fala como eles nem diz que aprovariam algo. Este projeto
não tem relação com nenhum deles.

**O painel é de compradores simulados, não de clientes.** Serve para achar
objeções, segmentos e palavras rápido e barato. Não é previsão: modelos de
linguagem tendem a concordar, então leia a taxa de compra como teto e confirme as
grandes decisões com gente de verdade. Nunca use respostas do painel como depoimento.

**Os números valem o que valem as entradas.** O CFO marca toda estimativa como
estimativa e pede orçamentos reais. As regras de `regras-br.md` têm fonte e data,
mas mudam: confira antes de decidir.

**Não é aconselhamento financeiro, jurídico nem tributário.** Um contador confirma
o regime e o imposto; um advogado confirma marca, LGPD e contratos.

## Créditos

Baseado no [founder-skill](https://github.com/Jakeschincariol/founder-skill), de
Jake Schincariol ([opusjake.ai](https://opusjake.ai)), sob licença MIT. Os 11
papéis, as lentes, o painel e o veredito calculado são dele; a adaptação para o
Brasil e as ferramentas novas são deste repositório. Veja `CREDITOS.md`.

## Licença

MIT. Pegue, mude, publique.
