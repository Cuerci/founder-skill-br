"""Testes das ferramentas do fundador (versão brasileira).

    python3 -m unittest discover -s tests -v
"""

import importlib.util
import json
import math
import os
import shutil
import tempfile
import unittest

SKILLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")


def load(folder, name):
    spec = importlib.util.spec_from_file_location("fundador_" + name, os.path.join(SKILLS, folder, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ue = load("fundador-cfo", "economia_unitaria")
vw = load("fundador-preco", "van_westendorp")
pn = load("fundador-consumidor", "painel")
cp = load("fundador-plano", "compilar")


def example(name):
    with open(os.path.join(SKILLS, "fundador-cfo", name), encoding="utf-8") as fh:
        return json.load(fh)


class EconomiaUnitaria(unittest.TestCase):
    def test_modo_dia(self):
        a = ue.analyse(example("exemplo.json"))
        # 14 - 2,10 - 0,60 - 1,2% de 14 - 4% de 14
        self.assertAlmostEqual(a["contribution"], 14 - 2.70 - 14 * 0.052, places=6)
        self.assertEqual(math.ceil(a["breakeven"]), 50)
        self.assertEqual(a["flags"], [])

    def test_modo_assinatura(self):
        s = example("exemplo-assinatura.json")
        a = ue.analyse(s)
        self.assertAlmostEqual(a["months"][0]["units"], 10)
        self.assertAlmostEqual(a["months"][1]["units"], 10 * 0.92 + 15)
        self.assertAlmostEqual(a["ltv"], a["contribution"] / 0.08)
        self.assertEqual(math.ceil(a["breakeven"]), 15)
        self.assertEqual(len(ue.sensitivity(s)), 5)

    def test_modo_mes_venda_unica(self):
        s = example("exemplo-venda-unica.json")
        a = ue.analyse(s)
        self.assertEqual(a["period"], "mês")
        self.assertAlmostEqual(a["months"][0]["units"], 5)
        self.assertEqual(math.ceil(a["breakeven"]), math.ceil(450 / a["contribution"]))
        self.assertIn("vendas por mês", ue.report(s, a))

    def test_custo_de_aquisicao(self):
        s = example("exemplo-assinatura.json")
        base = ue.analyse(s)
        s["custo_aquisicao"] = 200
        a = ue.analyse(s)
        self.assertAlmostEqual(base["year1_profit"] - a["year1_profit"], 200 * sum(s["novos_por_mes"]))
        self.assertAlmostEqual(a["ltv_cac"], a["ltv"] / 200)
        self.assertTrue(any("LTV/CAC" in f for f in a["flags"]))

    def test_percentual_acompanha_o_preco(self):
        s = example("exemplo-assinatura.json")
        self.assertGreater(ue.analyse(s)["variable_per_unit"], ue.analyse(s, price=10)["variable_per_unit"])

    def test_preco_abaixo_do_custo_gera_alerta(self):
        s = example("exemplo.json")
        s["preco"] = 2.0
        a = ue.analyse(s)
        self.assertTrue(math.isinf(a["breakeven"]))
        self.assertTrue(any("prejuízo antes dos custos fixos" in f for f in a["flags"]))

    def test_entrada_ruim_e_recusada(self):
        s = example("exemplo-assinatura.json")
        del s["churn_mensal"]
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)
        s = example("exemplo.json")
        s["rampa_por_dia"] = [1] * 11
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)
        s = example("exemplo.json")
        s["fixo_mensal"][0] = {"item": "x", "percentual": 0.1}
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)

    def test_formato_brasileiro(self):
        self.assertEqual(ue._money(1234.5), "R$ 1.234,50")
        self.assertEqual(ue._whole(-55900), "-R$ 55.900")
        self.assertEqual(ue._pct(0.0099), "0,99%")
        s = example("exemplo-assinatura.json")
        self.assertIn("R$ 49,90", ue.report(s, ue.analyse(s)))


class VanWestendorp(unittest.TestCase):
    def test_csv_do_google_forms(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        path = os.path.join(d, "r.csv")
        with open(path, "w", encoding="utf-8-sig") as fh:
            fh.write("Carimbo;Muito_Barato;Barato;Caro;Muito_Caro\n"
                     '1;"R$ 10,00";20;60;90\n2;15;30;50;80\n3;10;25;45;70\n4;"R$ 20";35;70;120\n'
                     "5;5;20;40;60\n6;12;28;55;85\n7;30;20;10;5\n")
        rows, dropped = vw.read(path)
        self.assertEqual((len(rows), dropped), (6, 1))
        res = vw.analyse(rows)
        self.assertLess(res["points"]["PMC"], res["points"]["PME"])
        self.assertIn("dentro da", vw.report(res, dropped, 50))

    def test_numeros(self):
        self.assertEqual(vw._f("R$ 1.234,50"), 1234.5)
        self.assertEqual(vw._f("49.9"), 49.9)
        self.assertIsNone(vw._f(""))


class Painel(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d)
        self.pd = os.path.join(self.d, "painel")
        base = os.path.join(SKILLS, "fundador-consumidor")
        pn.init(self.pd, os.path.join(base, "cliente.exemplo.json"), os.path.join(base, "pitch.exemplo.md"), n=10, seed=3)

    def test_mesma_seed_mesmas_fichas(self):
        with open(os.path.join(SKILLS, "fundador-consumidor", "cliente.exemplo.json"), encoding="utf-8") as fh:
            c = json.load(fh)
        self.assertEqual(pn.deal(c, 10, 3), pn.deal(c, 10, 3))

    def test_briefing_em_portugues_e_apuracao(self):
        waves = pn.write_briefs(self.pd)
        self.assertEqual(sum(len(w) for w in waves), 10)
        with open(waves[0][0][1], encoding="utf-8") as fh:
            brief = fh.read()
        self.assertIn("por mês", brief)
        self.assertIn('"preco_muito_caro"', brief)
        _, cards = pn.load_state(self.pd)
        for i, c in enumerate(cards):
            pn._write_json(os.path.join(self.pd, "respostas", c["id"] + ".json"), {
                "id": c["id"], "compra": i < 3, "motivo_codigo": "preco", "motivo": "caro",
                "compras_primeiro_mes": 2, "mudaria_de_ideia": "desconto",
                "preco_muito_barato": 3, "preco_barato": 6, "preco_caro": 12, "preco_muito_caro": 18})
        self.assertEqual(pn.check(self.pd), [])
        res = pn.tally(self.pd)
        self.assertEqual((res["buys"], res["passes"], res["price_answers"]), (3, 7, 10))
        self.assertIn("3 compram · 7 passam", pn.results_md(res))
        rows, _ = vw.read(os.path.join(self.pd, "respostas"))
        self.assertEqual(len(rows), 10)

    def test_resposta_invalida(self):
        _, cards = pn.load_state(self.pd)
        pid = cards[0]["id"]
        with self.assertRaises(pn.PanelError):
            pn.save(self.pd, pid, '{"id": "%s", "compra": "sim"}' % pid)


class Plano(unittest.TestCase):
    def test_veredito(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        self.assertEqual(cp.verdict(d)[0], "Incompleto")
        shutil.copy(os.path.join(SKILLS, "fundador-cfo", "exemplo-assinatura.json"), os.path.join(d, "numeros.json"))
        self.assertEqual(cp.verdict(d)[0], "Lucrativo")
        os.makedirs(os.path.join(d, "painel"))
        with open(os.path.join(d, "painel", "resultados.json"), "w") as fh:
            json.dump({"buy_rate": 0.1, "buys": 2, "passes": 18, "answered": 20}, fh)
        v, text = cp.compile_plan(d)
        self.assertEqual(v, "Ainda não")
        self.assertIn("LTV por assinante", text)
        self.assertIn("rode /fundador-conselho", text)


if __name__ == "__main__":
    unittest.main()
