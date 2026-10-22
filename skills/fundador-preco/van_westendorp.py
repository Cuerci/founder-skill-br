#!/usr/bin/env python3
"""Sensibilidade de preço (Van Westendorp) para o fundador-preco. Só biblioteca padrão.

Versão brasileira do van_westendorp.py do founder-skill (MIT, Jake Schincariol).
Cada respondente diz a que preço o produto seria barato demais para confiar, uma
pechincha, começando a ficar caro e caro demais para comprar. Juntas, as quatro
respostas dão a faixa de preço aceitável e o preço que deixa menos gente insatisfeita.

    python3 van_westendorp.py fundador/painel/respostas
    python3 van_westendorp.py respostas.csv --preco 50 --out fundador/curva-de-preco.md
    python3 van_westendorp.py fundador/painel/respostas --json

A entrada é a pasta de respostas do painel (um JSON por comprador, escrito pelo
fundador-consumidor) ou um CSV com as colunas muito_barato, barato, caro, muito_caro
(uma linha por respondente; outras colunas são ignoradas). O CSV exportado do Google
Forms ou do Excel brasileiro funciona: separador vírgula ou ponto e vírgula, valores
como "R$ 1.234,50" ou "50". Quem deixar um dos quatro em branco, ou responder fora de
ordem (muito barato tem que ser o menor, muito caro o maior), sai da conta e é contado.

Os quatro pontos:

    PMC  ponto de barateza marginal     abaixo dele, gente demais acha barato demais
    PME  ponto de carestia marginal     acima dele, gente demais acha caro demais
    OPP  preço ótimo                    tantos dizem "barato demais" quanto "caro demais"
    IPP  preço de indiferença           tantos dizem "pechincha" quanto "caro"

De PMC a PME é a faixa aceitável. Respostas de compradores simulados servem para
escolher o que TESTAR; depois teste com gente de verdade.
"""

import argparse
import csv
import glob
import json
import os
import sys

KEYS = ("muito_barato", "barato", "caro", "muito_caro")
ALIASES = {"muito_barato": ("too_cheap",), "barato": ("cheap",), "caro": ("expensive",),
           "muito_caro": ("too_expensive",)}


class PricingError(Exception):
    pass


def _f(v):
    """Lê 50, 49.9, "R$ 49,90" ou "1.234,50"."""
    if isinstance(v, (int, float)):
        x = float(v)
    else:
        t = str(v or "").replace("R$", "").replace("$", "").replace(" ", "").strip()
        if "," in t:
            t = t.replace(".", "").replace(",", ".")
        try:
            x = float(t)
        except ValueError:
            return None
    return x if x > 0 else None


def _get(row, key, prefix=""):
    for k in (key,) + ALIASES[key]:
        if prefix + k in row:
            return row[prefix + k]
    return None


def read(path):
    """Return (rows, dropped) where rows are (too_cheap, cheap, expensive, too_expensive)."""
    raw = []
    if os.path.isdir(path):
        for fp in sorted(glob.glob(os.path.join(path, "*.json"))):
            try:
                with open(fp, encoding="utf-8") as fh:
                    a = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError):
                raw.append(None)
                continue
            raw.append(tuple(_f(_get(a, k, "preco_")) for k in KEYS))
    elif path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig") as fh:
            sample = fh.read(4096)
            fh.seek(0)
            delim = ";" if sample.count(";") > sample.count(",") else ","
            for r in csv.DictReader(fh, delimiter=delim):
                r = {(k or "").strip().lower(): v for k, v in r.items()}
                raw.append(tuple(_f(_get(r, k)) for k in KEYS))
    else:
        raise PricingError("informe a pasta de respostas do painel ou um .csv")
    rows, dropped = [], 0
    for r in raw:
        if r is None or any(v is None for v in r) or not (r[0] <= r[1] <= r[2] <= r[3]):
            dropped += 1
            continue
        rows.append(r)
    return rows, dropped


def curves(rows, grid):
    n = float(len(rows))
    tc = [sum(1 for r in rows if r[0] >= p) / n for p in grid]          # too cheap at p (falls)
    ch = [sum(1 for r in rows if r[1] >= p) / n for p in grid]          # a bargain at p (falls)
    ex = [sum(1 for r in rows if r[2] <= p) / n for p in grid]          # expensive at p (rises)
    te = [sum(1 for r in rows if r[3] <= p) / n for p in grid]          # too expensive at p (rises)
    return tc, ch, ex, te


def cross(grid, falling, rising):
    """First price where the rising curve meets the falling one (linear interpolation)."""
    for i in range(1, len(grid)):
        d0 = rising[i - 1] - falling[i - 1]
        d1 = rising[i] - falling[i]
        if d0 <= 0 <= d1 and d1 != d0:
            t = -d0 / (d1 - d0)
            return grid[i - 1] + t * (grid[i] - grid[i - 1])
        if d0 == 0:
            return grid[i - 1]
    return None


def analyse(rows, step=None):
    if len(rows) < 5:
        raise PricingError("preciso de pelo menos 5 respostas completas (vieram %d)" % len(rows))
    lo = min(r[0] for r in rows)
    hi = max(r[3] for r in rows)
    step = step or max(0.01, round((hi - lo) / 400, 2))
    grid, p = [], lo
    while p <= hi + 1e-9:
        grid.append(round(p, 4))
        p += step
    tc, ch, ex, te = curves(rows, grid)
    not_cheap = [1 - v for v in ch]
    not_exp = [1 - v for v in ex]
    pts = {
        "PMC": cross(grid, tc, not_cheap),
        "PME": cross(grid, not_exp, te),
        "OPP": cross(grid, tc, te),
        "IPP": cross(grid, ch, ex),
    }
    return {"n": len(rows), "points": pts, "range": [pts["PMC"], pts["PME"]],
            "median": {k: sorted(r[i] for r in rows)[len(rows) // 2] for i, k in enumerate(KEYS)}}


def _money(v):
    return "n/d" if v is None else "R$ " + ("%.2f" % v).replace(".", ",")


def report(res, dropped, price=None):
    m = _money
    p = res["points"]
    L = ["# Sensibilidade de preço", "",
         "%d respostas completas%s. Se vieram do painel simulado, use para escolher o que testar, não como palavra final." % (
             res["n"], (", %d descartadas (incompletas ou fora de ordem)" % dropped) if dropped else ""), "",
         "| ponto | preço | o que significa |", "| --- | ---: | --- |",
         "| PMC | %s | abaixo dele, gente demais acha barato demais para ser bom |" % m(p["PMC"]),
         "| OPP | %s | tantos acham barato demais quanto caro demais: a menor resistência |" % m(p["OPP"]),
         "| IPP | %s | tantos acham pechincha quanto acham caro |" % m(p["IPP"]),
         "| PME | %s | acima dele, gente demais acha caro demais para comprar |" % m(p["PME"]), "",
         "**Faixa aceitável: %s a %s.**" % (m(p["PMC"]), m(p["PME"])), ""]
    md = res["median"]
    L.append("Medianas: barato demais %s, pechincha %s, ficando caro %s, caro demais %s." % (
        m(md["muito_barato"]), m(md["barato"]), m(md["caro"]), m(md["muito_caro"])))
    if price is not None and p["PMC"] is not None and p["PME"] is not None:
        where = "dentro da" if p["PMC"] <= price <= p["PME"] else ("abaixo da" if price < p["PMC"] else "acima da")
        L += ["", "O preço atual, %s, está **%s** faixa aceitável." % (m(price), where)]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("fonte", help="a pasta de respostas do painel, ou um CSV")
    ap.add_argument("--preco", type=float, help="o preço atual, para situar na faixa")
    ap.add_argument("--out", help="grava o relatório aqui (markdown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        rows, dropped = read(a.fonte)
        res = analyse(rows)
    except (PricingError, FileNotFoundError) as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(dict(res, dropped=dropped), indent=1))
        return 0
    text = report(res, dropped, a.preco)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("gravado %s" % a.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
