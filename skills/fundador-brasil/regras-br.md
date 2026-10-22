# Regras e referências do Brasil

Base compartilhada pelas skills `fundador-*`. Cada fato tem fonte e data de
verificação. Tarifas, alíquotas e leis mudam: antes de usar um número num cálculo
que vai decidir dinheiro, confira a fonte oficial e atualize a data aqui.

Última verificação geral: 2026-10-21.

## Moeda, formato e idioma

- Valores em reais: `R$ 1.234,56`. Renda de pessoa física se fala **por mês**, não
  por ano (salário mensal, renda familiar mensal).
- Texto em português do Brasil, com o vocabulário do cliente: cada nicho tem as
  suas gírias e termos técnicos; o dossiê de mercado deve registrá-los.

## Empresa e impostos

| tema | o que vale | fonte |
| --- | --- | --- |
| MEI e software | Desenvolver ou vender software/SaaS **não** é atividade permitida ao MEI em 2026. O PLP 25/2026, que incluiria programadores no MEI, passou numa comissão da Câmara em 30/06/2026 e ainda tramita. | [contabilidade.com](https://contabilidade.com/blog/desenvolvedor-pode-ser-mei-em-2026-veja-como-abrir-seu-cnpj-corretamente-e-pagar-menos-impostos/), [Fenacon](https://fenacon.org.br/noticias/comissao-aprova-inclusao-de-programadores-e-desenvolvedores-de-software-no-mei/) |
| SaaS no Simples | Assinatura de software é tributada no Anexo III ou V conforme o Fator R (folha de 12 meses ÷ receita de 12 meses). Fator R ≥ 28%: Anexo III, a partir de **6%**. Abaixo: Anexo V, a partir de **15,5%**. Pró-labore conta como folha. Nos Anexos III e V, o INSS patronal (CPP) já está no DAS; o sócio paga 11% sobre o pró-labore. | [Agilize](https://agilize.com.br/artigos/?p=4180), [Tributo Devido](https://tributodevido.com.br/portal/tributacao-no-simples-nacional-para-licenciamento-e-assinatura-de-software/) |
| Caminho comum | ME (até R$ 360 mil/ano) no Simples, CNAE 6203-1/00 ou similar. Confirmar com contador. | [contabilidade.com](https://contabilidade.com/blog/desenvolvedor-pode-ser-mei-em-2026-veja-como-abrir-seu-cnpj-corretamente-e-pagar-menos-impostos/) |
| MEI em geral | Limite de R$ 81 mil por ano; só atividades da lista oficial do MEI. Confira a ocupação antes de abrir. | [Portal do Empreendedor](https://www.gov.br/empresas-e-negocios/pt-br/empreendedor) |

### Tabelas dos Anexos III e V

LC 123/2006, redação da LC 155/2016, sem mudança até 2026. Alíquota efetiva =
(RBT12 × nominal − parcela a deduzir) ÷ RBT12. ([Agilize](https://agilize.com.br/artigos/?p=498), [contabilidade.com](https://contabilidade.com/blog/anexos-do-simples-nacional-2026-tabela-completa-por-atividade/))

| receita em 12 meses | Anexo III | deduzir | Anexo V | deduzir |
| --- | ---: | ---: | ---: | ---: |
| até R$ 180 mil | 6% | 0 | 15,5% | 0 |
| até R$ 360 mil | 11,2% | 9.360 | 18% | 4.500 |
| até R$ 720 mil | 13,5% | 17.640 | 19,5% | 9.900 |
| até R$ 1,8 milhão | 16% | 35.640 | 20,5% | 17.100 |
| até R$ 3,6 milhões | 21% | 125.640 | 23% | 62.100 |
| até R$ 4,8 milhões | 33% | 648.000 | 30,5% | 540.000 |

As faixas 4 a 6 do Anexo V vêm da lei; não as achei repetidas numa fonte secundária
nesta verificação.

**Início de atividade:** no 1º mês, a RBT12 é a receita do mês × 12; do 2º ao 12º, a
média dos meses anteriores × 12. O Fator R segue a mesma proporção. ([Contábeis](https://www.contabeis.com.br/forum/tributos-federais/319914/simples-nacional-inicio-de-atividade/))

No CFO, use `"simples": {"anexo": "fator_r"}` (ou `"III"`, `"V"`) e o imposto é
calculado mês a mês, com `prolabore_mensal` entrando no Fator R. Outros anexos
(comércio, indústria) ainda vão como `percentual` em `variavel`.

### "Vender como curso" para cair no Anexo III

Tem gente que fatura um SaaS como "treinamento", "mentoria" ou "curso" para pagar
6% sem pró-labore. O que vale:

- **Curso de verdade pode ser Anexo III direto**, sem Fator R, quando é ensino em
  formato de curso ou escola livre (turma, conteúdo padronizado). Um curso gravado
  vendido de fato, com receita separada, é um caso legítimo.
- **Treinamento personalizado ou mentoria sob demanda é atividade intelectual**, e
  segue o Fator R (Anexo III ou V). Solução de Consulta Cosit nº 166/2026. ([Rota da Jurisprudência](https://rotadajurisprudencia.com.br/wp-content/uploads/2026/09/SC-Cosit-ny-166-2026.pdf), [Ozai](https://www.ozai.com.br/?p=25750))
- **Assinatura de software é licenciamento** e segue o Fator R. A Receita olha o
  que é prestado de fato, não o nome na nota nem o CNAE escolhido. ([Tributo Devido](https://tributodevido.com.br/portal/tributacao-no-simples-nacional-para-licenciamento-e-assinatura-de-software/), [Agilize](https://agilize.com.br/artigos/?p=4180))
- **Risco:** se a fiscalização reclassificar, cobra a diferença com juros e multa de
  ofício de 75%, que pode ir a 150% se houver fraude (Lei 9.430/1996, art. 44), e
  pode excluir a empresa do Simples. A Receita cruza dados de notas e de pagamento.

O caminho legal para o SaaS chegar ao Anexo III é o Fator R: um pró-labore de pelo
menos 28% da receita. A seção "Para viver disso" do CFO mostra que isso costuma
custar menos clientes do que pagar o Anexo V.

## Meios de pagamento

| meio | taxa | fonte |
| --- | --- | --- |
| Pix no Mercado Pago, checkout online ou link de pagamento | **0,99%**, recebimento na hora | [Mercado Pago](https://www.mercadopago.com.br/blog/quanto-custa-receber-pagamentos-via-pix-e-codigo-qr), [Mercado Pago, checkout](https://www.mercadopago.com.br/blog/opcoes-checkout-plataformas-ecommerce) |
| Pix por QR na maquininha | 0,49% (0% em perfil promocional) | idem |
| Cartão no Mercado Pago (agregador) | débito ~0,89%, crédito à vista ~2,82% | [Calculadora de Taxas](https://www.calculadoradetaxas.com.br/mercado-pago/taxas) (não oficial) |

As páginas do Mercado Pago misturam condições promocionais e padrão. Confirme a
taxa no painel da conta antes de fechar o preço.

## Consumidor e publicidade

- **Direito de arrependimento (CDC, art. 49):** compra fora do estabelecimento
  (internet) pode ser cancelada em 7 dias corridos, com devolução integral e
  imediata. Planeje o reembolso no fluxo de pagamento; uma "garantia de 7 dias"
  não é bônus, é lei. [Advbox](https://advbox.com.br/blog/legislacao-direito-de-arrependimento/)
- **Publicidade:** sem depoimento inventado, sem antes/depois falso, sem urgência
  falsa. Siga o Código do CONAR e o CDC (publicidade enganosa, art. 37).
- **Renovação:** assinatura com renovação automática precisa estar clara antes do
  pagamento e ser fácil de cancelar.

## Dados pessoais (LGPD)

- Foto de pessoa é dado pessoal; foto que revela saúde da pele pode ser lida como
  dado sensível. Peça consentimento específico e registrado para publicar a foto do
  cliente, permita revogar e apagar.
- Tenha política de privacidade, um contato do encarregado e o registro de onde os
  dados ficam (servidor, provedores como Cloudflare ou Anthropic).

## Marca e presença

| item | onde | custo e prazo | fonte |
| --- | --- | --- | --- |
| Marca | [INPI, busca de marcas](https://busca.inpi.gov.br/pePI/) | R$ 440 por classe para ME/pessoa física com especificação pré-aprovada (R$ 880 sem desconto); pagamento único desde 09/2025 cobre 10 anos. Análise sem oposição: ~18,5 meses em 2025, meta de 10 meses em 2026. | [Contajá](https://contaja.com.br/blog/quanto-custa-registrar-uma-marca/), [Fenacon](https://fenacon.org.br/noticias/pequenos-negocios-podem-economizar-ate-60-para-registrar-marca-no-inpi/) |
| Classes de Nice para SaaS | 42 (software como serviço), 9 (app baixável), 41 ou 35 se houver conteúdo/marketing | | |
| Domínio | [Registro.br](https://registro.br) para `.com.br` | | |
| Arroba | Instagram, TikTok, YouTube, WhatsApp Business | | |

## Onde pesquisar no Brasil

- Reclamações: [Reclame Aqui](https://www.reclameaqui.com.br), avaliações da Google
  Play e da App Store **Brasil**, Google Maps, grupos de Facebook e comentários no
  Instagram e no TikTok.
- Dados de empresas: [Data Sebrae](https://datasebrae.com.br), [Portal do
  Empreendedor / dados do MEI](https://www.gov.br/empresas-e-negocios/pt-br/empreendedor),
  [IBGE](https://www.ibge.gov.br), CNAE em [CONCLA](https://concla.ibge.gov.br).
- Licenças: prefeitura e vigilância sanitária do município; regras mudam de cidade
  para cidade.

Isso não é aconselhamento jurídico, contábil nem tributário. Um contador confirma o
enquadramento; um advogado confirma marca, LGPD e contratos.
