#!/usr/bin/env python3
"""Economia unitária para o fundador-cfo. Só biblioteca padrão, sem rede.

Versão brasileira do unit_economics.py do founder-skill (MIT, Jake Schincariol).
Lê um JSON com os números do negócio e mostra o que um CFO confere antes de gastar
um real: quanto uma unidade deixa, a margem real no volume planejado, o ponto de
equilíbrio, o ano 1 mês a mês e em quanto tempo o investimento inicial volta.

    python3 economia_unitaria.py fundador/numeros.json
    python3 economia_unitaria.py fundador/numeros.json --out fundador/cfo.md
    python3 economia_unitaria.py fundador/numeros.json --json
    python3 economia_unitaria.py fundador/numeros.json --preco 59.90 --volume 0.8

Campos (veja exemplo.json e exemplo-assinatura.json nesta pasta):

    negocio             nome, para o relatório
    unidade             o que se vende: "copo", "pedido", "assinante-mês"
    preco               preço por unidade, em reais
    variavel            [{item, custo}] ou [{item, percentual}]: custo de UMA unidade.
                        "percentual" é sobre o preço (0.0099 = 0,99%): taxa do Pix,
                        do cartão, imposto do Simples. Acompanha o preço nos cenários.
    fixo_mensal         [{item, custo}] o que se paga todo mês: servidor, aluguel, pró-labore
    inicial             [{item, custo}] gasto único antes de abrir

  Modo "dia" (padrão; loja, café, serviço):
    dias_por_mes        dias de venda no mês (padrão 30)
    capacidade_por_dia  o máximo de unidades por dia (opcional)
    plano_por_dia       o volume depois que o negócio pegar
    rampa_por_dia       12 números: unidades por dia em cada mês do ano 1 (opcional)

  Modo "mes" (venda única contada por mês: curso, e-book, template, app pago uma vez,
  projeto): "modelo": "mes"
    plano_por_mes       vendas por mês depois que o negócio pegar
    rampa_por_mes       12 números: vendas em cada mês do ano 1 (opcional)
    capacidade_por_mes  o máximo de vendas por mês (opcional)

  Modo "assinatura" (SaaS, clube, mensalidade): "modelo": "assinatura"
    novos_por_mes       12 números: assinantes novos em cada mês do ano 1
    churn_mensal        fração da base que cancela ou não renova por mês (0.06 = 6%)
    assinantes_iniciais base no início do mês 1 (padrão 0)
    capacidade_assinantes  o máximo que a operação aguenta (opcional)
    custo_aquisicao     quanto custa conquistar um assinante novo (anúncio, comissão,
                        brinde); entra como gasto no mês em que ele chega (opcional)

  Em venda única, o custo de aquisição por venda vai em "variavel".

Todo número do relatório vem desse arquivo. Nada é buscado nem chutado. Se faltar
um campo, a ferramenta avisa em vez de preencher.

--preco e --volume rodam um cenário sem editar o arquivo: --preco troca o preço,
--volume multiplica todo volume (0.8 = 20 por cento menos vendas ou assinantes novos).
"""

import argparse
import json
import math
import sys


class NumbersError(Exception):
    pass


def _br(v, casas):
    s = "{:,.{c}f}".format(abs(v), c=casas)
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def _money(v):
    return "%sR$ %s" % ("-" if v < 0 else "", _br(v, 2))


def _whole(v):
    return "%sR$ %s" % ("-" if round(v) < 0 else "", _br(round(v), 0))


def _num(v):
    return _br(v, 0)


def _pct(v):
    t = "%.2f" % (v * 100)
    t = t.rstrip("0").rstrip(".") if "." in t and abs(v * 100) < 10 else "%.1f" % (v * 100)
    return t.replace(".", ",") + "%"


def _item_cost(it, field, i, price):
    if not isinstance(it, dict) or ("custo" not in it and "percentual" not in it):
        raise NumbersError("%s[%d] precisa de 'custo' (ou 'percentual' em variavel)" % (field, i))
    key = "custo" if "custo" in it else "percentual"
    if key == "percentual" and field != "variavel":
        raise NumbersError("%s[%d]: 'percentual' só vale em variavel" % (field, i))
    try:
        v = float(it[key])
    except (TypeError, ValueError):
        raise NumbersError("%s[%d].%s não é número: %r" % (field, i, key, it[key]))
    return v * price if key == "percentual" else v


def _sum(items, field, price=0.0):
    return sum(_item_cost(it, field, i, price) for i, it in enumerate(items or []))


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise NumbersError("arquivo não existe: %s" % path)
    except json.JSONDecodeError as e:
        raise NumbersError("%s não é JSON válido: %s" % (path, e))


def _twelve(spec, key):
    v = spec.get(key)
    if v is None:
        return None
    if len(v) != 12:
        raise NumbersError("'%s' precisa de 12 números, um por mês (veio %d)" % (key, len(v)))
    return [float(x) for x in v]


def analyse(spec, price=None, volume=1.0):
    """Devolve um dict com todos os números do relatório. Função pura, fácil de testar."""
    if "preco" not in spec and price is None:
        raise NumbersError("falta 'preco'")
    p = float(price if price is not None else spec["preco"])
    if p <= 0:
        raise NumbersError("o preço precisa ser maior que zero")
    mode = spec.get("modelo", "dia")
    if mode not in ("dia", "mes", "assinatura"):
        raise NumbersError("'modelo' é 'dia', 'mes' ou 'assinatura' (veio %r)" % mode)
    var = _sum(spec.get("variavel"), "variavel", p)
    fixed = _sum(spec.get("fixo_mensal"), "fixo_mensal")
    startup = _sum(spec.get("inicial"), "inicial")
    contribution = p - var

    churn = None
    cac = 0.0
    new_by_month = [0.0] * 12
    if mode == "mes":
        if "plano_por_mes" not in spec and "rampa_por_mes" not in spec:
            raise NumbersError("informe 'plano_por_mes' ou 'rampa_por_mes' (12 números)")
        plan = float(spec.get("plano_por_mes", 0)) * volume
        ramp = _twelve(spec, "rampa_por_mes")
        ramp = [plan] * 12 if ramp is None else [v * volume for v in ramp]
        if not plan:
            plan = ramp[-1]
        units_by_month = level_by_month = ramp
        plan_units_month = plan
        breakeven = math.inf if contribution <= 0 else fixed / contribution
        capacity = spec.get("capacidade_por_mes")
        period = "mês"
    elif mode == "dia":
        days = float(spec.get("dias_por_mes", 30))
        if "plano_por_dia" not in spec and "rampa_por_dia" not in spec:
            raise NumbersError("informe 'plano_por_dia' ou 'rampa_por_dia' (12 números)")
        plan = float(spec.get("plano_por_dia", 0)) * volume
        ramp = _twelve(spec, "rampa_por_dia")
        ramp = [plan] * 12 if ramp is None else [v * volume for v in ramp]
        if not plan:
            plan = ramp[-1]
        units_by_month = [d * days for d in ramp]
        level_by_month = ramp
        plan_units_month = plan * days
        breakeven = math.inf if contribution <= 0 else fixed / (contribution * days)
        capacity = spec.get("capacidade_por_dia")
        period = "dia"
    else:
        new = _twelve(spec, "novos_por_mes")
        if new is None:
            raise NumbersError("o modo assinatura precisa de 'novos_por_mes' (12 números)")
        if "churn_mensal" not in spec:
            raise NumbersError("o modo assinatura precisa de 'churn_mensal' (ex.: 0.06)")
        churn = float(spec["churn_mensal"])
        if not 0 <= churn < 1:
            raise NumbersError("'churn_mensal' fica entre 0 e 1 (veio %r)" % churn)
        cac = float(spec.get("custo_aquisicao", 0))
        if cac < 0:
            raise NumbersError("'custo_aquisicao' não pode ser negativo")
        active = float(spec.get("assinantes_iniciais", 0))
        units_by_month = []
        new_by_month = [n * volume for n in new]
        for n in new_by_month:
            active = active * (1 - churn) + n
            units_by_month.append(active)
        level_by_month = units_by_month
        plan = plan_units_month = units_by_month[-1]
        breakeven = math.inf if contribution <= 0 else fixed / contribution
        capacity = spec.get("capacidade_assinantes")
        period = "mês"

    margin_at_plan = (contribution - (fixed / plan_units_month if plan_units_month else math.inf)) / p

    months = []
    cumulative = -startup
    payback_month = None
    for m, (units, level, new_m) in enumerate(zip(units_by_month, level_by_month, new_by_month), start=1):
        revenue = units * p
        variable_cost = units * var
        acquisition = new_m * cac
        profit = revenue - variable_cost - fixed - acquisition
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append({"month": m, "level": level, "units": units, "revenue": revenue,
                       "variable": variable_cost, "fixed": fixed, "acquisition": acquisition, "profit": profit,
                       "cumulative": cumulative})
    year_profit = sum(m["profit"] for m in months)
    year_revenue = sum(m["revenue"] for m in months)
    # o caixa necessário: o inicial mais o buraco mais fundo que os meses de prejuízo cavam
    lowest = min([-startup] + [m["cumulative"] for m in months])
    cash_needed = -lowest

    ltv = None
    if churn:
        ltv = contribution / churn

    unit = spec.get("unidade", "unidade")
    ltv_cac = (ltv / cac) if (ltv is not None and cac) else None
    cac_payback = (cac / contribution) if (cac and contribution > 0) else None
    flags = []
    if contribution <= 0:
        flags.append("Cada %s dá prejuízo antes dos custos fixos: o preço está abaixo do custo variável." % unit)
    if capacity is not None and breakeven > float(capacity):
        flags.append("O ponto de equilíbrio pede %s por %s, mas a capacidade é %s." % (_num(breakeven), period, capacity))
    if capacity is not None and plan > float(capacity):
        flags.append("O plano (%s por %s) passa da capacidade (%s)." % (_num(plan), period, capacity))
    if year_profit < 0:
        flags.append("O ano 1 dá prejuízo operacional de %s." % _whole(-year_profit))
    if payback_month is None:
        flags.append("O investimento inicial não volta dentro do ano 1.")
    if ltv_cac is not None and ltv_cac < 3:
        flags.append("LTV/CAC de %s: abaixo de 3, a aquisição come a margem." % ("%.1f" % ltv_cac).replace(".", ","))

    return {
        "business": spec.get("negocio", ""), "unit": unit, "mode": mode, "period": period,
        "price": p, "variable_per_unit": var, "contribution": contribution,
        "contribution_pct": contribution / p, "fixed_monthly": fixed, "startup": startup,
        "plan": plan, "margin_at_plan": margin_at_plan, "breakeven": breakeven,
        "capacity": capacity, "churn": churn, "ltv": ltv, "cac_max": ltv / 3 if ltv else None,
        "cac": cac, "ltv_cac": ltv_cac, "cac_payback_months": cac_payback,
        "year1_revenue": year_revenue, "year1_profit": year_profit,
        "year1_after_startup": year_profit - startup, "payback_month": payback_month,
        "cash_needed": cash_needed, "months": months, "flags": flags,
        "variable_items": spec.get("variavel", []), "fixed_items": spec.get("fixo_mensal", []),
    }


def sensitivity(spec):
    """Os cenários que todo plano precisa aguentar."""
    base = analyse(spec)
    rows = [("Plano base", base)]
    rows.append(("Preço -10%", analyse(spec, price=base["price"] * 0.9)))
    rows.append(("Volume -20%", analyse(spec, volume=0.8)))
    worse = json.loads(json.dumps(spec))
    for it in worse.get("variavel", []):
        for k in ("custo", "percentual"):
            if k in it:
                it[k] = float(it[k]) * 1.15
    rows.append(("Custos unitários +15%", analyse(worse)))
    if base["mode"] == "assinatura":
        churny = dict(spec, churn_mensal=min(0.99, float(spec["churn_mensal"]) * 1.5))
        rows.append(("Churn +50%", analyse(churny)))
    return rows


def _be(v):
    return "nunca" if math.isinf(v) else _num(math.ceil(v))


def report(spec, a):
    u, per = a["unit"], a["period"]
    sub = a["mode"] == "assinatura"
    L = ["# Economia unitária: %s" % (a["business"] or "seu negócio"), "",
         "Todo número abaixo vem do arquivo de entrada. Nada foi buscado nem chutado.", "",
         "## Por %s" % u, "", "| linha | por %s |" % u, "| --- | ---: |",
         "| Preço | %s |" % _money(a["price"])]
    for it in a["variable_items"]:
        if "percentual" in it:
            label = "%s (%s do preço)" % (it.get("item", "custo"), _pct(float(it["percentual"])))
            cost = float(it["percentual"]) * a["price"]
        else:
            label, cost = it.get("item", "custo"), float(it["custo"])
        L.append("| %s | -%s |" % (label, _money(cost)))
    L.append("| **Margem de contribuição** (o que cada %s deixa para pagar os fixos) | **%s** (%s) |"
             % (u, _money(a["contribution"]), _pct(a["contribution_pct"])))
    L += ["", "## A margem que importa", ""]
    L.append("Custos fixos: %s por mês (%s)." % (_whole(a["fixed_monthly"]), ", ".join(
        "%s %s" % (it.get("item", "custo"), _whole(float(it["custo"]))) for it in a["fixed_items"]) or "nenhum informado"))
    L.append("")
    if sub:
        L.append("- **Ponto de equilíbrio: %s assinantes ativos.**" % _be(a["breakeven"]))
        L.append("- Margem de lucro com a base do mês 12 (%s assinantes): **%s**." % (_num(a["plan"]), _pct(a["margin_at_plan"])))
        L.append("- Churn de %s por mês: um assinante fica em média %s meses." % (
            _pct(a["churn"]), ("%.1f" % (1 / a["churn"])).replace(".", ",") if a["churn"] else "infinitos"))
        if a["ltv"] is not None:
            L.append("- **LTV** (margem de contribuição na vida do assinante): %s. Para pagar a aquisição com folga,"
                     " gaste no máximo **%s por assinante** (LTV/3, regra de bolso)." % (_money(a["ltv"]), _money(a["cac_max"])))
        if a["cac"]:
            L.append("- Custo de aquisição: %s por assinante novo. LTV/CAC: **%s**; a margem paga a aquisição em %s meses."
                     % (_money(a["cac"]), ("%.1f" % a["ltv_cac"]).replace(".", ",") if a["ltv_cac"] else "n/d",
                        ("%.1f" % a["cac_payback_months"]).replace(".", ",") if a["cac_payback_months"] else "nunca"))
        if a["capacity"] is not None:
            L.append("- Capacidade: %s assinantes." % a["capacity"])
    elif a["mode"] == "mes":
        L.append("- **Ponto de equilíbrio: %s vendas por mês (%s).**" % (_be(a["breakeven"]), u))
        L.append("- Margem de lucro no plano (%s por mês): **%s**." % (_num(a["plan"]), _pct(a["margin_at_plan"])))
        if a["capacity"] is not None:
            L.append("- Capacidade: %s por mês." % a["capacity"])
    else:
        L.append("- **Ponto de equilíbrio: %s por dia (%s).**" % (_be(a["breakeven"]), u))
        L.append("- Margem de lucro no plano (%s por dia): **%s**." % (_num(a["plan"]), _pct(a["margin_at_plan"])))
        if a["capacity"] is not None:
            L.append("- Capacidade: %s por dia." % a["capacity"])
    L += ["", "## Ano 1, mês a mês", ""]
    L.append("| mês | %s | receita | lucro | acumulado (após %s iniciais) |" % (
        "assinantes ativos" if sub else ("vendas no mês" if a["mode"] == "mes" else "por dia (%s)" % u), _whole(a["startup"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for m in a["months"]:
        L.append("| %d | %s | %s | %s | %s |" % (m["month"], _num(m["level"]), _whole(m["revenue"]),
                                             _whole(m["profit"]), _whole(m["cumulative"])))
    L += ["",
          "- **Lucro operacional do ano 1: %s** sobre %s de receita." % (_whole(a["year1_profit"]), _whole(a["year1_revenue"])),
          "- Depois dos %s iniciais: %s." % (_whole(a["startup"]), _whole(a["year1_after_startup"])),
          "- Investimento inicial recuperado: %s." % ("no mês %d" % a["payback_month"] if a["payback_month"] else "não dentro do ano 1"),
          "- Caixa necessário antes de se pagar: **%s**." % _whole(a["cash_needed"]),
          "", "## E se", "",
          "| cenário | margem no plano | equilíbrio (%s) | lucro do ano 1 |" % (
              "assinantes" if sub else ("por mês" if a["mode"] == "mes" else "por dia")),
          "| --- | ---: | ---: | ---: |"]
    for name, s in sensitivity(spec):
        L.append("| %s | %s | %s | %s |" % (name, _pct(s["margin_at_plan"]), _be(s["breakeven"]), _whole(s["year1_profit"])))
    L.append("")
    if a["flags"]:
        L += ["## Alertas", ""] + ["- %s" % f for f in a["flags"]]
    else:
        L.append("Nenhum alerta nesses números. Eles valem o que valem as entradas: confira cada custo com um orçamento real.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numeros", help="o numeros.json do negócio")
    ap.add_argument("--out", help="grava o relatório aqui (markdown)")
    ap.add_argument("--json", action="store_true", help="imprime os números em JSON")
    ap.add_argument("--preco", type=float, help="preço do cenário")
    ap.add_argument("--volume", type=float, default=1.0, help="multiplicador de volume do cenário")
    args = ap.parse_args(argv)
    try:
        spec = load(args.numeros)
        if args.preco is not None:
            spec = dict(spec, preco=args.preco)
        if args.volume != 1.0:
            spec = dict(spec)
            for k in ("rampa_por_dia", "rampa_por_mes", "novos_por_mes"):
                if k in spec:
                    spec[k] = [float(v) * args.volume for v in spec[k]]
            for k in ("plano_por_dia", "plano_por_mes"):
                if k in spec:
                    spec[k] = float(spec[k]) * args.volume
        a = analyse(spec)
    except NumbersError as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.endswith("_items")}
        out["breakeven"] = None if math.isinf(out["breakeven"]) else out["breakeven"]
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    text = report(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("gravado %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
