#!/usr/bin/env python3
"""Simples Nacional para o fundador-cfo: Anexos III e V, Fator R e RBT12. Só biblioteca padrão.

Tabelas da LC 123/2006 com a redação da LC 155/2016, sem mudança até 2026.
Confira em regras-br.md (fundador-brasil) a data da última verificação.

    alíquota efetiva = (RBT12 x alíquota nominal - parcela a deduzir) / RBT12

RBT12 é a receita bruta dos 12 meses anteriores. No início de atividade ela é
proporcional: no 1º mês, a receita do próprio mês x 12; do 2º ao 12º, a média dos
meses anteriores x 12. O Fator R (folha de 12 meses / RBT12) segue a mesma
proporção. Fator R >= 28%: Anexo III; abaixo: Anexo V.

    python3 simples.py 15000 --anexo V        # alíquota efetiva com R$ 15 mil por mês
"""

import argparse
import sys

TETO = 4_800_000.0
FATOR_R_MINIMO = 0.28

# (receita bruta em 12 meses até, alíquota nominal, parcela a deduzir)
ANEXOS = {
    "III": [(180_000, 0.060, 0), (360_000, 0.112, 9_360), (720_000, 0.135, 17_640),
            (1_800_000, 0.160, 35_640), (3_600_000, 0.210, 125_640), (4_800_000, 0.330, 648_000)],
    "V": [(180_000, 0.155, 0), (360_000, 0.180, 4_500), (720_000, 0.195, 9_900),
          (1_800_000, 0.205, 17_100), (3_600_000, 0.230, 62_100), (4_800_000, 0.305, 540_000)],
}
ANEXO_MODOS = ("III", "V", "fator_r")


class SimplesError(Exception):
    pass


def aliquota_efetiva(rbt12, anexo):
    """Alíquota efetiva para uma RBT12 num anexo. RBT12 zero usa a 1ª faixa."""
    if anexo not in ANEXOS:
        raise SimplesError("anexo é III ou V (veio %r)" % anexo)
    if rbt12 > TETO:
        raise SimplesError("RBT12 de R$ %.0f passa do teto do Simples (R$ 4,8 milhões)" % rbt12)
    if rbt12 <= 0:
        return ANEXOS[anexo][0][1]
    for limite, nominal, deduzir in ANEXOS[anexo]:
        if rbt12 <= limite:
            return (rbt12 * nominal - deduzir) / rbt12
    raise SimplesError("faixa não encontrada")  # inalcançável abaixo do teto


def _proporcional(serie, i):
    """Valor anualizado para o mês i (0 = primeiro mês), pela regra do início de atividade."""
    if i == 0:
        return serie[0] * 12
    anteriores = serie[max(0, i - 12):i]
    return sum(anteriores) / len(anteriores) * 12


def fator_r(folha12, rbt12):
    if rbt12 <= 0:
        return FATOR_R_MINIMO if folha12 > 0 else 0.01
    return folha12 / rbt12


def apurar(receitas, folhas, modo):
    """Para cada mês: (anexo, alíquota efetiva, Fator R, RBT12). modo é III, V ou fator_r."""
    if modo not in ANEXO_MODOS:
        raise SimplesError("'simples.anexo' é III, V ou fator_r (veio %r)" % modo)
    out = []
    for i in range(len(receitas)):
        rbt12 = _proporcional(receitas, i)
        r = fator_r(_proporcional(folhas, i), rbt12)
        anexo = modo if modo != "fator_r" else ("III" if r >= FATOR_R_MINIMO else "V")
        out.append((anexo, aliquota_efetiva(rbt12, anexo), r, rbt12))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("receita_mensal", type=float, help="receita média por mês, em reais")
    ap.add_argument("--anexo", default="V", choices=sorted(ANEXOS))
    a = ap.parse_args(argv)
    try:
        aliq = aliquota_efetiva(a.receita_mensal * 12, a.anexo)
    except SimplesError as e:
        print("erro: %s" % e, file=sys.stderr)
        return 2
    br = lambda v: "{:,.2f}".format(v).replace(",", "_").replace(".", ",").replace("_", ".")
    print("Anexo %s com RBT12 de R$ %s: alíquota efetiva de %s%%, R$ %s por mês."
          % (a.anexo, br(a.receita_mensal * 12), br(aliq * 100), br(aliq * a.receita_mensal)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
