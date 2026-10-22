#!/usr/bin/env python3
"""O painel de compradores do fundador-consumidor. Só biblioteca padrão, sem rede.

Versão brasileira do panel.py do founder-skill (MIT, Jake Schincariol).
Cuida da contabilidade de um enxame de compradores simulados: distribui uma ficha
de persona por comprador a partir do perfil do cliente-alvo (renda mensal, idade,
comportamento, objeção), escreve um briefing por comprador para um subagente
responder, confere as respostas e apura quem compra, quem não compra e por quê.

    python3 painel.py init --cliente fundador/cliente.json --pitch fundador/pitch.md [--n 100] [--seed 7]
    python3 painel.py prompts [--onda 10]    # um briefing por comprador que falta, em ondas
    python3 painel.py check                  # respostas faltando ou quebradas
    python3 painel.py save P003 < resposta.txt  # arquiva o JSON que o comprador imprimiu em vez de gravar
    python3 painel.py tally [--out fundador/painel/resultados.md]
    python3 painel.py status

O estado fica em fundador/painel/ (--dir para mudar): painel.json, personas.json,
briefings/<id>.md, respostas/<id>.json, resultados.md, resultados.json.

A ferramenta nunca responde por um comprador. Todo número em resultados.md é contado
dos arquivos que os subagentes escreveram. Compradores simulados acham objeções e
pontos fracos rápido e barato. Não são clientes: confirme o que importa com gente
de verdade (pré-venda, lista de espera, página com preço).
"""

import argparse
import json
import os
import random
import sys

FIRST_NAMES = [
    "Ana", "Beatriz", "Bruno", "Camila", "Caio", "Carla", "Daniel", "Débora", "Diego", "Eduarda", "Felipe",
    "Fernanda", "Gabriel", "Giovana", "Gustavo", "Helena", "Henrique", "Isabela", "Igor", "Jéssica", "João",
    "Juliana", "Kaique", "Larissa", "Leandro", "Letícia", "Lucas", "Luana", "Marcelo", "Mariana", "Mateus",
    "Michele", "Murilo", "Natália", "Otávio", "Paula", "Pedro", "Priscila", "Rafael", "Raquel", "Renato", "Roberta",
    "Rodrigo", "Sabrina", "Samuel", "Tainá", "Thiago", "Vanessa", "Vinícius", "Yasmin", "Wesley", "Aline",
    "Anderson", "Bianca", "Breno", "Cíntia", "Cléber", "Dandara", "Davi", "Elaine", "Emerson", "Fabiana", "Fábio",
    "Gisele", "Hugo", "Ingrid", "Jefferson", "Joana", "Kelly", "Leonardo", "Lorena", "Márcio", "Milena", "Nathan",
    "Patrícia", "Railson", "Rayssa", "Ricardo", "Simone", "Tiago", "Valéria", "Wagner", "Alessandra", "Arthur",
    "Bárbara", "Cristiano", "Daiane", "Elias", "Flávia", "Guilherme", "Iara", "Jonas", "Kátia", "Luiz", "Marcela",
    "Nicolas", "Pâmela", "Rogério", "Sueli", "Thalita", "Ubirajara", "Vitória", "Weslley", "Zé",
]
REASONS = ["preco", "habito", "necessidade", "confianca", "qualidade", "conveniencia", "momento", "valores", "outro"]
ANSWER_FIELDS = {"id", "compra", "motivo_codigo", "motivo"}
WAVE = 10


class PanelError(Exception):
    pass


# ── dealing ─────────────────────────────────────────────────────────────────────
def _quota(items, n, key="share"):
    """Split n across items by their shares, exactly (largest remainder)."""
    total = sum(float(it.get(key, 1)) for it in items) or 1.0
    raw = [n * float(it.get(key, 1)) / total for it in items]
    counts = [int(r) for r in raw]
    order = sorted(range(len(items)), key=lambda i: raw[i] - counts[i], reverse=True)
    for i in order[: n - sum(counts)]:
        counts[i] += 1
    return counts


def validate_customer(c):
    for k in ("negocio", "alvo", "segmentos", "comportamentos", "objecoes"):
        if k not in c or c[k] in ("", [], None):
            raise PanelError("cliente.json precisa de '%s'" % k)
    for s in c["segmentos"]:
        if "nome" not in s or "renda_mensal" not in s or len(s["renda_mensal"]) != 2:
            raise PanelError("todo segmento precisa de nome e renda_mensal [mínima, máxima]")
    for b in c["comportamentos"]:
        if "nome" not in b:
            raise PanelError("todo comportamento precisa de nome")


def deal(customer, n=100, seed=7):
    """Deal n persona cards. Same customer + n + seed = the same cards, every time."""
    validate_customer(customer)
    if n < 1:
        raise PanelError("--n precisa ser pelo menos 1")
    rng = random.Random(seed)
    age = customer.get("idade", [25, 45])
    segs = []
    for s, k in zip(customer["segmentos"], _quota(customer["segmentos"], n)):
        segs += [s] * k
    behs = []
    for b, k in zip(customer["comportamentos"], _quota(customer["comportamentos"], n)):
        behs += [b] * k
    rng.shuffle(segs)
    rng.shuffle(behs)
    names = FIRST_NAMES[:]
    rng.shuffle(names)
    while len(names) < n:
        names += ["%s %d" % (x, len(names) // len(FIRST_NAMES) + 1) for x in FIRST_NAMES]
    objections = customer["objecoes"]
    habits = customer.get("habitos") or []
    cards = []
    for i in range(n):
        s, b = segs[i], behs[i]
        lo, hi = float(s["renda_mensal"][0]), float(s["renda_mensal"][1])
        cards.append({
            "id": "P%03d" % (i + 1),
            "name": names[i],
            "age": rng.randint(int(age[0]), int(age[1])),
            "segment": s["nome"],
            "income": int(round(rng.uniform(lo, hi), -2)),
            "behaviour": b["nome"],
            "behaviour_how": b.get("como", ""),
            "objection": objections[rng.randrange(len(objections))],
            "habit": habits[rng.randrange(len(habits))] if habits else "",
        })
    return cards


# ── state ───────────────────────────────────────────────────────────────────────
def _path(d, *p):
    return os.path.join(d, *p)


def _read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def init(d, customer_path, pitch_path, n=100, seed=None):
    try:
        customer = _read_json(customer_path)
    except FileNotFoundError:
        raise PanelError("arquivo não existe: %s" % customer_path)
    try:
        with open(pitch_path, encoding="utf-8") as fh:
            pitch = fh.read().strip()
    except FileNotFoundError:
        raise PanelError("arquivo não existe: %s (escreva o pitch antes: o que vende, o preço, onde)" % pitch_path)
    if not pitch:
        raise PanelError("o pitch está vazio")
    if seed is None:
        seed = random.SystemRandom().randrange(1, 10 ** 6)
    cards = deal(customer, n, seed)
    _write_json(_path(d, "panel.json"), {"n": n, "seed": seed, "customer": customer, "pitch": pitch})
    _write_json(_path(d, "personas.json"), cards)
    os.makedirs(_path(d, "briefings"), exist_ok=True)
    os.makedirs(_path(d, "respostas"), exist_ok=True)
    return cards


def load_state(d):
    try:
        return _read_json(_path(d, "panel.json")), _read_json(_path(d, "personas.json"))
    except FileNotFoundError:
        raise PanelError("não há painel em %s: rode init antes" % d)


BRIEF = """Você é um comprador simulado num painel de consumidores. Um empreendedor quer saber, antes de gastar qualquer dinheiro, se pessoas reais como você comprariam. Sua resposta só serve se for honesta: a maioria das pessoas não compra a maioria das coisas, e um sim por educação é pior que um não claro.

=== QUEM VOCÊ É ===
{name}, {age} anos. {segment}. Você ganha cerca de R$ {income_br} por mês.
Como você compra: {behaviour}. {behaviour_how}
{habit_line}A primeira coisa que vem à cabeça quando você ouve uma oferta assim: "{objection}"
Você é uma destas pessoas: {target}.
=== FIM ===

=== O QUE ESTÁ SENDO OFERECIDO (você vê pela primeira vez, como quem passa na rua ou rola o feed) ===
{pitch}
=== FIM ===

Decida como {name} decidiria, com o dinheiro, os hábitos e as dúvidas de {name}, numa semana normal. Não seja agradável. Não invente fatos sobre o negócio além do que está escrito acima. Responda em português do Brasil, com o seu jeito de falar.

Crie o arquivo {out} com a sua ferramenta de escrever arquivos (não só imprima a resposta) contendo APENAS este JSON, sem cerca de markdown, nada mais:
{{
  "id": "{id}",
  "compra": true ou false,
  "compras_primeiro_mes": quantas vezes você compraria no primeiro mês (0 se não compraria),
  "motivo_codigo": um de {reasons},
  "motivo": "por quê, em uma ou duas frases, do seu jeito",
  "objecao": "a dúvida que mais pesa para você, com as suas palavras",
  "mudaria_de_ideia": "a única coisa que viraria a sua resposta, ou vazio",
  "preco_muito_barato": o preço em reais a partir do qual pareceria barato demais para prestar (um número),
  "preco_barato": o preço em reais que pareceria uma pechincha (um número),
  "preco_caro": o preço em reais que começa a parecer caro, mas talvez você ainda comprasse (um número),
  "preco_muito_caro": o preço em reais em que você não compraria de jeito nenhum (um número)
}}
"""


def write_briefs(d, wave=WAVE):
    state, cards = load_state(d)
    target = state["customer"]["alvo"]
    todo = []
    for c in cards:
        out = _path(d, "respostas", c["id"] + ".json")
        if _answer_ok(out, c["id"]) is None:
            continue
        brief = BRIEF.format(pitch=state["pitch"], target=target, out=os.path.abspath(out),
                             habit_line=("Seu dia a dia: %s.\n" % c["habit"]) if c.get("habit") else "",
                             income_br="{:,}".format(c["income"]).replace(",", "."),
                             reasons=" / ".join(REASONS), **c)
        bp = _path(d, "briefings", c["id"] + ".md")
        with open(bp, "w", encoding="utf-8") as fh:
            fh.write(brief)
        todo.append((c["id"], os.path.abspath(bp)))
    waves = [todo[i:i + wave] for i in range(0, len(todo), wave)]
    return waves


def _answer_ok(path, pid):
    """None if the answer file is good, else a short problem string."""
    if not os.path.exists(path):
        return "faltando"
    try:
        a = _read_json(path)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "JSON inválido"
    missing = ANSWER_FIELDS - set(a)
    if missing:
        return "faltam " + ", ".join(sorted(missing))
    if a.get("id") != pid:
        return "id é %r, esperado %s" % (a.get("id"), pid)
    if not isinstance(a.get("compra"), bool):
        return "'compra' precisa ser true ou false"
    if a.get("motivo_codigo") not in REASONS:
        return "motivo_codigo %r não é um de %s" % (a.get("motivo_codigo"), ", ".join(REASONS))
    return None


def save(d, pid, text):
    """File a buyer's OWN answer that it printed instead of writing. Never used to answer for a buyer."""
    _, cards = load_state(d)
    if pid not in {c["id"] for c in cards}:
        raise PanelError("não há comprador %s neste painel" % pid)
    start = text.find("{")
    if start < 0:
        raise PanelError("nenhum objeto JSON na resposta")
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError as e:
        raise PanelError("o JSON da resposta não é válido: %s" % e)
    path = _path(d, "respostas", pid + ".json")
    _write_json(path, obj)
    prob = _answer_ok(path, pid)
    if prob:
        os.remove(path)
        raise PanelError("a resposta de %s não é válida (%s); rode o briefing de novo" % (pid, prob))
    return path


def check(d):
    _, cards = load_state(d)
    probs = []
    for c in cards:
        p = _answer_ok(_path(d, "respostas", c["id"] + ".json"), c["id"])
        if p:
            probs.append((c["id"], p))
    return probs


# ── tally ───────────────────────────────────────────────────────────────────────
def _rate(rows):
    return (sum(1 for r in rows if r["compra"]) / len(rows)) if rows else 0.0


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def tally(d):
    state, cards = load_state(d)
    by_id = {c["id"]: c for c in cards}
    rows, skipped = [], []
    for c in cards:
        path = _path(d, "respostas", c["id"] + ".json")
        p = _answer_ok(path, c["id"])
        if p:
            skipped.append((c["id"], p))
            continue
        a = _read_json(path)
        rows.append(dict(by_id[c["id"]], **{k: v for k, v in a.items() if k != "id"}, id=c["id"]))
    if not rows:
        raise PanelError("nenhuma resposta válida ainda: rode os briefings antes (painel.py prompts)")

    def group(key):
        out = {}
        for r in rows:
            out.setdefault(r[key], []).append(r)
        return sorted(((k, len(v), _rate(v)) for k, v in out.items()), key=lambda t: -t[2])

    # renda em terços da faixa distribuída, para as faixas significarem o mesmo a cada rodada
    incomes = sorted(r["income"] for r in rows)
    cut1, cut2 = incomes[len(incomes) // 3], incomes[2 * len(incomes) // 3]
    br = lambda v: "R$ " + "{:,}".format(v).replace(",", ".")
    for r in rows:
        r["income_band"] = ("abaixo de %s/mês" % br(cut1)) if r["income"] < cut1 else (
            ("%s/mês ou mais" % br(cut2)) if r["income"] >= cut2 else "%s a %s/mês" % (br(cut1), br(cut2)))

    no = [r for r in rows if not r["compra"]]
    yes = [r for r in rows if r["compra"]]

    def reasons(rs):
        out = {}
        for r in rs:
            out.setdefault(r["motivo_codigo"], []).append(r)
        return sorted(((k, v) for k, v in out.items()), key=lambda kv: -len(kv[1]))

    def mean(vals):
        vals = [v for v in vals if v is not None]
        return sum(vals) / len(vals) if vals else None

    res = {
        "business": state["customer"]["negocio"], "seed": state["seed"], "dealt": len(cards),
        "answered": len(rows), "skipped": skipped, "buys": len(yes), "passes": len(no),
        "buy_rate": len(yes) / len(rows),
        "by_segment": group("segment"), "by_behaviour": group("behaviour"), "by_income": group("income_band"),
        "why_not": [(k, len(v), [r["motivo"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in reasons(no)],
        "why_yes": [(k, len(v), [r["motivo"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in reasons(yes)],
        "flip": [r["mudaria_de_ideia"] for r in no if (r.get("mudaria_de_ideia") or "").strip()],
        "purchases_first_month_per_buyer": mean([_num(r.get("compras_primeiro_mes")) for r in yes]),
        "price_answers": sum(1 for r in rows if all(_num(r.get(k)) is not None for k in
                                                     ("preco_muito_barato", "preco_barato", "preco_caro", "preco_muito_caro"))),
    }
    return res


def results_md(res):
    pct = lambda v: "%.0f%%" % (v * 100)
    L = ["# Painel de compradores: %s" % res["business"], ""]
    L.append("**%d compram · %d passam** (%s compram) de %d compradores simulados. Seed %s, para distribuir as mesmas fichas de novo."
             % (res["buys"], res["passes"], pct(res["buy_rate"]), res["answered"], res["seed"]))
    if res["skipped"]:
        L.append("")
        L.append("%d de %d compradores não têm resposta válida e ficaram de fora: %s." % (
            len(res["skipped"]), res["dealt"], ", ".join("%s (%s)" % s for s in res["skipped"][:10])))
    L.append("")
    L.append("São compradores simulados, não clientes. Use para achar objeções e pontos fracos e confirme as grandes"
             " com gente de verdade antes de gastar.")
    for title, key in (("Por segmento", "by_segment"), ("Por comportamento de compra", "by_behaviour"), ("Por renda", "by_income")):
        L += ["", "## %s" % title, "", "| grupo | compradores | taxa de compra |", "| --- | ---: | ---: |"]
        for k, n, r in res[key]:
            L.append("| %s | %d | %s%s |" % (k, n, pct(r), "  (pouca gente)" if n < 8 else ""))
    L += ["", "## Por que passam", "", "| motivo | compradores | nas palavras deles |", "| --- | ---: | --- |"]
    for k, n, quotes, ids in res["why_not"]:
        L.append("| %s | %d | %s |" % (k, n, " · ".join('"%s" (%s)' % (q.replace("|", "/"), i) for q, i in zip(quotes, ids))))
    L += ["", "## Por que compram", "", "| motivo | compradores | nas palavras deles |", "| --- | ---: | --- |"]
    for k, n, quotes, ids in res["why_yes"]:
        L.append("| %s | %d | %s |" % (k, n, " · ".join('"%s" (%s)' % (q.replace("|", "/"), i) for q, i in zip(quotes, ids))))
    if res["flip"]:
        L += ["", "## O que viraria um não", ""]
        for f in res["flip"][:12]:
            L.append("- %s" % f)
    if res["purchases_first_month_per_buyer"] is not None:
        L += ["", "Quem compra diz que compraria **%.1f vezes** no primeiro mês, em média." % res["purchases_first_month_per_buyer"]]
    if res["price_answers"]:
        L += ["", "%d compradores deram as quatro respostas de preço. Rode o van_westendorp.py do fundador-preco na pasta respostas." % res["price_answers"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default=os.path.join("fundador", "painel"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--cliente", required=True)
    i.add_argument("--pitch", required=True)
    i.add_argument("--n", type=int, default=100)
    i.add_argument("--seed", type=int)
    p = sub.add_parser("prompts")
    p.add_argument("--onda", type=int, default=WAVE)
    sub.add_parser("check")
    sv = sub.add_parser("save")
    sv.add_argument("id")
    t = sub.add_parser("tally")
    t.add_argument("--out")
    sub.add_parser("status")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "init":
            cards = init(a.dir, a.cliente, a.pitch, a.n, a.seed)
            st, _ = load_state(a.dir)
            print("%d compradores distribuídos (seed %s) em %s. Próximo: painel.py prompts" % (len(cards), st["seed"], a.dir))
        elif a.cmd == "prompts":
            waves = write_briefs(a.dir, a.onda)
            n = sum(len(w) for w in waves)
            if not n:
                print("todo comprador tem resposta válida. Próximo: painel.py tally")
            else:
                print("%d briefings em %d ondas de até %d. Lance uma onda por vez:" % (n, len(waves), a.onda))
                for k, w in enumerate(waves, 1):
                    print("onda %d: %s" % (k, " ".join("%s=%s" % job for job in w)))
        elif a.cmd == "check":
            probs = check(a.dir)
            if not probs:
                print("todas as respostas presentes e válidas")
            for pid, prob in probs:
                print("%s: %s" % (pid, prob))
            return 1 if probs else 0
        elif a.cmd == "save":
            print("salvo %s" % save(a.dir, a.id, sys.stdin.read()))
        elif a.cmd == "tally":
            res = tally(a.dir)
            text = results_md(res)
            out = a.out or _path(a.dir, "resultados.md")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(text)
            _write_json(_path(a.dir, "resultados.json"), res)
            print("%d compram · %d passam (%.0f%%). Gravado %s" % (res["buys"], res["passes"], res["buy_rate"] * 100, out))
        elif a.cmd == "status":
            st, cards = load_state(a.dir)
            probs = check(a.dir)
            print("%d compradores (seed %s), %d responderam, faltam %d" % (len(cards), st["seed"], len(cards) - len(probs), len(probs)))
    except PanelError as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
