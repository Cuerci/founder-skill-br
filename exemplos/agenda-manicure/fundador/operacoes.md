# Operação: Unhas em Dia

`/fundador-operacoes`. Negócio online, fundador solo.

## O ciclo do dia

Cadastros novos → agendamentos chegam pelo link → **lembretes da véspera saem às
18h** (cliente vê) → respostas de confirmar ou desmarcar atualizam a agenda (cliente
vê) → sinais no Pix confirmados (cliente vê) → lista de espera avisada → suporte no
WhatsApp → monitoramento da fila de mensagens → backup noturno.

## Fornecedores

| item | opções | preço | observação |
| --- | --- | --- | --- |
| Mensagens | API oficial do WhatsApp (Meta Cloud API), ou um provedor (BSP) | ~R$ 0,035 por mensagem de utilidade | provedores somam taxa própria; confirmar na tabela da Meta |
| Sinal no Pix | Mercado Pago, Efí, Asaas | Pix no checkout ~0,99% no Mercado Pago | o sinal cai na conta da **manicure** (subconta ou chave dela), não na da empresa |
| Servidor | VPS nacional ou internacional | ~R$ 100/mês (estimativa) | |

## Pessoas

Só o fundador. Suporte das 9h às 19h no WhatsApp; as 18h, hora dos lembretes, são o
pico. Com 300 assinantes, avaliar um atendente meio período (encargos: contador).

## Rotinas

1. **Lembrete não saiu:** alerta automático se a fila atrasar 15 min; reenvio manual; avisar as manicures afetadas.
2. **Reembolso em 7 dias (CDC):** devolução integral no mesmo meio, em até 2 dias úteis.
3. **Exclusão de dados (LGPD):** pedido da manicure apaga ela e as clientes dela; pedido de uma cliente final vai para a manicure, que é a controladora.
4. **Reclamação:** resposta em até 4 h úteis; se for falha do app, um mês grátis.
5. **Revisão semanal:** faltas evitadas, churn, CAC, custo de mensagens por assinante.

## Ferramentas

WhatsApp Business no número de suporte, emissor de NFS-e da prefeitura, contador
online, gateway de pagamento da assinatura com renovação automática e cancelamento
de um clique.

## Empresa e licenças

- **ME no Simples**, CNAE de SaaS (ex.: 6311-9/00 ou 6203-1/00, o contador define). SaaS não pode ser MEI.
- NFS-e e ISS do município.
- **LGPD:** termos de uso, política de privacidade e contrato de operador com a manicure (ela é a controladora dos dados das clientes).
- Política comercial da Meta para a API do WhatsApp: modelos de mensagem aprovados.

## Riscos

| risco | chance | gravidade | plano |
| --- | --- | --- | --- |
| Meta reprova ou muda o preço do modelo de lembrete | média | alta | dois modelos aprovados; preço com folga |
| Número de envio bloqueado por denúncia de spam | média | alta | só manda para quem agendou; botão de sair |
| Cliente responde "desmarcar" e a manicure não vê | média | alta | a resposta atualiza a agenda e notifica a manicure |
| Sinal no Pix cai na conta errada | baixa | alta | sinal direto na chave da manicure |
| Fundador doente na semana de lançamento | média | média | lembretes automáticos não dependem dele; aviso de suporte reduzido |
| Concorrente lança lembrete no WhatsApp | alta | média | foco em sinal + lista de espera + nicho |
| Vazamento de dados de clientes | baixa | alta | criptografia, backup, plano de comunicação à ANPD |
