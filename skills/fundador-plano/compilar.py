#!/usr/bin/env python3
"""Compila o plano de negócio do fundador-plano. Só biblioteca padrão, sem rede.

Versão brasileira do compile.py do founder-skill (MIT, Jake Schincariol).
Lê tudo o que as outras skills gravaram em fundador/ e monta um documento,
fundador/plano-de-negocio.md, com um veredito no topo. O veredito é calculado
pelos números, nunca escrito à mão:

    Lucrativo    toda checagem que tem dados passa
    Ainda não    pelo menos uma checagem falha (cada falha listada com o número)
    Incompleto   ainda não há números (rode o fundador-cfo antes)

As checagens:
    1. cada unidade dá dinheiro antes dos custos fixos   (fundador/numeros.json)
    2. o ano 1 dá lucro operacional                       (fundador/numeros.json)
    3. o ponto de equilíbrio cabe na capacidade, se houver capacidade
    4. parte suficiente do painel compra                   (fundador/painel/resultados.json, --taxa-minima, padrão 25%)

    python3 compilar.py                     # lê ./fundador, grava ./fundador/plano-de-negocio.md
    python3 compilar.py --dir caminho/fundador --taxa-minima 0.3
    python3 compilar.py --check             # imprime o veredito e sai com 0 (Lucrativo) ou 1
"""

import argparse
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = [  # (arquivo em fundador/, título, skill que escreve)
    ("resumo.md", "Resumo", "fundador-plano"),
    ("conselho.md", "O que o conselho disse", "fundador-conselho"),
    ("mercado.md", "O mercado no Brasil", "fundador-brasil"),
    ("concorrentes.md", "A concorrência", "fundador-concorrentes"),
    ("painel/resultados.md", "O painel de compradores", "fundador-consumidor"),
    ("preco.md", "Preço", "fundador-preco"),
    ("oferta.md", "A oferta", "fundador-oferta"),
    ("cfo.md", "Os números", "fundador-cfo"),
    ("marketing.md", "Marketing", "fundador-marketing"),
    ("marca.md", "Marca", "fundador-marca"),
    ("operacoes.md", "Operação", "fundador-operacoes"),
    ("lancamento.md", "Plano de lançamento", "fundador-lancamento"),
]


def _load_unit_economics():
    path = os.path.join(HERE, "..", "fundador-cfo", "economia_unitaria.py")
    spec = importlib.util.spec_from_file_location("fundador_economia_unitaria", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None


def _strip_h1(text):
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    # rebaixa os títulos um nível para caberem sob o título da seção
    return "\n".join(("#" + l) if l.startswith("#") else l for l in lines).strip()


def verdict(d, min_buy_rate=0.25):
    """Devolve (veredito, checagens, números, painel). checagens = [(ok, texto)]."""
    checks = []
    numbers = panel = None
    raw = _read(os.path.join(d, "numeros.json"))
    if raw:
        ue = _load_unit_economics()
        numbers = ue.analyse(json.loads(raw))
        u = numbers["unit"]
        c = numbers["contribution"]
        checks.append((c > 0, "Cada %s deixa %s antes dos custos fixos (%s de margem de contribuição)." % (
            u, ue._money(c), ue._pct(numbers["contribution_pct"])) if c > 0
            else "Cada %s DÁ PREJUÍZO de %s antes dos custos fixos." % (u, ue._money(-c))))
        y = numbers["year1_profit"]
        checks.append((y > 0, "Lucro operacional do ano 1: %s." % ue._whole(y) if y > 0
                       else "PREJUÍZO operacional no ano 1: %s." % ue._whole(-y)))
        be, cap = numbers["breakeven"], numbers["capacity"]
        if cap is not None:
            fits = not math.isinf(be) and be <= float(cap)
            what = {"assinatura": "assinantes", "mes": "por mês"}.get(numbers["mode"], "por dia")
            checks.append((fits, "O equilíbrio é %s %s, contra uma capacidade de %s." % (ue._be(be), what, cap)))
    raw = _read(os.path.join(d, "painel", "resultados.json"))
    if raw:
        panel = json.loads(raw)
        r = panel["buy_rate"]
        checks.append((r >= min_buy_rate, "%d de %d compradores simulados compram (%.0f%%, a régua é %.0f%%)." % (
            panel["buys"], panel["answered"], r * 100, min_buy_rate * 100)))
    if numbers is None:
        v = "Incompleto"
    elif all(ok for ok, _ in checks):
        v = "Lucrativo"
    else:
        v = "Ainda não"
    return v, checks, numbers, panel


def compile_plan(d, min_buy_rate=0.25):
    idea = _read(os.path.join(d, "ideia.md"))
    name = None
    if idea:
        first = idea.splitlines()[0]
        name = first[2:].strip() if first.startswith("# ") else None
    v, checks, numbers, panel = verdict(d, min_buy_rate)
    title = name or (numbers["business"] if numbers and numbers.get("business") else "Seu negócio")
    L = ["# %s · Plano de negócio" % title, ""]
    L.append("**Veredito: %s**" % v)
    L.append("")
    for ok, text in checks:
        L.append("- %s %s" % ("✓" if ok else "✗", text))
    if v == "Incompleto":
        L.append("- Ainda não há números. Rode /fundador-cfo e compile de novo.")
    L.append("")
    if numbers:
        ue = _load_unit_economics()
        sub = numbers["mode"] == "assinatura"
        L += ["| número-chave | |", "| --- | ---: |",
              "| Preço | %s por %s |" % (ue._money(numbers["price"]), numbers["unit"]),
              "| Margem de lucro no plano | %s |" % ue._pct(numbers["margin_at_plan"]),
              "| Ponto de equilíbrio | %s %s |" % (ue._be(numbers["breakeven"]), {
                  "assinatura": "assinantes ativos", "mes": "vendas por mês"}.get(numbers["mode"], "por dia")),
              "| Lucro operacional do ano 1 | %s |" % ue._whole(numbers["year1_profit"]),
              "| Investimento inicial | %s |" % ue._whole(numbers["startup"]),
              "| Caixa necessário antes de se pagar | %s |" % ue._whole(numbers["cash_needed"]),
              "| Investimento recuperado | %s |" % ("no mês %d" % numbers["payback_month"] if numbers["payback_month"] else "não no ano 1")]
        if sub and numbers["ltv"] is not None:
            L.append("| LTV por assinante | %s |" % ue._money(numbers["ltv"]))
        if panel:
            L.append("| Painel de compradores | %d compram · %d passam |" % (panel["buys"], panel["passes"]))
        L.append("")
    if idea:
        L += ["## A ideia", "", _strip_h1(idea), ""]
    missing = []
    for fname, heading, skill in SECTIONS:
        text = _read(os.path.join(d, fname))
        if text:
            L += ["## %s" % heading, "", _strip_h1(text), ""]
        else:
            missing.append((heading, skill))
    if missing:
        L += ["## O que falta", ""]
        for heading, skill in missing:
            L.append("- %s: rode /%s" % (heading, skill))
        L.append("")
    L.append("_O painel é de compradores simulados e os números são projeções a partir das suas entradas. Confirme a"
             " demanda com clientes reais e os custos com orçamentos reais antes de gastar. Não é aconselhamento"
             " financeiro, jurídico nem tributário; confirme com um contador._")
    return v, "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="fundador")
    ap.add_argument("--taxa-minima", type=float, default=0.25)
    ap.add_argument("--check", action="store_true", help="só imprime o veredito; sai com 0 se Lucrativo")
    ap.add_argument("--out", help="padrão: <dir>/plano-de-negocio.md")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dir):
        print("erro: não há pasta %s/ aqui. Rode as outras skills do fundador antes." % a.dir, file=sys.stderr)
        return 2
    v, text = compile_plan(a.dir, a.taxa_minima)
    if a.check:
        _, checks, _, _ = verdict(a.dir, a.taxa_minima)
        print("Veredito: %s" % v)
        for ok, t in checks:
            print("  %s %s" % ("✓" if ok else "✗", t))
        return 0 if v == "Lucrativo" else 1
    out = a.out or os.path.join(a.dir, "plano-de-negocio.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("Veredito: %s. Gravado %s" % (v, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
